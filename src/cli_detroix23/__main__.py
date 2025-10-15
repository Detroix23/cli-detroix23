#!/.venv/bin/python
"""
main.py
"""
import compatibility.plateform as plateform
import test.debug
import base.style as style
import base.models as models
import base.colors
import base.exemples
import animations.exemples
import animations.loadings as loadings
import inputs.select_menu as select
import inputs.exemples
import shapes.exemples

def main() -> None:
    print("# CLI module for Python, by Detroix23.")
    print(f"Running on {plateform.OS}")

    user_in: bool = True
    debug: bool = True

    if debug:
        test.debug.ENABLE_DEBUG = True
    
    try:
        while user_in:
            main_select: select.SelectMenu = select.SelectMenu(
                [
                    "Animations.Matrix",
                    "Animations.GameOfLife",
                    #"Base.Style", 
                    "Animations.Loadings",
                    "Base.Models",
                    "Shapes.Base",
                    "Base.Colors",
                    "Inputs.Keys",
                    "Quit",
                ],
                models.select_gh_style("Select widget.")
            )
            user_main_choice: str = main_select.show()
            print()

            if user_main_choice == "Animations.Matrix":
                animations.exemples.run_matrix()

            elif user_main_choice == "Animations.GameOfLife":
                animations.exemples.run_game_of_life()

            elif user_main_choice == "Base.Style":
                base.exemples.main()

            elif user_main_choice == "Animations.Loadings":
                loadings.main()

            elif user_main_choice == "Base.Models":
                print(models.input_gh_style("What's your name ? I dont read it actually.", usage="asd", default="a"))
                print(models.bool_gh_style("You sure ? But I dont care"))
                print(models.select_gh_style("You know this one."))

                print()

            elif user_main_choice == "Shapes.Base":
                shapes.exemples.run_exemple1()

            elif user_main_choice == "Base.Colors":
                base.colors.main()

            elif user_main_choice == "Inputs.Keys":
                inputs.exemples.run_basic_keys()

            elif user_main_choice == "Quit":
                style.printc("Quiting.", style=style.Color.YELLOW)
                user_in = False

            else:
                style.printc("Quiting (Not a valid choice).", style=style.Color.YELLOW)
                user_in = False

    except KeyboardInterrupt:
        user_in = False
        style.printc("Quiting (Ctrl+C).", style=style.Color.YELLOW)

    finally:
        if plateform.OS == plateform.Os.UNIX:
            import compatibility.unix

            test.debug.debug_print("__main__.main - End CLI reseted settings.")
            compatibility.unix.set_to_default()

if __name__ == "__main__":
    main()