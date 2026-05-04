import base64
import re
import sqlite3
import tempfile
from datetime import date, datetime, timedelta, timezone

import airportsdata
import pandas as pd
import requests
import streamlit as st
import yaml

# ============ CONFIG ============
st.set_page_config(page_title="Flight Tracker", page_icon="✈️", layout="centered")

REPO = st.secrets.get("GITHUB_REPO", "")
BRANCH = st.secrets.get("GITHUB_BRANCH", "main")
TOKEN = st.secrets.get("GITHUB_TOKEN", "")
SEARCHES_PATH = "flight-tracker/data/searches.yaml"
DB_PATH = "flight-tracker/data/flights.db"

CLASSE_OPTS = {
    "Econômica": "ECONOMY",
    "Econômica Premium": "PREMIUM_ECONOMY",
    "Executiva": "BUSINESS",
    "Primeira Classe": "FIRST",
}


# ============ AEROPORTOS ============
@st.cache_data
def load_airports():
    data = airportsdata.load("IATA")
    return {k: v for k, v in data.items() if k and len(k) == 3 and v.get("city")}


def airport_label(iata):
    a = load_airports().get(iata)
    if not a:
        return iata
    return f"{iata} — {a.get('city', '')}, {a.get('country', '')}"


def airport_options():
    return sorted(load_airports().keys())


# ============ GITHUB IO ============
def _gh_headers():
    return {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
    }


@st.cache_data(ttl=60)
def fetch_searches():
    url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{SEARCHES_PATH}"
    r = requests.get(url, timeout=10)
    if r.status_code != 200:
        return []
    return yaml.safe_load(r.text) or []


def fetch_file_sha(path):
    url = f"https://api.github.com/repos/{REPO}/contents/{path}?ref={BRANCH}"
    r = requests.get(url, headers=_gh_headers(), timeout=10)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json()["sha"]


def write_searches(searches, message):
    sha = fetch_file_sha(SEARCHES_PATH)
    content = yaml.safe_dump(searches, allow_unicode=True, sort_keys=False)
    body = {
        "message": message,
        "content": base64.b64encode(content.encode("utf-8")).decode(),
        "branch": BRANCH,
    }
    if sha:
        body["sha"] = sha
    url = f"https://api.github.com/repos/{REPO}/contents/{SEARCHES_PATH}"
    r = requests.put(url, headers=_gh_headers(), json=body, timeout=15)
    r.raise_for_status()


@st.cache_data(ttl=60)
def fetch_db_stats():
    url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{DB_PATH}"
    r = requests.get(url, timeout=20)
    if r.status_code != 200:
        return {}

    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        f.write(r.content)
        tmp_path = f.name

    conn = sqlite3.connect(tmp_path)
    conn.row_factory = sqlite3.Row
    stats = {}
    try:
        rows = conn.execute(
            """SELECT search_id, MIN(preco) AS min_p, AVG(preco) AS avg_p,
                      COUNT(*) AS n, MAX(coletado_em) AS last_check
               FROM price_history GROUP BY search_id"""
        ).fetchall()
    except sqlite3.OperationalError:
        conn.close()
        return {}

    cutoff = (datetime.now(timezone.utc) - timedelta(days=60)).isoformat()

    for row in rows:
        sid = row["search_id"]
        stats[sid] = {
            "min_p": row["min_p"],
            "avg_p": row["avg_p"],
            "n": row["n"],
            "last_check": row["last_check"],
        }

        cur = conn.execute(
            """SELECT preco FROM price_history
               WHERE search_id = ? ORDER BY coletado_em DESC LIMIT 1""",
            (sid,),
        ).fetchone()
        if cur:
            stats[sid]["preco_atual"] = cur["preco"]

        series = conn.execute(
            """SELECT substr(coletado_em, 1, 10) AS dia, MIN(preco) AS preco
               FROM price_history
               WHERE search_id = ? AND coletado_em >= ?
               GROUP BY substr(coletado_em, 1, 10)
               ORDER BY dia ASC""",
            (sid, cutoff),
        ).fetchall()
        stats[sid]["series"] = [{"dia": r["dia"], "preco": r["preco"]} for r in series]

        alert = conn.execute(
            """SELECT preco, enviado_em FROM alerts_sent
               WHERE search_id = ? ORDER BY enviado_em DESC LIMIT 1""",
            (sid,),
        ).fetchone()
        if alert:
            stats[sid]["last_alert"] = {
                "preco": alert["preco"],
                "enviado_em": alert["enviado_em"],
            }

    conn.close()
    return stats


