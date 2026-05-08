import sys
import yaml
from . import config, db, collector, analyzer, notifier, bootstrapper


def load_searches():
    if not config.SEARCHES_PATH.exists():
        print(f"! {config.SEARCHES_PATH} não existe")
        return []
    with open(config.SEARCHES_PATH, encoding="utf-8") as f:
        data = yaml.safe_load(f) or []
    return [s for s in data if s.get("ativo", True)]


def process_search(search):
    sid = search["id"]
    print(f"\n=== {sid}: {search['origem']}→{search['destino']} ===")

    melhor, todos = collector.collect(search)
    if not melhor:
        print("  - nenhum resultado")
        return

    # Grava todos os preços coletados (mais dados = melhor análise)
    for r in todos:
        db.insert_price(
            search_id=sid,
            origem=search["origem"],
            destino=search["destino"],
            data_ida=r["ida"],
            data_volta=r.get("volta"),
            pax=search.get("pax", 1),
            classe=search.get("classe", "ECONOMY"),
            preco=r["preco"],
            moeda=r["moeda"],
            cia=r.get("cia"),
            link=None,
            fonte="serpapi",
        )
    print(f"  + {len(todos)} preços coletados, melhor R$ {melhor['preco']:.2f}")

    stats = analyzer.evaluate(
        search_id=sid,
        preco_atual=melhor["preco"],
        preco_alvo=search.get("preco_alvo"),
    )
    print(f"  ~ análise: {stats['motivo']}")

    if stats["deve_alertar"]:
        ok, payload = notifier.send(search, melhor, stats)
        if ok:
            db.insert_alert(sid, melhor["preco"], payload)
            print("  ✓ alerta enviado e gravado")
        else:
            print("  ✗ falha ao enviar alerta")


def main():
    db.init()
    db.prune_old_history()

    searches = load_searches()
    if not searches:
        print("Nenhuma busca ativa em data/searches.yaml")
        return 0

    print(f"Processando {len(searches)} busca(s)...")
    for s in searches:
        try:
            bootstrapper.fetch_market_context(s)
            process_search(s)
        except Exception as e:
            print(f"! erro em {s.get('id', '?')}: {e}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
