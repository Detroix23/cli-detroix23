#!/.venv/bin/python
"""
# CLI.
src/cli_detroix23/__main__.py

Main script to test, and show examples of the library.
"""

import os

from cli_detroix23.compatibility import platform, defaults, debug
from cli_detroix23 import base, inputs, shapes, animations
from cli_detroix23.base import style, models
from cli_detroix23.animations import loadings
from cli_detroix23.inputs import select_menu

def main() -> None:
    print("# CLI module for Python, by Detroix23.\n\n")

    # Settings and arguments.
    settings: inputs.start.Settings = inputs.start.Settings()

    settings.read_arguments()
    if settings.enable_debug:
        debug.ENABLE_DEBUG = True
    
    debug.debug_print(f"__main__.main() Args: {settings.args}")

    # OS-wise configuration.
    if os.name == "posix":
        from cli_detroix23.compatibility import unix

        debug.debug_print("__main__.main() Running on UNIX.")
        unix.print_attr(unix.SETTINGS)
    
    elif platform.OS == platform.Os.WINDOWS:
        debug.debug_print("__main__.main() Running on WINDOWS.")

    if debug.ENABLE_DEBUG:
        debug.debug_print("__main__.main() Debug enabled.")

    # Selection loop.
    settings.user_in = True

    try:
        while settings.user_in:
            main_select: select_menu.SelectMenu = select_menu.SelectMenu(
                [
                    "Animations.Matrix",
                    "Animations.GameOfLife",
                    #"Base.Style", 
                    "Animations.Loadings",
                    "Base.Models",
                    "Shapes.Base",
                    "Base.Colors",
                    "Inputs.Keys",
                    "Inputs.Stdin",
                    "Quit",
                ],
                models.select_gh_style("Select widget.")
            )
            settings.choice = main_select.show()
            print()

            if settings.choice == "Animations.Matrix":
                animations.examples.run_matrix()

            elif settings.choice == "Animations.GameOfLife":
                animations.examples.run_game_of_life()

            elif settings.choice == "Base.Style":
                base.examples.main()

            elif settings.choice == "Animations.Loadings":
                loadings.main()

            elif settings.choice == "Base.Models":
                print(models.input_gh_style("What's your name ? I dont read it actually.", usage="asd", default="a"))
                print(models.bool_gh_style("You sure ? But I dont care"))
                print(models.select_gh_style("You know this one."))
                print()

            elif settings.choice == "Shapes.Base":
                shapes.examples.run_example1()

            elif settings.choice == "Base.Colors":
                base.colors.main()

            elif settings.choice == "Inputs.Keys":
                inputs.examples.run_basic_keys()

            elif settings.choice == "Inputs.Stdin":
                inputs.examples.run_sys_reading()

            elif settings.choice == "Quit":
                style.printc(f"{defaults.LOG_INFO}Quitting (from menu).", style=style.Color.YELLOW)
                settings.user_in = False

            else:
                style.printc(f"{defaults.LOG_INFO}Quitting (somehow, not a valid choice).", style=style.Color.YELLOW)
                settings.user_in = False

    except KeyboardInterrupt:
        settings.user_in = False
        style.printc(f"{defaults.LOG_INFO}Quitting (Ctrl+C).", style=style.Color.YELLOW)

    finally:
        if os.name == "posix":
            from cli_detroix23.compatibility import unix

            debug.debug_print(f"{defaults.LOG_INFO} __main__.main End of CLI: reset settings.")
            unix.set_to_default()

        print()
        base.controls.cursor_show()
        base.controls.fin()

if __name__ == "__main__":
    main()
