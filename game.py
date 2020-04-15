import random
from os import system
from time import sleep


gosper_glider_gun = """
......................................
.........................#............
.......................#.#............
.............##......##............##.
............#...#....##............##.
.##........#.....#...##...............
.##........#...#.##....#.#............
...........#.....#.......#............
............#...#.....................
.............##.......................
......................................

""".replace('.', ' ')


class Game:
    def __init__(self, x, y, rand=True):
        self.x = x
        self.y = y
        if rand:
            self.grid = [[random.randint(0, 1) for i in range(y)] for j in range(x)]
        else:
            self.grid = [[0 for i in range(y)] for j in range(x)]
        self.future_state = [[0 for i in range(y)] for j in range(x)]

    def reset_future(self):
        self.future_state = [[0 for i in range(self.y)] for j in range(self.x)]

    def display(self):
        for row in self.grid:
            print(row)

    def neighbour_number(self, x, y):
        neighbours = [(x+1, y-1), (x+1, y), (x+1, y+1), (x, y-1), (x, y+1), (x-1, y-1), (x-1, y), (x-1, y+1)]
        total = 0
        for a, b in neighbours:
            if a >= 0 and b >= 0:
                try:
                    if self.grid[a][b] == 1 or self.grid[a][b] == 0:
                        total += self.grid[a][b]
                except IndexError:
                    pass
        return total

    def update_cell(self, x, y):
        neighbours = self.neighbour_number(x, y)
        if self.grid[x][y] == 1:
            if neighbours <= 1:
                # a live cell with 0 or 1 neighbour becomes dead
                return 0
            if 2 <= neighbours <= 3:
                # a live cell with 2 or 3 neighbours stays alive
                return 1
            if neighbours > 3:
                # a live cell with more than three neighbours becomes dead
                return 0
        elif self.grid[x][y] == 0:
            if neighbours == 3:
                # a dead cell with exactly three neighbours becomes alive
                return 1
            else:
                # a dead cell with any other number of neighbours stays dead
                return 0

    def update_cell_brian(self, x, y):
        neighbours = self.neighbour_number(x, y)
        if self.grid[x][y] == 1:
            # a cell that is on becomes dying
            return 0.5
        if self.grid[x][y] == 0.5:
            # a dying cell always becomes off in the next step
            return 0
        if self.grid[x][y] == 0:
            # an off cell with precisely 2 neighbours becomes on, otherwise it remains off
            if neighbours == 2:
                return 1
            else:
                return 0

    def update_grid(self):
        for i in range(self.x):
            for j in range(self.y):
                self.future_state[i][j] = self.update_cell(i, j)

        self.grid = self.future_state
        self.reset_future()

    def update_grid_brian(self):
        for i in range(self.x):
            for j in range(self.y):
                self.future_state[i][j] = self.update_cell_brian(i, j)
        self.grid = self.future_state
        self.reset_future()

    def __str__(self):
        string = ''
        for row in self.grid:
            for cell in row:
                if cell == 1:
                    string += '#'
                elif cell == 0:
                    string += ' '
                elif cell == 0.5:
                    string += '.'
            string += '\n'
        return string

    def run(self):
        while True:
            print(self)
            sleep(0.1)
            self.update_grid()
            system('clear')

    def run_brian(self):
        while True:
            print(self)
            sleep(0.1)
            self.update_grid_brian()
            system('clear')

    def load_from_string(self, string):
        rows = string.split('\n')
        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                if cell == ' ':
                    self.grid[i][j] = 0
                elif cell == '#':
                    self.grid[i][j] = 1
                elif cell == '.':
                    self.grid[i][j] = 0.5


if __name__ == '__main__':
    game = Game(40, 150)
    # game.run_brian()
    game.run()
