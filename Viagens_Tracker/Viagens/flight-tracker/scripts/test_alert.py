"""
Seeda dados sintéticos no SQLite e roda o pipeline de avaliação + notificação,
sem precisar esperar coleta real do Amadeus.

O que faz:
  1. Cria uma busca fake "TESTE-LOCAL" e apaga histórico anterior dela
  2. Insere 30 preços sintéticos (média 3300, stddev 200) espalhados em 30 dias
  3. Avalia 3 cenários (preço normal / levemente baixo / bem baixo)
  4. Dispara notificação real via CallMeBot pro cenário "bem baixo"

Uso (a partir de flight-tracker/):
    python -m scripts.test_alert
"""
import random
import sys
from datetime import datetime, timedelta, timezone

from app import analyzer, config, db, notifier

SEARCH_ID = "TESTE-LOCAL"


def reset():
    db.init()
    with db.conn() as c:
        c.execute("DELETE FROM price_history WHERE search_id = ?", (SEARCH_ID,))
        c.execute("DELETE FROM alerts_sent WHERE search_id = ?", (SEARCH_ID,))


def seed(n=30, mean=3300, stddev=200):
    random.seed(42)
    now = datetime.now(timezone.utc)
    with db.conn() as c:
        for i in range(n):
            preco = max(2500, random.gauss(mean, stddev))
            ts = now - timedelta(days=30) + timedelta(days=i)
            c.execute(
                """INSERT INTO price_history
                     (search_id, origem, destino, data_ida, data_volta,
                      pax, classe, preco, moeda, cia, link, coletado_em)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    SEARCH_ID, "GRU", "LIS",
                    "2026-07-15", "2026-07-30",
                    1, "ECONOMY",
                    round(preco, 2), "BRL", "TP", None,
                    ts.isoformat(),
                ),
            )


def avaliar(preco):
    stats = analyzer.evaluate(SEARCH_ID, preco)
    print(f"  preço atual:   R$ {preco:,.2f}")
    if stats.get("p_alert") is not None:
        print(f"  P{int(config.ALERT_PERCENTILE)} histórico: R$ {stats['p_alert']:,.2f}")
    if stats.get("media") is not None:
        print(f"  média:         R$ {stats['media']:,.2f}  "
              f"(stddev R$ {stats['stddev']:,.2f}, n={stats['n_amostras']})")
    if stats.get("z_score") is not None:
        print(f"  z-score:       {stats['z_score']:+.2f}")
    print(f"  → alertar?     {'🚨 SIM' if stats['deve_alertar'] else 'não'}")
    print(f"  motivo:        {stats['motivo']}")
    return stats


def main():
    print(f"=== Teste do pipeline de alerta ({SEARCH_ID}) ===\n")
    reset()
    seed()
    print("✓ 30 preços sintéticos inseridos (média R$ 3.300, stddev R$ 200)\n")

    cenarios = [
        ("Preço normal",           3350.00),
        ("Levemente baixo",        3050.00),
        ("Bem baixo",              2700.00),
    ]

    resultados = []
    for label, preco in cenarios:
        print(f"--- {label} ---")
        stats = avaliar(preco)
        resultados.append((label, preco, stats))
        print()

    # Pega o último cenário e dispara notificação real
    label, preco, stats = resultados[-1]
    print(f"=== Disparando notificação WhatsApp ({label}) ===")

    if not (config.CALLMEBOT_PHONE and config.CALLMEBOT_APIKEY):
        print("! CallMeBot não configurado no .env — pulando envio")
        return 0

    fake_search = {"id": SEARCH_ID, "origem": "GRU", "destino": "LIS"}
    fake_oferta = {
        "preco": preco, "moeda": "BRL", "cia": "TP",
        "ida": "2026-07-15", "volta": "2026-07-30",
    }
    # Force-override pra contornar cooldown se já houver alerta recente
    stats["deve_alertar"] = True

    ok, payload = notifier.send(fake_search, fake_oferta, stats)
    if ok:
        print("✓ Notificação enviada — cheque seu WhatsApp em até 30s.")
        db.insert_alert(SEARCH_ID, preco, payload)
    else:
        print("✗ Falha no envio (veja logs acima).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
