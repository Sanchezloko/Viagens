from datetime import date, timedelta
import requests
from . import config, db


def _target_months(search):
    """Return future (year, month) tuples covering the departure window ±1 month."""
    today = date.today()
    ida_min = date.fromisoformat(str(search["ida_min"]))
    ida_max = date.fromisoformat(str(search.get("ida_max", search["ida_min"])))

    months = set()
    # Walk from ida_min month to ida_max month
    d = ida_min.replace(day=1)
    end = ida_max.replace(day=1)
    while d <= end:
        months.add((d.year, d.month))
        d = (d + timedelta(days=32)).replace(day=1)

    # Add one month before and after for seasonal context
    first = min(months)
    last = max(months)
    prev = (date(*first, 1) - timedelta(days=1)).replace(day=1)
    months.add((prev.year, prev.month))
    nxt = (date(*last, 1) + timedelta(days=32)).replace(day=1)
    months.add((nxt.year, nxt.month))

    # Only future months (Travelpayouts has no past flight data)
    return sorted(m for m in months if date(*m, 1) >= today.replace(day=1))


def _fetch_month(search, year, month):
    volta_min = search.get("volta_min")
    params = {
        "origin": search["origem"],
        "destination": search["destino"],
        "depart_date": f"{year}-{month:02d}",
        "currency": search.get("moeda", "brl").lower(),
        "token": config.TRAVELPAYOUTS_TOKEN,
        "limit": 30,
    }
    if volta_min:
        volta = date.fromisoformat(str(volta_min))
        params["return_date"] = f"{volta.year}-{volta.month:02d}"

    try:
        r = requests.get(
            "https://api.travelpayouts.com/v1/prices/cheap",
            params=params,
            timeout=15,
        )
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print(f"    ! Travelpayouts {year}-{month:02d}: {e}")
        return []

    if not data.get("success", True) or data.get("error"):
        print(f"    ! Travelpayouts {year}-{month:02d}: {data.get('error', 'sem dados')}")
        return []

    raw = data.get("data", {}) or {}
    # Response can be {origin: {date: info}} or {date: info}
    first_val = next(iter(raw.values()), None)
    if isinstance(first_val, dict) and "price" not in first_val:
        raw = first_val

    results = []
    for day_str, info in raw.items():
        if not isinstance(info, dict):
            continue
        price = info.get("price")
        if not price:
            continue
        departure_at = info.get("departure_at", day_str)
        return_at = info.get("return_at")
        results.append({
            "preco": float(price),
            "moeda": search.get("moeda", "BRL"),
            "cia": info.get("airline"),
            "ida": departure_at[:10] if departure_at else day_str,
            "volta": return_at[:10] if return_at else None,
        })
    return results


def fetch_market_context(search):
    """Append Travelpayouts cross-sectional prices every run.

    Queries prices across the target departure month ±1 on every execution,
    building a longitudinal record of how market prices evolve over time.
    Combined with real-time SerpApi data, this gives the analyzer a richer
    baseline for anomaly detection.
    """
    if not config.TRAVELPAYOUTS_TOKEN:
        return

    sid = search["id"]
    if db.has_travelpayouts_today(sid):
        print(f"  ~ mercado {sid}: Travelpayouts já consultado hoje, pulando")
        return
    print(f"  ~ mercado {sid}: consultando Travelpayouts...")

    months = _target_months(search)
    if not months:
        print("  ! nenhum mês futuro para consultar")
        return

    all_results = []
    for year, month in months:
        results = _fetch_month(search, year, month)
        all_results.extend(results)
        print(f"    {year}-{month:02d}: {len(results)} preços")

    if not all_results:
        print("  ! Travelpayouts não retornou dados — verifique o token")
        return

    for r in all_results:
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
            fonte="travelpayouts",
        )
    print(f"  + {len(all_results)} preços de baseline inseridos")
