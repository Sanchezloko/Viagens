from datetime import date, timedelta
import requests
from . import config

TRAVEL_CLASS_MAP = {
    "ECONOMY": 1,
    "PREMIUM_ECONOMY": 2,
    "BUSINESS": 3,
    "FIRST": 4,
}


def _to_str(d):
    return d.isoformat() if hasattr(d, "isoformat") else str(d)


def _date_range(d_min, d_max, step_days=3):
    start = date.fromisoformat(_to_str(d_min))
    end = date.fromisoformat(_to_str(d_max))
    if start > end:
        return []
    out = []
    cur = start
    while cur <= end:
        out.append(cur.isoformat())
        cur += timedelta(days=step_days)
    if out[-1] != end.isoformat():
        out.append(end.isoformat())
    return out


def _search_one(search, ida, volta):
    params = {
        "engine": "google_flights",
        "departure_id": search["origem"],
        "arrival_id": search["destino"],
        "outbound_date": ida,
        "currency": search.get("moeda", "BRL"),
        "hl": "pt",
        "gl": "br",
        "adults": search.get("pax", 1),
        "api_key": config.SERPAPI_KEY,
    }
    if volta:
        params["return_date"] = volta
        params["type"] = 1  # round trip
    else:
        params["type"] = 2  # one way

    classe = search.get("classe", "ECONOMY")
    params["travel_class"] = TRAVEL_CLASS_MAP.get(classe, 1)

    if search.get("nao_paradas"):
        params["stops"] = 1  # 1 = nonstop only

    try:
        r = requests.get("https://serpapi.com/search.json", params=params, timeout=20)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print(f"  ! SerpApi error em {ida}->{volta}: {e}")
        return None

    if data.get("error"):
        print(f"  ! SerpApi error em {ida}->{volta}: {data['error']}")
        return None

    flights = (data.get("best_flights") or []) + (data.get("other_flights") or [])
    if not flights:
        return None

    cheapest = min(flights, key=lambda f: f.get("price", float("inf")))
    price = cheapest.get("price")
    if not price:
        return None

    legs = cheapest.get("flights", [])
    cia = legs[0].get("airline") if legs else None

    return {
        "preco": float(price),
        "moeda": search.get("moeda", "BRL"),
        "cia": cia,
        "ida": ida,
        "volta": volta,
    }


def collect(search):
    idas = _date_range(search["ida_min"], search["ida_max"],
                       step_days=search.get("step_dias", 3))

    duracao_min = search.get("duracao_min_dias")
    duracao_max = search.get("duracao_max_dias")
    volta_min = _to_str(search["volta_min"]) if search.get("volta_min") else None
    volta_max = _to_str(search["volta_max"]) if search.get("volta_max") else None

    pares = []
    for ida in idas:
        ida_d = date.fromisoformat(ida)
        if duracao_min and duracao_max:
            dur = (duracao_min + duracao_max) // 2
            volta = (ida_d + timedelta(days=dur)).isoformat()
            if volta_max and volta > volta_max:
                volta = volta_max
            if volta_min and volta < volta_min:
                volta = volta_min
            pares.append((ida, volta))
        elif volta_min and volta_max:
            voltas = _date_range(volta_min, volta_max,
                                 step_days=search.get("step_dias", 3))
            for v in voltas:
                if v >= ida:
                    pares.append((ida, v))
        else:
            pares.append((ida, None))

    max_consultas = search.get("max_consultas_por_run", 8)
    pares = pares[:max_consultas]

    resultados = []
    for ida, volta in pares:
        r = _search_one(search, ida, volta)
        if r:
            resultados.append(r)

    if not resultados:
        return None, []

    melhor = min(resultados, key=lambda x: x["preco"])
    return melhor, resultados
