
[ CEN 4020 - Software Engineering - Final Project ]

Welcome to GRID WARS!

HOW TO PLAY
    Every new game starts at Level 1. Complete a level to advance automatically to the next.
    The ultimate goal is to successfully fill in numbers 2 through 25 according to the rules of each level.

LEVEL 1: The Inner Grid
    In this level, you'll play on a 5x5 grid with the number 1 already placed randomly by the game. Fill numbers 2
    to 25 one at a time in ascending order.

    RULES FOR PLACING NUMBERS
        - The number must be placed into an empty cell.
        - The cell must be adjacent to the previous number`s cell.

LEVEL 2: The Outer Ring
    In this level a 7x7 grid appears, keeping the inner 5x5 grid intact with all the numbers from Level 1. Now you
    must fill numbers 2 to 25 into the outer ring of the 7x7 grid.

    RULES FOR PLACING NUMBERS
        - The number must be placed into an empty cell.
        - Match one of the following from the number`s inner grid position.
                1.  Be on the same row or column as the inner position.
                2.  Be on the matching corner if the inner position
                    is one of the longest diagonals.

LEVEL 3: Return to the Inner Grid
    In this level the system clears all numbers from the inner 5x5 grid except for the 1, while the outer ring numbers from level 2
    remain. Fill numbers 2 to 25 into the inner grid, following the rules from level 1 with some additional constraints.
    
    RULES FOR PLACING NUMBERS
        - Cell must be adjacent to the previous number.
        - Cell must be on the same row or column as the matching number in the outer-ring OR on a diagonal where the number
            exists at one corner.

**Dead Ends and Undos**
    Even if the rules are followed, sometimes a dead-end may occur which means that there are no valid tiles
    available for the next number. If this occurs players can undo turns one at a time, starting from the most
    recent, to resolve a dead-end. There is, however, one case where players cannot perform an undo:
        -   Players cannot undo at the beginning of a level
            (i.e. players cannot undo into a previous level).

**Hints**
    For players who are stuck or need help, clicking on the light-bulb icon will use a hint. This will give players some
    help on the current level.

**Saving**
    Clicking on the `S` icon will allows players to save their game for later. Saved games can be loaded from the main menu.
