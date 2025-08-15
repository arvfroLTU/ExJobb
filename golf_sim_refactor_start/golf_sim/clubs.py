from .types import Club

# Cohesive, data-only module
CLUBS: dict[str, Club] = {
    "Driver": Club("Driver", 210, 280),
    "3-Wood": Club("3-Wood", 192, 229),
    "5-Wood": Club("5-Wood", 183, 219),
    "3-Iron": Club("3-Iron", 165, 201),
    "4-Iron": Club("4-Iron", 155, 192),
    "5-Iron": Club("5-Iron", 146, 183),
    "6-Iron": Club("6-Iron", 137, 174),
    "7-Iron": Club("7-Iron", 128, 165),
    "8-Iron": Club("8-Iron", 119, 155),
    "9-Iron": Club("9-Iron", 110, 146),
    "Pitching Wedge": Club("Pitching Wedge", 101, 137),
    "Sand Wedge": Club("Sand Wedge", 92, 129),
    "Lob Wedge": Club("Lob Wedge", 82, 119),
    "Soft Pitching Wedge": Club("Soft Pitching Wedge", 61, 80),
    "Soft Sand Wedge": Club("Soft Sand Wedge", 28, 60),
    "Soft Lob Wedge": Club("Soft Lob Wedge", 14, 27),
    "Putter": Club("Putter", 0, 14),
}

def select_club(distance_m: float) -> str:
    s = distance_m
    if 0 <= s <= 14: return "Putter"
    if 14 < s <= 40: return "Soft Lob Wedge"
    if 40 < s <= 60: return "Soft Sand Wedge"
    if 60 < s <= 82: return "Soft Pitching Wedge"
    if 82 < s <= 119: return "Lob Wedge"
    if 119 < s <= 137: return "Sand Wedge"
    if 137 < s <= 146: return "Pitching Wedge"
    if 146 < s <= 155: return "9-Iron"
    if 155 < s <= 165: return "8-Iron"
    if 165 < s <= 174: return "7-Iron"
    if 174 < s <= 183: return "6-Iron"
    if 183 < s <= 192: return "5-Iron"
    if 192 < s <= 201: return "4-Iron"
    if 201 < s <= 210: return "3-Iron"
    if 210 < s <= 219: return "5-Wood"
    if 219 < s <= 229: return "3-Wood"
    return "Driver"
