import itertools
import random


class MineSweeper():
    def __init__(self, height=8, width=8, mines=8):
        self.height = height
        self.width = width
        self.mines = set()

        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        self.mines_found = set()

    def print_board(self):
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        count = 0
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def win(self):
        return self.mines_found == self.mines


class Sentence():
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells}={self.count}"

    def known_mines(self):
        if len(self.cells) == self.count and self.count != 0:
            return self.cells
        return set()

    def known_safes(self):
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    def __init__(self, height=8, width=8):
        self.height = height
        self.width = width
        self.moves_made = set()
        self.mines = set()
        self.safes = set()
        self.knowledge = []

    def knowledge_update(self):
        while True:
            breaker = True
            for s1 in self.knowledge:
                for s2 in self.knowledge:
                    if len(s1.cells) != 0 and len(s2.cells) != 0:
                        if s1.cells < s2.cells:
                            s2.cells -= s1.cells
                            s2.count -= s1.count
                            breaker = False
                    else:
                        if s1 in self.knowledge and len(s1.cells) == 0:
                            self.knowledge.remove(s1)
                        if s2 in self.knowledge and len(s2.cells) == 0:
                            self.knowledge.remove(s2)
            if breaker:
                break

    def mark_mine(self, cell):
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)
        self.knowledge_update()

    def mark_safe(self, cell):
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
        print(self.safes)
        self.knowledge_update()

    def add_knowledge(self, cells, count):
        self.moves_made.add(cells)
        self.mark_safe(cells)
        nearby_Cell = set()
        for i in range(cells[0] - 1, cells[0] + 2):
            for j in range(cells[1] - 1, cells[1] + 2):
                if 0 <= i < self.height and 0 <= j < self.width and (i, j) != cells:
                    nearby_Cell.add((i, j))
        nearby_unknown = nearby_Cell - self.moves_made - self.mines - self.safes
        nearby_unknown_count = count - len(nearby_Cell & self.mines)
        if len(nearby_unknown) > 0:
            self.knowledge.append(Sentence(nearby_unknown, nearby_unknown_count))
            self.knowledge_update()

        for sentence in self.knowledge:
            self.safes |= sentence.known_safes()
            self.mines |= sentence.known_mines()

    def make_safe_move(self):
        for cell in self.safes:
            if cell not in self.mines:
                if cell not in self.moves_made:
                    return cell
        return None

    def make_random_move(self):
        possiblemoves = []
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    possiblemoves.append((i, j))
        if len(possiblemoves) != 0:
            return random.choice(possiblemoves)
        else:
            return None



