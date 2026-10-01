# 计算口径（随单固化，勿轻易改动）：
#   1) 出血扩边先作用 —— 印刷出血向各面外侧延伸，盒体每个维度两侧各出一个出血，
#      即有效边长 = 原边长 + 2 × bleed_mm / 1000（米）。bleed_mm 为 0 时有效几何即原长宽高。
#   2) 折边系数后作用 —— 用纸面积 = 扩边后表面积 × overlap。
BLEED_CALC_ORDER = "bleed_then_overlap"


def expand_dims(length: float, width: float, height: float, bleed_mm: float = 0.0) -> tuple:
    """Apply print bleed (mm) to box dims, returning effective dims in meters.

    Bleed extends on both sides of every dimension: eff = dim + 2 * bleed_mm / 1000.
    """
    bleed = float(bleed_mm)
    if bleed < 0:
        raise ValueError("bleed_mm must be >= 0")
    extra = 2 * bleed / 1000.0
    return (
        round(float(length) + extra, 6),
        round(float(width) + extra, 6),
        round(float(height) + extra, 6),
    )


def paper_area(length: float, width: float, height: float, overlap: float = 1.15, bleed_mm: float = 0.0) -> dict:
    bleed = float(bleed_mm)
    if bleed < 0:
        raise ValueError("bleed_mm must be >= 0")
    L, W, H = expand_dims(length, width, height, bleed)
    if min(L, W, H) <= 0:
        raise ValueError("box dimensions must be positive")
    base = 2 * (L * W + L * H + W * H)
    need = base * float(overlap)
    return {
        "box_surface": round(base, 3),
        "overlap": float(overlap),
        "paper_m2": round(need, 3),
        "bleed_mm": bleed,
        "eff_length": L,
        "eff_width": W,
        "eff_height": H,
        "calc_order": BLEED_CALC_ORDER,
    }


def ribbon_estimate(length: float, width: float, height: float, wrap_style: str = "cross") -> dict:
    """Helper: approximate ribbon length in meters (not stored as primary metric)."""
    L, W, H = float(length), float(width), float(height)
    girth = 2 * (W + H)
    if wrap_style == "band":
        meters = girth + 0.3
    else:
        meters = girth * 2 + L + 0.5
    return {"wrap_style": wrap_style, "ribbon_m": round(meters, 2)}