def refresh_caches():
    fetch_searches.clear()
    fetch_db_stats.clear()


# ============ FORMATTERS ============
def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def fmt_brl(v):
    if v is None:
        return "—"
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_date(iso):
    if not iso:
        return "—"
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return dt.strftime("%d/%m %H:%M")
    except Exception:
        return iso


def time_ago(iso):
    if not iso:
        return "—"
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        delta = datetime.now(timezone.utc) - dt
        h = int(delta.total_seconds() / 3600)
        if h < 1:
            return "agora há pouco"
        if h < 24:
            return f"há {h}h"
        return f"há {h // 24}d"
    except Exception:
        return iso


def classe_pt(code):
    return next((k for k, v in CLASSE_OPTS.items() if v == code), code or "—")


# ============ UI ============
st.title("✈️ Flight Tracker")

if not REPO or not TOKEN:
    st.warning(
        "⚙️ Configuração ausente. Defina **GITHUB_REPO** e **GITHUB_TOKEN** "
        "em *Settings → Secrets* do app no Streamlit Cloud "
        "(ou em `.streamlit/secrets.toml` localmente)."
    )
    st.stop()

st.caption(f"Repo: `{REPO}` · branch: `{BRANCH}`")

tab_cadastro, tab_listagem = st.tabs(["➕ Nova busca", "📋 Buscas cadastradas"])

