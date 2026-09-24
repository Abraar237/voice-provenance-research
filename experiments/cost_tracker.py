"""Spend tracker with hard stop. Every OpenRouter call logs the exact `usage.cost` it returned.
State: results/spend.json. Raises CostCapExceeded once the total crosses HARD_STOP_USD."""

import json
import os
import threading
import time

HARD_STOP_USD = 25.00
STATE = os.path.join(os.path.dirname(__file__), "..", "results", "spend.json")
_lock = threading.Lock()


class CostCapExceeded(RuntimeError):
    pass


def _load():
    if os.path.exists(STATE):
        return json.load(open(STATE))
    return {"total_usd": 0.0, "by_model": {}, "n_calls": 0, "updated": None}


def log_call(model, cost_usd):
    with _lock:
        s = _load()
        s["total_usd"] = round(s["total_usd"] + float(cost_usd), 6)
        s["by_model"][model] = round(s["by_model"].get(model, 0.0) + float(cost_usd), 6)
        s["n_calls"] += 1
        s["updated"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        os.makedirs(os.path.dirname(STATE), exist_ok=True)
        json.dump(s, open(STATE, "w"), indent=1)
        if s["total_usd"] >= HARD_STOP_USD:
            raise CostCapExceeded(f"spend {s['total_usd']:.2f} >= {HARD_STOP_USD}")
        return s["total_usd"]


def total():
    return _load()["total_usd"]
