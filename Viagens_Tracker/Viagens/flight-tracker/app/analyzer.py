import statistics
from datetime import datetime, timedelta, timezone
from . import config, db


def _percentile(values, pct):
    """Percentil simples sem numpy."""
    if not values:
        return None
    s = sorted(values)
    k = (len(s) - 1) * (pct / 100)
    f, c = int(k), min(int(k) + 1, len(s) - 1)
    if f == c:
        return s[f]
    return s[f] + (s[c] - s[f]) * (k - f)


def evaluate(search_id, preco_atual, preco_alvo=None):
    """
    Decide se deve disparar alerta.
    Retorna dict com decisão + estatísticas (úteis pra mensagem).
    """
    historico = db.recent_prices(search_id, days=config.HISTORY_DAYS)
    n = len(historico)

    stats = {
        "n_amostras": n,
        "preco_atual": preco_atual,
        "media": None,
        "stddev": None,
        "p25": None,
        "p_alert": None,
        "z_score": None,
        "deve_alertar": False,
        "motivo": "",
    }

    # Regra 1: preço alvo bateu — sempre alerta
    if preco_alvo and preco_atual <= preco_alvo:
        stats["deve_alertar"] = True
        stats["motivo"] = f"preço ≤ alvo (R$ {preco_alvo:.2f})"
        return _check_cooldown(search_id, stats)

    # Regra 2: bootstrap — menos de 2 semanas de histórico, usa preço fixo
    if n < config.BOOTSTRAP_SAMPLES:
        if preco_atual <= config.BOOTSTRAP_TARGET:
            stats["deve_alertar"] = True
            stats["motivo"] = (
                f"bootstrap: preço ≤ R$ {config.BOOTSTRAP_TARGET:.0f} "
                f"({n}/{config.BOOTSTRAP_SAMPLES} amostras)"
            )
            return _check_cooldown(search_id, stats)
        stats["motivo"] = (
            f"bootstrap: acima de R$ {config.BOOTSTRAP_TARGET:.0f} "
            f"({n}/{config.BOOTSTRAP_SAMPLES} amostras)"
        )
        return stats

    # Sem histórico suficiente para estatística → cold start
    if n < config.MIN_SAMPLES_FOR_ALERT:
        stats["motivo"] = f"cold start ({n}/{config.MIN_SAMPLES_FOR_ALERT} amostras)"
        return stats

    media = statistics.mean(historico)
    stddev = statistics.pstdev(historico) if n > 1 else 0.0
    p_alert = _percentile(historico, config.ALERT_PERCENTILE)
    p25 = _percentile(historico, 25)
    z = (preco_atual - media) / stddev if stddev > 0 else 0.0

    stats.update({
        "media": media,
        "stddev": stddev,
        "p25": p25,
        "p_alert": p_alert,
        "z_score": z,
    })

    # Regra 2: bottom-percentile + z-score baixo
    abaixo_percentil = preco_atual <= p_alert
    z_baixo = z <= config.ALERT_ZSCORE
    if abaixo_percentil and z_baixo:
        stats["deve_alertar"] = True
        stats["motivo"] = (
            f"abaixo do P{int(config.ALERT_PERCENTILE)} "
            f"(R$ {p_alert:.2f}) e z-score {z:.2f}"
        )
        return _check_cooldown(search_id, stats)

    stats["motivo"] = (
        f"acima do gatilho (P{int(config.ALERT_PERCENTILE)}=R${p_alert:.2f}, "
        f"z={z:.2f})"
    )
    return stats


def _check_cooldown(search_id, stats):
    """Aplica cooldown — não alerta de novo dentro de COOLDOWN_HOURS."""
    last = db.last_alert(search_id)
    if last:
        last_dt = datetime.fromisoformat(last["enviado_em"])
        delta = datetime.now(timezone.utc) - last_dt
        if delta < timedelta(hours=config.COOLDOWN_HOURS):
            stats["deve_alertar"] = False
            stats["motivo"] += f" (em cooldown, último alerta há {delta})"
    return stats
