#!/usr/bin/env python3
"""Build figures 2-4 from results/analysis.json only. Each figure prints the numbers it drew."""

import json
import pathlib
import sys

import matplotlib.pyplot as plt
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import style as S  # noqa: E402

S.apply()
ROOT = HERE.parent
A = json.load(open(ROOT / "results" / "analysis.json"))
OUT = ROOT / "paper" / "iclr" / "assets"
OUT.mkdir(parents=True, exist_ok=True)
DOCS = ROOT / "docs" / "assets"
DOCS.mkdir(parents=True, exist_ok=True)

LABEL = {"google/gemini-3.6-flash": "Gemini 3.6 Flash", "google/gemini-3.1-pro-preview": "Gemini 3.1 Pro",
         "mistralai/Voxtral-Mini-3B-2507": "Voxtral-Mini-3B", "Qwen/Qwen2.5-Omni-3B": "Qwen2.5-Omni-3B"}
ARMS = ["real", "resynth", "clone", "stock"]
ARM_LABEL = {"real": "REAL", "resynth": "RESYNTH", "clone": "CLONE", "stock": "STOCK"}
ARM_COL = {"real": S.SLATE, "resynth": S.SHELF, "clone": S.HOT, "stock": "#7a6f9b"}
MODELS = [m for m in LABEL if m in A["models"]]


def save(fig, name):
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(DOCS / f"{name}.png", bbox_inches="tight", dpi=200)
    plt.close(fig)
    print("wrote", name)


def fig2_grade():
    """Reading grade by provenance arm, per family, plus paired deltas vs REAL."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.9), gridspec_kw={"width_ratios": [1.2, 1]})
    ax = axes[0]
    w = 0.19
    drew = {}
    for i, m in enumerate(MODELS):
        arms = A["models"][m]["arms"]
        for j, arm in enumerate(ARMS):
            if arm not in arms or "grade" not in arms[arm]:
                continue
            v = arms[arm]["grade"]
            ax.bar(i + (j - 1.5) * w, v["mean"], w, color=ARM_COL[arm], label=ARM_LABEL[arm] if i == 0 else None)
            ax.errorbar(i + (j - 1.5) * w, v["mean"], yerr=[[v["mean"] - v["ci"][0]], [v["ci"][1] - v["mean"]]],
                        color="black", capsize=2, lw=0.8)
            drew[(m, arm)] = round(v["mean"], 2)
    ax.set_xticks(range(len(MODELS)))
    ax.set_xticklabels([LABEL[m] for m in MODELS], fontsize=9)
    ax.set_ylabel("reading grade (1–10)")
    lo = min(drew.values()) - 1.2
    ax.set_ylim(max(1, lo), 10.3)
    ax.legend(frameon=False, ncol=4, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, 1.14))
    S.eyebrow(ax, "SAME SPEAKER, SAME WORDS: GRADE BY PROVENANCE", y=1.18)
    S.clean(ax)
    ax = axes[1]
    ys = []
    for i, m in enumerate(MODELS):
        c = A["models"][m]["contrasts"]
        for j, (k, lab, col) in enumerate([("grade:clone-real", "CLONE − REAL", S.HOT),
                                           ("grade:resynth-real", "RESYNTH − REAL", S.SHELF),
                                           ("grade:stock-real", "STOCK − REAL", "#7a6f9b")]):
            if k not in c:
                continue
            v = c[k]
            y = i * 4 + j
            ys.append(y)
            ax.errorbar(v["mean"], y, xerr=[[v["mean"] - v["ci"][0]], [v["ci"][1] - v["mean"]]], fmt="o",
                        color=col, capsize=3, ms=5)
            star = "*" if A["tests"].get(f"{m}:{k}", {}).get("bh_survives_05") else ""
            ax.text(v["ci"][1] + 0.03, y, f"{v['mean']:+.2f}{star}", va="center", fontsize=8)
            drew[(m, k)] = round(v["mean"], 3)
    ax.axvline(0, color="black", lw=0.8)
    ax.set_yticks([i * 4 + 1 for i in range(len(MODELS))])
    ax.set_yticklabels([LABEL[m] for m in MODELS], fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("paired difference in grade (points); * survives BH")
    S.eyebrow(ax, "PAIRED DELTAS VS THE REAL RECORDING", y=1.18)
    S.clean(ax)
    fig.tight_layout()
    save(fig, "fig2_grade")
    print("fig2:", json.dumps({f"{k[0]}|{k[1]}": v for k, v in drew.items()}))


def fig3_probe():
    """Explicit probe: share of clips called SYNTHETIC per arm, and implicit vs explicit discriminability."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.9))
    ax = axes[0]
    w = 0.19
    drew = {}
    for i, m in enumerate(MODELS):
        pr = A["models"][m]["probe"]
        for j, arm in enumerate(ARMS):
            if arm not in pr:
                continue
            v = pr[arm]["share_synthetic"]
            ax.bar(i + (j - 1.5) * w, v, w, color=ARM_COL[arm], label=ARM_LABEL[arm] if i == 0 else None)
            drew[(m, arm)] = round(v, 3)
    ax.axhline(0.5, color="black", lw=0.6, ls="--")
    ax.set_xticks(range(len(MODELS)))
    ax.set_xticklabels([LABEL[m] for m in MODELS], fontsize=9)
    ax.set_ylabel('share of clips called "SYNTHETIC"')
    ax.set_ylim(0, 1.05)
    ax.legend(frameon=False, ncol=4, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, 1.14))
    S.eyebrow(ax, "THE EXPLICIT PROBE: WHAT THE MODEL SAYS", y=1.18)
    S.clean(ax)
    ax = axes[1]
    for i, m in enumerate(MODELS):
        d1 = A["models"][m]["d1"].get("grade")
        if not d1:
            continue
        ax.bar(i - 0.17, d1["implicit_auc_dirfree"] - 0.5, 0.32, color=S.HOT, label="implicit (grade separates REAL/CLONE)" if i == 0 else None)
        ax.bar(i + 0.17, d1["explicit_auc"] - 0.5, 0.32, color=S.SLATE, label="explicit (probe separates REAL/CLONE)" if i == 0 else None)
        drew[(m, "implicit")] = round(d1["implicit_auc_dirfree"], 3)
        drew[(m, "explicit")] = round(d1["explicit_auc"], 3)
    ax.axhline(0, color="black", lw=0.8)
    ax.set_xticks(range(len(MODELS)))
    ax.set_xticklabels([LABEL[m] for m in MODELS], fontsize=9)
    ax.set_ylabel("discriminability above chance (AUC − 0.5)")
    ax.legend(frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, 1.14))
    S.eyebrow(ax, "IMPLICIT VS EXPLICIT SENSITIVITY TO PROVENANCE", y=1.18)
    S.clean(ax)
    fig.tight_layout()
    save(fig, "fig3_probe")
    print("fig3:", json.dumps({f"{k[0]}|{k[1]}": v for k, v in drew.items()}))


