"""
main.py
"""

import animations.screen as screen
import animations.loadings as loadings
import inputs.select_menu as select
import base.style as style
import base.models as models

def main() -> None:
    print("# CLI module for Python, by Detroix23.")
    
    user_in: bool = True
    while user_in:
        main_select: select.SelectMenu = select.SelectMenu(
            [
                "Animations.Matrix",
                "Base.Style", 
                "Animations.Loadings",
                "Quit",
            ],
            models.select_gh_style("Select widget.")
        )
        user_main_choice: str = main_select.show()
        print()

        if user_main_choice == "Animations.Matrix":
            screen.main()

        if user_main_choice == "Base.Style":
            style.main()

        if user_main_choice == "Animations.Loadings":
            loadings.main()

        elif user_main_choice == "Quit":
            style.printc("Quiting.", style=style.Color.YELLOW)
            user_in = False


if __name__ == "__main__":
    main()