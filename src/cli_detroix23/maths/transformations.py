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
    a %= 360
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
    a %= 360
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
    print(f"\nROTATION with table {table}, angle {angle}deg.")

    raise_negative: bool = True
    # Create table.
    x_max_original: int = 0
    for row in table:
        if len(row) > x_max_original:
            x_max_original = len(row)
    y_max_original: int = len(table)

    size_max: base.Size = base.Size(
        abs(x_max_original * simple_cos(angle) - y_max_original * simple_sin(angle)),
        abs(x_max_original * simple_sin(angle) + y_max_original * simple_cos(angle)),
    )

    new_table: base.table2D = base.create_table(size_max, character="_")

    # Rotate.
    for y, row in enumerate(table):
        for x, char in enumerate(row):
            x_prime: int = (x) * simple_cos(angle) - (y) * simple_sin(angle)
            y_prime: int = (x) * simple_sin(angle) + (y) * simple_cos(angle)
            x_index: int = x_prime if x_prime >= 0 else size_max.x + x_prime
            y_index: int = y_prime if y_prime >= 0 else size_max.y + y_prime

            print(f"Char: {char}.")
            try:
                if raise_negative and (y_index < 0 or x_index < 0):
                    raise IndexError('(X) - Trans.Rotation: neg.')
                new_table[y_index][x_index]

            except IndexError:
                raise IndexError(f"""(X) - Trans.Rotation:                     
a={angle} char='{char}' 
x={x}, y={y} 
x'={x_prime}, y'={y_prime}
xi={x_index}, yi={y_index} 
Table: {table}, 
New: {new_table}
""")
            else:
                new_table[y_index][x_index] = char

    return new_table


def transpose(table: base.table2D) -> base.table2D:
    """
    Return a transposed list of list <=> -90 degrees rotation + mirroring. \n
    ```
    [[1, 2, 3], => [[1, 4], \r
     [4, 5, 6]]     [2, 5], \r
                    [3, 6]] \r
    ```
    """
    return [list(t) for t in list(zip(*table))]

def mirror(table: base.table2D) -> base.table2D:
    """
    Mirror the sub-lists.
    """
    new: base.table2D = list()
    for row in table:
        for i in range(len(row) // 2):
            row[i], row[len(row) - i - 1] = row[len(row) - i - 1], row[i]
        new.append(row)
    
    return new

def simple_rotation(table: base.table2D, angle: int) -> base.table2D:
    """
    Perform a rotation of simple degree angle.
    """
    if angle % 90 != 0:
        raise ValueError(f"(X) - Simple rotation accepts only simple angles (dividable by 90). Given {angle}.")
    
    angle %= 360
    if angle == 0:
        pass
    else:
        for _ in range(angle // 90):
            # -90 degrees rotation
            table = transpose(table)
            table = mirror(table)

    return table

    