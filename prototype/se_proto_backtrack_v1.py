import random 

class Game:

    stack = []
    turn = 1

    # initializer for Game class
    # creates new board with 1 placed randomly, and appends it to the stack
    def __init__(self):
        
        board = [[0 for i in range(5)] for j in range(5)]
        y, x = random.randrange(0,5), random.randrange(0,5)

        initial_board = State((y, x), board, self.turn)
        self.stack.append(initial_board)

    # backtracking algorithm that finds a solution for a given starting board
    def play(self):
        
        st = self.stack.pop()
        viable_spaces = check_valid_space(st.y, st.x, st.board)
        self.stack.append(st)

        # exit if the turn number is 25
        if self.turn >= 25: 
            print("FINISHED")
            return
        
        # if there are no viable spaces revert to previous board in stack
        if not viable_spaces:
            self.turn -= 1
            self.stack.pop()
            st.board[st.y][st.x] = 0
            self.stack.append(st.board)
            return
        
        # check all viable spaces recursively
        for vs in viable_spaces:
            self.turn += 1
            new_board = State(vs, st.board, self.turn)

            self.stack.append(new_board)
            self.play()

            if self.turn == 25: return

        # revert to previous board
        self.turn -= 1
        self.stack.pop()
        st.board[st.y][st.x] = 0
        self.stack.append(st.board)

class State:

    def __init__(self, space: tuple, state: list, turn: int):
        
        self.board = state
        self.y, self.x = space[0], space[1]

        self.board[space[0]][space[1]] = turn
    

def check_valid_space(y:int, x:int, l:list):

    viable_space = []
    r, c = min(y+1, 4), min(x+1, 4)

    for i in range(max(0, y-1), r+1):
        for j in range(max(0, x-1), c+1):
            if not (l[i][j]): viable_space.append([i, j])

    return viable_space


game = Game()
game.play()

st = game.stack.pop()
for b in st.board:
    for i in b:
        print(f"{i}\t", end='')
    print("")


# print(f"{self.turn}: {st.y, st.x}")
#     for b in st.board:
#         for i in b:
#             print(f"{i}\t", end='')
#         print("")