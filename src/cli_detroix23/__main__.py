#!/.venv/bin/python
"""
# CLI.
src/cli_detroix23/__main__.py

Main script to test, and show examples of the library.
"""
from cli_detroix23.compatibility import plateform
from cli_detroix23 import test
from cli_detroix23 import base
from cli_detroix23.base import style, models
from cli_detroix23 import animations
from cli_detroix23.animations import loadings
from cli_detroix23 import inputs
from cli_detroix23.inputs import select_menu
from cli_detroix23 import shapes

def main() -> None:
    print("# CLI module for Python, by Detroix23.")
    if plateform.OS == plateform.Os.UNIX:
        from cli_detroix23.compatibility import unix

        print(f"Running on UNIX.")
        unix.print_attr(unix.SETTINGS)
    

    settings: inputs.start.Settings = inputs.start.Settings()

    settings.read_arguments()
    if settings.enable_debug:
        test.debug.ENABLE_DEBUG = True
    test.debug.debug_print(f"Args: {settings.args}")

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
                animations.exemples.run_matrix()

            elif settings.choice == "Animations.GameOfLife":
                animations.exemples.run_game_of_life()

            elif settings.choice == "Base.Style":
                base.exemples.main()

            elif settings.choice == "Animations.Loadings":
                loadings.main()

            elif settings.choice == "Base.Models":
                print(models.input_gh_style("What's your name ? I dont read it actually.", usage="asd", default="a"))
                print(models.bool_gh_style("You sure ? But I dont care"))
                print(models.select_gh_style("You know this one."))

                print()

            elif settings.choice == "Shapes.Base":
                shapes.exemples.run_exemple1()

            elif settings.choice == "Base.Colors":
                base.colors.main()

            elif settings.choice == "Inputs.Keys":
                inputs.exemples.run_basic_keys()

            elif settings.choice == "Inputs.Stdin":
                inputs.exemples.run_sys_reading()

            elif settings.choice == "Quit":
                style.printc("Quiting.", style=style.Color.YELLOW)
                settings.user_in = False

            else:
                style.printc("Quiting (Not a valid choice).", style=style.Color.YELLOW)
                settings.user_in = False

    except KeyboardInterrupt:
        settings.user_in = False
        style.printc("Quiting (Ctrl+C).", style=style.Color.YELLOW)

    finally:
        if plateform.OS == plateform.Os.UNIX:
            from cli_detroix23.compatibility import unix

            test.debug.debug_print("__main__.main - End CLI reseted settings.")
            unix.set_to_default()

        print()
        base.controls.cursor_show()
        base.controls.fin()

if __name__ == "__main__":
    main()