# ----- ABA: NOVA BUSCA -----
with tab_cadastro:
    iata_codes = airport_options()

    def _index_or_zero(code):
        try:
            return iata_codes.index(code)
        except ValueError:
            return 0

    with st.form("nova_busca", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            origem = st.selectbox(
                "📍 Origem",
                options=iata_codes,
                index=_index_or_zero("GRU"),
                format_func=airport_label,
            )
        with col2:
            destino = st.selectbox(
                "📍 Destino",
                options=iata_codes,
                index=_index_or_zero("LIS"),
                format_func=airport_label,
            )

        st.markdown("##### 📅 Janela de ida")
        ida_range = st.date_input(
            "De – Até",
            value=(date.today() + timedelta(days=60), date.today() + timedelta(days=75)),
            min_value=date.today(),
            key="ida_range",
        )

        st.markdown("##### 📅 Janela de volta")
        volta_range = st.date_input(
            "De – Até",
            value=(date.today() + timedelta(days=80), date.today() + timedelta(days=95)),
            min_value=date.today(),
            key="volta_range",
        )

        col3, col4, col5 = st.columns(3)
        with col3:
            paradas = st.radio("✈️ Paradas", ["Qualquer", "Só voos diretos"])
        with col4:
            pax = st.number_input("👥 Passageiros", min_value=1, max_value=9, value=1, step=1)
        with col5:
            classe_label = st.selectbox("💺 Classe", list(CLASSE_OPTS.keys()))

        preco_alvo = st.number_input(
            "🎯 Preço alvo (opcional, R$)",
            min_value=0, value=0, step=100,
            help="Se o preço cair abaixo deste valor, alerta sempre. 0 = desativado.",
        )

        submitted = st.form_submit_button(
            "💾 Salvar busca", type="primary", use_container_width=True
        )

        if submitted:
            errors = []
            if origem == destino:
                errors.append("Origem e destino devem ser diferentes.")
            if not isinstance(ida_range, tuple) or len(ida_range) != 2:
                errors.append("Janela de ida incompleta (selecione duas datas).")
            if not isinstance(volta_range, tuple) or len(volta_range) != 2:
                errors.append("Janela de volta incompleta (selecione duas datas).")

            if not errors:
                ida_min, ida_max = ida_range
                volta_min, volta_max = volta_range
                if volta_min < ida_min:
                    errors.append("Volta não pode ser antes da ida.")

            if errors:
                for e in errors:
                    st.error(e)
            else:
                searches = fetch_searches()
                base_id = slugify(f"{origem}-{destino}-{ida_min.strftime('%Y%m')}")
                new_id = base_id
                k = 2
                existing_ids = {s.get("id") for s in searches}
                while new_id in existing_ids:
                    new_id = f"{base_id}-{k}"
                    k += 1

                nova = {
                    "id": new_id,
                    "origem": origem,
                    "destino": destino,
                    "ida_min": ida_min.isoformat(),
                    "ida_max": ida_max.isoformat(),
                    "volta_min": volta_min.isoformat(),
                    "volta_max": volta_max.isoformat(),
                    "pax": int(pax),
                    "classe": CLASSE_OPTS[classe_label],
                    "nao_paradas": paradas == "Só voos diretos",
                    "ativo": True,
                }
                if preco_alvo > 0:
                    nova["preco_alvo"] = float(preco_alvo)

                try:
                    searches.append(nova)
                    write_searches(searches, f"add search {new_id}")
                    refresh_caches()
                    st.success(f"✅ Busca **{new_id}** cadastrada!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Falha ao salvar: {e}")

# ----- ABA: LISTAGEM -----
with tab_listagem:
    if st.button("🔄 Atualizar", use_container_width=False):
        refresh_caches()
        st.rerun()

    searches = fetch_searches()
    stats = fetch_db_stats()

    if not searches:
        st.info("Nenhuma busca cadastrada ainda. Use a aba **Nova busca** pra começar.")
    else:
        ativas = sum(1 for s in searches if s.get("ativo", True))
        pausadas = len(searches) - ativas
        st.markdown(f"**{ativas} ativa(s)** · {pausadas} pausada(s)")

        for idx, s in enumerate(searches):
            sid = s["id"]
            ativo = s.get("ativo", True)
            ss = stats.get(sid, {})
            icon = "✅" if ativo else "⏸️"

            with st.container(border=True):
                colA, colB = st.columns([3, 1])
                with colA:
                    st.markdown(f"### {icon} {s['origem']} → {s['destino']}")
                    st.caption(
                        f"Ida {s.get('ida_min', '—')} – {s.get('ida_max', '—')}  ·  "
                        f"Volta {s.get('volta_min', '—')} – {s.get('volta_max', '—')}"
                    )
                    paradas_lbl = "Direto" if s.get("nao_paradas") else "Qualquer"
                    st.caption(
                        f"{paradas_lbl} · {s.get('pax', 1)} pax · {classe_pt(s.get('classe'))}"
                    )
                    if s.get("preco_alvo"):
                        st.caption(f"🎯 Alvo: {fmt_brl(s['preco_alvo'])}")
                with colB:
                    delta = None
                    if ss.get("preco_atual") is not None and ss.get("avg_p"):
                        pct = (ss["preco_atual"] / ss["avg_p"] - 1) * 100
                        delta = f"{pct:+.1f}% vs média"
                    st.metric(
                        "Preço atual",
                        fmt_brl(ss.get("preco_atual")) if ss.get("preco_atual") is not None else "—",
                        delta,
                        delta_color="inverse",
                    )

                if ss.get("n"):
                    cols = st.columns(4)
                    cols[0].caption(f"Mín: **{fmt_brl(ss.get('min_p'))}**")
                    cols[1].caption(f"Média: **{fmt_brl(ss.get('avg_p'))}**")
                    cols[2].caption(f"n = **{ss['n']}**")
                    cols[3].caption(f"Última: {time_ago(ss.get('last_check'))}")

                    if ss.get("last_alert"):
                        st.caption(
                            f"📨 Último alerta: {fmt_date(ss['last_alert']['enviado_em'])} "
                            f"({fmt_brl(ss['last_alert']['preco'])})"
                        )

                    if ss.get("series"):
                        df = pd.DataFrame(ss["series"])
                        df["dia"] = pd.to_datetime(df["dia"])
                        df = df.set_index("dia")
                        st.line_chart(df, height=140)
                else:
                    st.caption("_Sem histórico ainda — aguarde a próxima execução do workflow._")

                act = st.columns(3)
                if ativo:
                    if act[0].button("⏸️ Pausar", key=f"pause_{idx}", use_container_width=True):
                        for x in searches:
                            if x["id"] == sid:
                                x["ativo"] = False
                        write_searches(searches, f"pause search {sid}")
                        refresh_caches()
                        st.rerun()
                else:
                    if act[0].button("▶️ Retomar", key=f"resume_{idx}", use_container_width=True):
                        for x in searches:
                            if x["id"] == sid:
                                x["ativo"] = True
                        write_searches(searches, f"resume search {sid}")
                        refresh_caches()
                        st.rerun()

                if act[2].button("🗑️ Excluir", key=f"del_{idx}", use_container_width=True):
                    new_list = [x for x in searches if x["id"] != sid]
                    write_searches(new_list, f"delete search {sid}")
                    refresh_caches()
                    st.rerun()
