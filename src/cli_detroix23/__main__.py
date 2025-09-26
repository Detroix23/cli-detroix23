"""
main.py
"""

import animations.exemples
import animations.loadings as loadings
import inputs.select_menu as select
import base.style as style
import base.models as models
import shapes.base
import base.colors

def main() -> None:
    print("# CLI module for Python, by Detroix23.")
    


    user_in: bool = True
    while user_in:
        main_select: select.SelectMenu = select.SelectMenu(
            [
                "Animations.Matrix",
                "Base.Style", 
                "Animations.Loadings",
                "Base.Models",
                "Shapes.Base",
                "Base.Colors",
                "Quit",
            ],
            models.select_gh_style("Select widget.")
        )
        user_main_choice: str = main_select.show()
        print()

        if user_main_choice == "Animations.Matrix":
            animations.exemples.run_matrix()

        elif user_main_choice == "Base.Style":
            style.main()

        elif user_main_choice == "Animations.Loadings":
            loadings.main()

        elif user_main_choice == "Base.Models":
            print(models.input_gh_style("What's your name ? I dont read it actually.", usage="asd", default="a"))
            print(models.bool_gh_style("You sure ? But I dont care"))
            print(models.select_gh_style("You know this one."))

            print()

        elif user_main_choice == "Shapes.Base":
            shapes.base.run_exemple1()

        elif user_main_choice == "Base.Colors":
            base.colors.main()

        elif user_main_choice == "Quit":
            style.printc("Quiting.", style=style.Color.YELLOW)
            user_in = False


if __name__ == "__main__":
    main()