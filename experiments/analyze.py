#!/usr/bin/env python3
"""Single analysis pass: results/raw/*.jsonl (+ results/o5_judge.jsonl) -> results/analysis.json.
Every number in the paper traces to this file's output. Seeded; byte-identical on re-run.

Usage: python3 analyze.py
"""

import glob
import json
import os
import re

import jiwer
import numpy as np
import pandas as pd

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RAW = os.path.join(ROOT, "results", "raw")
RNG = np.random.default_rng(42)
N_BOOT = 10_000
N_PERM = 20_000
ARMS = ["real", "clone", "resynth", "stock"]
CONTRASTS = [("clone", "real"), ("resynth", "real"), ("stock", "real"), ("clone", "resynth")]
SYN = {"real": 0, "resynth": 0, "clone": 1, "stock": 1, "clone_b": 1}
ITEMS = {it["item"]: it for it in json.load(open(os.path.join(ROOT, "corpus", "items.json")))["items"]}


# ---------- parsing ----------
def norm_text(s):
    s = s.lower().replace("-", " ")
    s = re.sub(r"[^a-z' ]", " ", s)
    return " ".join(s.split())


def parse(rec):
    o, t = rec["outcome"], (rec["text"] or "").strip()
    if o == "O1":
        gold = norm_text(ITEMS[rec["item"]]["text"])
        hyp = norm_text(t)
        return {"wer": jiwer.wer(gold, hyp) if gold else np.nan}
    if o == "O2":
        m = re.search(r"\b(10|[1-9])\b", t)
        return {"grade": int(m.group(1)) if m else np.nan}
    if o == "O3":
        m = re.search(r"\b([ABCD])\b", t.upper())
        return {"mcq_correct": float(m.group(1) == rec.get("correct_letter")) if m else np.nan,
                "mcq_answered": float(bool(m))}
    if o == "O4":
        u = t.upper()
        lab = "SYNTHETIC" if "SYNTHETIC" in u else ("REAL" if "REAL" in u else None)
        return {"says_synthetic": (1.0 if lab == "SYNTHETIC" else 0.0) if lab else np.nan,
                "probe_correct": (float((lab == "SYNTHETIC") == bool(SYN[rec["arm"]]))) if lab else np.nan}
    if o == "O5":
        return {"reply_words": len(t.split()), "reply_empty": float(len(t.split()) == 0)}
    return {}


def load():
    rows = []
    for f in sorted(glob.glob(os.path.join(RAW, "*.jsonl"))):
        for line in open(f):
            r = json.loads(line)
            r.update(parse(r))
            rows.append(r)
    df = pd.DataFrame(rows)
    jp = os.path.join(ROOT, "results", "o5_judge.jsonl")
    if os.path.exists(jp):
        j = pd.DataFrame([json.loads(l) for l in open(jp)])
        df = df.merge(j[["key", "refusal", "voice_remark", "verify"]], on="key", how="left")
    return df


# ---------- statistics ----------
def boot_ci(vals, clusters, stat=np.mean):
    vals, clusters = np.asarray(vals, float), np.asarray(clusters)
    ok = ~np.isnan(vals)
    vals, clusters = vals[ok], clusters[ok]
    if len(vals) == 0:
        return [np.nan, np.nan]
    uc = np.unique(clusters)
    idx = {c: np.where(clusters == c)[0] for c in uc}
    out = np.empty(N_BOOT)
    for b in range(N_BOOT):
        pick = RNG.choice(uc, len(uc), replace=True)
        out[b] = stat(np.concatenate([vals[idx[c]] for c in pick]))
    return [float(np.nanpercentile(out, 2.5)), float(np.nanpercentile(out, 97.5))]


def perm_signflip(diffs, clusters):
    """Two-sided sign-flip permutation on paired diffs, flipping whole speaker clusters."""
    d, c = np.asarray(diffs, float), np.asarray(clusters)
    ok = ~np.isnan(d)
    d, c = d[ok], c[ok]
    if len(d) == 0:
        return np.nan
    uc = np.unique(c)
    cid = np.searchsorted(uc, c)
    obs = abs(d.mean())
    cnt = 0
    for _ in range(N_PERM):
        s = RNG.choice([-1.0, 1.0], len(uc))[cid]
        if abs((d * s).mean()) >= obs - 1e-12:
            cnt += 1
    return max(cnt, 1) / N_PERM


