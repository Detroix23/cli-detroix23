"""
Terminal - MATHS
transformations.py
"""

import maths.maths as base

def simple_cos(a: int) -> int:
    """
    Return obvious cosine, taking a as degrees.
    """
    map: dict[int, int] = {
        0: 1,
        90: 0,
        180: -1,
        270: 0,
    }
    a = a % 360
    if a not in map.keys():
        raise ValueError(f"(X) - Simple cosine accept only simple values. {a} not in ({map}).")
    
    return map[a]

def simple_sin(a: int) -> int:
    """
    Return obvious sine, taking a as degrees.
    """
    map: dict[int, int] = {
        0: 0,
        90: 1,
        180: 0,
        270: -1,
    }
    a = a % 360
    if a not in map.keys():
        raise ValueError(f"(X) - Simple sine accept only simple values. {a} not in ({map}).")
    
    return map[a]


def rotation(table: base.table2D, angle: int) -> base.table2D:
    """
    Rotate a table, with simple degree angles, using:
    x' = x * cos(angle) - y * sin(angle)
    y' = x * sin(angle) + y * cos(angle).
    Positive rotate the sprite to the left.
    """
    # Create table.
    x_max: int = 0
    for row in table:
        if len(row) > x_max:
            x_max = len(row)
    y_max: int = len(table)
    x_mid: int = len(table[0]) // 2
    y_mid: int = len(table) // 2

    new_table: base.table2D = base.create_table(base.Size(
        abs(x_max * simple_cos(angle) - y_max * simple_sin(angle)),
        abs(x_max * simple_sin(angle) + y_max * simple_cos(angle)),
    ))

    # Rotate.
    for y, row in enumerate(table):
        for x, char in enumerate(row):
            x_prime: int = (x - x_mid) * simple_cos(angle) - (y - y_mid) * simple_sin(angle)
            y_prime: int = (x - x_mid) * simple_sin(angle) + (y - y_mid) * simple_cos(angle)
            try:
                new_table[y_prime + y_mid][x_prime + x_mid] = char
            except IndexError:
                raise IndexError(f"(X) - Trans.Rotation: x={x_prime + x_mid}, y={y_prime + y_mid}. Table: {table}, New: {new_table}")

    return new_table