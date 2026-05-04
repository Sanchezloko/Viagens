import requests
from . import config


def _format_message(search, oferta, stats):
    rota = f"{search['origem']}→{search['destino']}"
    datas = oferta["ida"]
    if oferta.get("volta"):
        datas += f" / {oferta['volta']}"
    cia = oferta.get("cia") or "—"

    linhas = [
        f"Rota: {rota}",
        f"Datas: {datas}",
        f"Cia: {cia}",
        f"Motivo: {stats['motivo']}",
    ]
    if stats.get("media"):
        linhas.append(f"Média histórica: R$ {stats['media']:.2f} (n={stats['n_amostras']})")
    return "\n".join(linhas)


def send(search, oferta, stats):
    if not config.NTFY_TOPIC:
        print("  ! ntfy não configurado, pulando notificação")
        return False, ""

    preco = f"R$ {oferta['preco']:.2f}"
    rota = f"{search['origem']}→{search['destino']}"
    msg = _format_message(search, oferta, stats)

    try:
        r = requests.post(
            f"https://ntfy.sh/{config.NTFY_TOPIC}",
            data=msg.encode("utf-8"),
            headers={
                "Title": f"Oferta {rota} - {preco}".encode("utf-8"),
                "Priority": "high",
                "Tags": "airplane,money_with_wings",
            },
            timeout=15,
        )
        if r.status_code == 200:
            return True, msg
        print(f"  ! ntfy status={r.status_code} body={r.text[:200]}")
    except requests.RequestException as e:
        print(f"  ! ntfy exception: {e}")

    return False, msg
