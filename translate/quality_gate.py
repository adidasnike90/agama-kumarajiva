"""Kumarajiva-style quality gates for gold merge scripts."""

from __future__ import annotations

SIM_MAX_LONG = 0.45
SIM_MAX_SHORT = 0.50
LIT_LEN_LONG = 400
LIT_MOD_GAP_MAX = 0.10


def sim_threshold(lit_len: int) -> float:
    return SIM_MAX_LONG if lit_len >= LIT_LEN_LONG else SIM_MAX_SHORT


def assess_gold(
    sim_lit: float,
    lit_len: int,
    lit_mod_gap: float,
) -> tuple[str | None, list[str]]:
    """Return (review_status_override, reasons). None = keep gold."""
    reasons: list[str] = []
    thr = sim_threshold(lit_len)
    if sim_lit >= thr:
        reasons.append(f"sim_lit={sim_lit:.3f}>={thr}")
    # 仅当白话比罗什风更贴底本时拒收（罗什风未化）；白话更远属正常
    if lit_mod_gap <= -LIT_MOD_GAP_MAX:
        reasons.append(f"modern_closer_to_source gap={lit_mod_gap:.3f}")
    if reasons:
        return "needs_restyle", reasons
    return None, []
