from sudoku import *
from solver import *

if __name__ == "__main__":
    while True:
        input_is_valid = False
        while input_is_valid is False:
            user_input = list(input("Input the sudoku you want to solve as a continuous sequence of numbers with each digit divided by a comma. For empty squares input '0':\n"))
            user_input = [int(number) for number in user_input if number.isdigit()]
            if len(user_input) == 81 and all([isinstance(number, int) for number in user_input]) and all(number >= 0 and number < 10 for number in user_input):
                sudoku_to_solve = user_input
                break
            else:
                print("Input invalid! Please try again.")
        while input_is_valid is False:
            user_input = input("Do you want the sudoku to be solved the oring way (a) or the not so boring way (b)?\n The boring way should be able to solve every sudoku and yield all solutions if there are multiple, although if there are multiple then it isn't really a proper sudoku. \n The not so boring way can probably only solve about 95% of sudoku you may encounter in some newspapers and similiar and employs methods that are commonly used by people who are pretty good at solving sudokus. Because of this it can only solve sudokus that are actually solvable by humans which does not have to be the case for the boring way.\n \n solve the sudoku the \n a) The boring way \n b) The not so boring way \n Input 'a' or 'b': \n")
            if user_input == "a":
                boring_mode = True
                break
            if user_input == "b":
                boring_mode = False
                break
        else:
            print("Invalid input!\n Input either 'a' or 'b'. Without the single quotes.")
        New_Sudoku = Sudoku()
        New_Solver = Solver(New_Sudoku)
        New_Sudoku.input_numbers(sudoku_to_solve)
        if boring_mode == True:
            New_Solver.get_solutions()
            print(New_Solver.solutions)
        if boring_mode == False:
            if New_Solver.solve() == True:
                print([square.number for square in New_Sudoku.squares])
            else: print("Sorry, that was too difficult and I could't solve it.")
        break