def fig4_covariates():
    """WER (intelligibility) and comprehension by arm, per family."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.6))
    drew = {}
    for ax, col, lab, ey in [(axes[0], "wer", "word error rate", "INTELLIGIBILITY: WER BY ARM"),
                             (axes[1], "mcq_correct", "comprehension accuracy", "COMPREHENSION BY ARM")]:
        w = 0.19
        for i, m in enumerate(MODELS):
            arms = A["models"][m]["arms"]
            for j, arm in enumerate(ARMS):
                if arm not in arms or col not in arms[arm]:
                    continue
                v = arms[arm][col]
                ax.bar(i + (j - 1.5) * w, v["mean"], w, color=ARM_COL[arm], label=ARM_LABEL[arm] if (i == 0 and col == "wer") else None)
                ax.errorbar(i + (j - 1.5) * w, v["mean"], yerr=[[v["mean"] - v["ci"][0]], [v["ci"][1] - v["mean"]]],
                            color="black", capsize=2, lw=0.8)
                drew[(m, arm, col)] = round(v["mean"], 3)
        ax.set_xticks(range(len(MODELS)))
        ax.set_xticklabels([LABEL[m] for m in MODELS], fontsize=9)
        ax.set_ylabel(lab)
        if col == "mcq_correct":
            ax.set_ylim(0, 1.05)
        S.eyebrow(ax, ey, y=1.18)
        S.clean(ax)
    axes[0].legend(frameon=False, ncol=4, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, 1.14))
    fig.tight_layout()
    save(fig, "fig4_covariates")
    print("fig4:", json.dumps({"|".join(k): v for k, v in drew.items()}))


if __name__ == "__main__":
    fig2_grade()
    fig3_probe()
    fig4_covariates()
