class LightPuzzle:
    def __init__(self):
        self.statearray = [[0, 1, 0], [1, 1, 0], [0, 1, 1]]
        self.solved = False

    def PrintPuzzle(self):
        for row in self.statearray:
            rowprint = " ".join([str(tile) for tile in row])
            print(rowprint)
        print()

    def FlipTile(self, x, y):
        self.statearray[y][x] = self.ChangeState(self.statearray[y][x])
        if y > 0:
            self.statearray[y-1][x] = self.ChangeState(self.statearray[y-1][x])
        if y < len(self.statearray) - 1:
            self.statearray[y+1][x] = self.ChangeState(self.statearray[y+1][x])
        if x > 0:
            self.statearray[y][x-1] = self.ChangeState(self.statearray[y][x-1])
        if x < len(self.statearray[y]) - 1:
            self.statearray[y][x+1] = self.ChangeState(self.statearray[y][x+1])

    def ChangeState(self, number):
        return 0 if number == 1 else 1

    def TakeEdit(self):
        valid = False
        while not valid:
            ToChange = input("What part of the puzzle would you like to flip? Enter coordinates in the format X,Y (1-3): ")
            XY = ToChange.split(",")
            if len(XY) != 2 or not XY[0].isdigit() or not XY[1].isdigit():
                print("Invalid input. Please enter two numbers separated by a comma.")
            elif int(XY[0]) > 3 or int(XY[0]) < 1 or int(XY[1]) > 3 or int(XY[1]) < 1:
                print("Invalid input. Coordinates must be between 1 and 3.")
            else:
                valid = True

        self.FlipTile(int(XY[0]) - 1, 3 - int(XY[1]))

    def StartPuzzle(self):
        while not self.solved:
            self.PrintPuzzle()
            self.TakeEdit()
            self.CheckSolved()
        print("Puzzle solved!")

    def CheckSolved(self):
        for row in self.statearray:
            if 0 in row:
                return
        self.solved = True

puzzle = LightPuzzle()
puzzle.StartPuzzle()