def dz(diffs):
    d = np.asarray(diffs, float)
    d = d[~np.isnan(d)]
    return float(d.mean() / d.std(ddof=1)) if len(d) > 1 and d.std(ddof=1) > 0 else np.nan


def auc_paired(a, b):
    """P(a > b) + 0.5 P(a == b) over paired items: probability the measure ranks arm a above arm b."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = ~np.isnan(a) & ~np.isnan(b)
    a, b = a[ok], b[ok]
    if len(a) == 0:
        return np.nan
    return float(((a > b).sum() + 0.5 * (a == b).sum()) / len(a))


def bh(pvals):
    keys = [k for k, v in pvals.items() if v is not None and not np.isnan(v)]
    p = np.array([pvals[k] for k in keys])
    n = len(p)
    order = np.argsort(p)
    q = np.empty(n)
    prev = 1.0
    for rank in range(n - 1, -1, -1):
        i = order[rank]
        prev = min(prev, p[i] * n / (rank + 1))
        q[i] = prev
    return {k: float(q[i]) for i, k in enumerate(keys)}


# ---------- main ----------
def main():
    df = load()
    df = df[df.rep == 0].copy() if "rep" in df else df
    out = {"generated": "analyze.py", "n_records": int(len(df))}
    tests = {}
    measures = {"O1": "wer", "O2": "grade", "O3": "mcq_correct", "O4": "says_synthetic",
                "O5": "reply_words"}
    if "refusal" in df:
        measures["O5_refusal"] = "refusal"
        measures["O5_voice"] = "voice_remark"
        measures["O5_verify"] = "verify"
    models = sorted(df.model.unique())
    out["models"] = {}
    for m in models:
        dm = df[df.model == m]
        res = {"n_items": int(dm.item.nunique()), "arms": {}, "contrasts": {}, "probe": {}, "d1": {}}
        # per-arm means
        for arm in ARMS + ["clone_b"]:
            da = dm[dm.arm == arm]
            if da.empty:
                continue
            res["arms"][arm] = {}
            for o, col in measures.items():
                sub = da[da.outcome == o.split("_")[0]]
                if sub.empty or col not in sub:
                    continue
                v = sub[col].astype(float)
                res["arms"][arm][col] = {"mean": float(np.nanmean(v)), "n": int(v.notna().sum()),
                                         "ci": boot_ci(v, sub.spk)}
        # paired contrasts
        for o, col in measures.items():
            sub = dm[dm.outcome == o.split("_")[0]]
            if sub.empty or col not in sub:
                continue
            piv = sub.pivot_table(index="item", columns="arm", values=col, aggfunc="first")
            for a, b in CONTRASTS:
                if a not in piv or b not in piv:
                    continue
                d = (piv[a] - piv[b])
                spk = [ITEMS[i]["spk"] for i in piv.index]
                key = f"{m}:{col}:{a}-{b}"
                p = perm_signflip(d.values, spk)
                res["contrasts"][f"{col}:{a}-{b}"] = {
                    "mean": float(np.nanmean(d)), "ci": boot_ci(d.values, spk), "p": p,
                    "dz": dz(d.values), "n_pairs": int(d.notna().sum()),
                    "auc_a_over_b": auc_paired(piv[a], piv[b])}
                tests[key] = p
        # D2: share of clone-real delta explained by resynth-real (grade and mcq)
        for col in ("grade", "mcq_correct", "wer"):
            c1 = res["contrasts"].get(f"{col}:clone-real")
            c2 = res["contrasts"].get(f"{col}:resynth-real")
            if c1 and c2 and abs(c1["mean"]) > 1e-9:
                sub = dm[dm.outcome == {"grade": "O2", "mcq_correct": "O3", "wer": "O1"}[col]]
                piv = sub.pivot_table(index="item", columns="arm", values=col, aggfunc="first")
                spk = np.array([ITEMS[i]["spk"] for i in piv.index])
                dc, dr = (piv["clone"] - piv["real"]).values, (piv["resynth"] - piv["real"]).values
                ratios = []
                uc = np.unique(spk)
                for _ in range(N_BOOT):
                    pick = RNG.choice(uc, len(uc), replace=True)
                    ix = np.concatenate([np.where(spk == c)[0] for c in pick])
                    num, den = np.nanmean(dr[ix]), np.nanmean(dc[ix])
                    ratios.append(num / den if abs(den) > 1e-9 else np.nan)
                res["d2_" + col] = {"ratio": float(np.nanmean(dr) / np.nanmean(dc)),
                                    "ci": [float(np.nanpercentile(ratios, 2.5)), float(np.nanpercentile(ratios, 97.5))]}
        # probe (D4)
        p4 = dm[dm.outcome == "O4"]
        if not p4.empty:
            for arm in ARMS + ["clone_b"]:
                s = p4[p4.arm == arm]["says_synthetic"].astype(float)
                if s.notna().sum():
                    res["probe"][arm] = {"share_synthetic": float(np.nanmean(s)), "n": int(s.notna().sum())}
            piv = p4.pivot_table(index="item", columns="arm", values="says_synthetic", aggfunc="first")
            if "real" in piv and "clone" in piv:
                tpr = np.nanmean(piv["clone"])            # says synthetic when synthetic
                tnr = 1 - np.nanmean(piv["real"])         # says real when real
                res["probe"]["balanced_acc_real_vs_clone"] = float((tpr + tnr) / 2)
                # explicit discrimination AUC on paired items: P(prob_syn(clone) > prob_syn(real))
                res["probe"]["explicit_auc_real_vs_clone"] = auc_paired(piv["clone"], piv["real"])
                acc = p4[p4.arm.isin(["real", "clone"])]["probe_correct"].astype(float)
                res["probe"]["acc_real_clone"] = {"mean": float(np.nanmean(acc)),
                                                  "ci": boot_ci(acc, p4[p4.arm.isin(["real", "clone"])].spk)}
            if "real" in piv and "stock" in piv:
                res["probe"]["balanced_acc_real_vs_stock"] = float(
                    (np.nanmean(piv["stock"]) + 1 - np.nanmean(piv["real"])) / 2)
            if "real" in piv and "resynth" in piv:
                res["probe"]["share_synthetic_resynth_minus_real"] = float(
                    np.nanmean(piv["resynth"]) - np.nanmean(piv["real"]))
        # D1: implicit discrimination (grade / mcq ranks real above clone) vs explicit
        for col, o in (("grade", "O2"), ("mcq_correct", "O3")):
            sub = dm[dm.outcome == o]
            p4s = dm[dm.outcome == "O4"]
            if sub.empty or p4s.empty:
                continue
            piv = sub.pivot_table(index="item", columns="arm", values=col, aggfunc="first")
            pv4 = p4s.pivot_table(index="item", columns="arm", values="says_synthetic", aggfunc="first")
            common = piv.index.intersection(pv4.index)
            if "real" not in piv or "clone" not in piv or "real" not in pv4 or "clone" not in pv4:
                continue
            spk = np.array([ITEMS[i]["spk"] for i in common])
            gr, gc = piv.loc[common, "real"].values, piv.loc[common, "clone"].values
            sr, sc = pv4.loc[common, "real"].values, pv4.loc[common, "clone"].values
            imp = auc_paired(gr, gc)               # grade ranks real above clone
            imp_dir = imp if imp >= 0.5 else 1 - imp  # direction-free discriminability
            exp = auc_paired(sc, sr)               # probe says synthetic more for clone
            diffs = []
            uc = np.unique(spk)
            for _ in range(N_BOOT):
                pick = RNG.choice(uc, len(uc), replace=True)
                ix = np.concatenate([np.where(spk == c)[0] for c in pick])
                i_ = auc_paired(gr[ix], gc[ix])
                i_ = i_ if i_ >= 0.5 else 1 - i_
                diffs.append(i_ - auc_paired(sc[ix], sr[ix]))
            res["d1"][col] = {"implicit_auc": imp, "implicit_auc_dirfree": imp_dir, "explicit_auc": exp,
                              "implicit_minus_explicit": float(imp_dir - exp),
                              "ci": [float(np.nanpercentile(diffs, 2.5)), float(np.nanpercentile(diffs, 97.5))],
                              "n": int(len(common))}
        out["models"][m] = res

    # D3: family x provenance interaction: difference of clone-real grade deltas between model pairs
    out["d3_pairs"] = {}
    g = df[df.outcome == "O2"]
    for i, m1 in enumerate(models):
        for m2 in models[i + 1:]:
            p1 = g[g.model == m1].pivot_table(index="item", columns="arm", values="grade", aggfunc="first")
            p2 = g[g.model == m2].pivot_table(index="item", columns="arm", values="grade", aggfunc="first")
            if not {"real", "clone"} <= set(p1.columns) or not {"real", "clone"} <= set(p2.columns):
                continue
            common = p1.index.intersection(p2.index)
            d = ((p1.loc[common, "clone"] - p1.loc[common, "real"]) -
                 (p2.loc[common, "clone"] - p2.loc[common, "real"]))
            spk = [ITEMS[i]["spk"] for i in common]
            p = perm_signflip(d.values, spk)
            out["d3_pairs"][f"{m1} vs {m2}"] = {"diff_of_deltas": float(np.nanmean(d)), "ci": boot_ci(d.values, spk),
                                                "p": p, "n": int(d.notna().sum())}
            tests[f"d3:{m1}|{m2}"] = p

    # noise floor and stability batteries
    full = load()
    nf = full[full.rep > 0] if "rep" in full else full.iloc[0:0]
    out["noise_floor"] = {}
    for m in nf.model.unique():
        for o, col in (("O2", "grade"), ("O4", "says_synthetic")):
            s = nf[(nf.model == m) & (nf.outcome == o)]
            if s.empty:
                continue
            cells = s.groupby(["item", "arm"])[col].agg(["nunique", "std", "count"])
            cells = cells[cells["count"] >= 2]
            out["noise_floor"][f"{m}:{col}"] = {"cells": int(len(cells)),
                                               "frac_cells_inconsistent": float((cells["nunique"] > 1).mean()),
                                               "mean_within_sd": float(cells["std"].fillna(0).mean())}
    st = df[df.arm.isin(["clone", "clone_b"])]
    out["stability"] = {}
    for m in st.model.unique():
        for o, col in (("O2", "grade"), ("O4", "says_synthetic")):
            piv = st[(st.model == m) & (st.outcome == o)].pivot_table(index="item", columns="arm", values=col, aggfunc="first")
            if "clone_b" in piv and "clone" in piv:
                d = (piv["clone_b"] - piv["clone"]).dropna()
                out["stability"][f"{m}:{col}"] = {"mean_abs_clone_to_clone": float(d.abs().mean()),
                                                  "mean_signed": float(d.mean()), "n": int(len(d))}

    # BH over the full reported family
    q = bh(tests)
    out["tests"] = {k: {"p": float(v), "q_bh": q.get(k), "bh_survives_05": bool(q.get(k, 1) <= 0.05)} for k, v in tests.items()}
    out["bh"] = {"n_tests": len(tests), "n_survive": int(sum(1 for k in q if q[k] <= 0.05))}
    spend = os.path.join(ROOT, "results", "spend.json")
    out["spend"] = json.load(open(spend)) if os.path.exists(spend) else None
    json.dump(out, open(os.path.join(ROOT, "results", "analysis.json"), "w"), indent=1, default=float)
    print(json.dumps({m: {k: v for k, v in out["models"][m]["contrasts"].items() if k.startswith("grade:") or k.startswith("mcq")} for m in models}, indent=1)[:3000])
    print("BH", out["bh"])


if __name__ == "__main__":
    main()
