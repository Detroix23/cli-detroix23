"""
CLI - Base
colors.py
"""

def color_table() -> None:
    """
    prints table of formatted text format options
    """
    for style in range(8):
        for fg in range(30,38):
            s1: str = ''
            for bg in range(40,48):
                format: str = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            print(s1)
        print('\n')


def main() -> None:
    color_table()

if __name__ == "__main__":
    main()