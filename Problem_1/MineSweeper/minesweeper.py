import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
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
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # one/more mines nearby
        if len(self.cells) == self.count and self.count > 0:
            return self.cells

        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # no mine nearby
        if self.count == 0:
            return self.cells

        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # if the cell is in the sentence, remove it and reduce count
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # if the cell is in the sentence, remove it
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)

        nearbyCells = self.getNearbyCells(cell)
        sentence = Sentence(nearbyCells, count)
        self.knowledge.append(sentence)

        checkFlag = True

        # loop through all sentences and find is there any additional cells that could be marked as safe/mine
        while checkFlag:
            checkFlag = False

            for sentence in self.knowledge:
                knownSafes = sentence.known_safes()
                knownMines = sentence.known_mines()

                # mark all cells that's known to be safe
                for cell in knownSafes.copy():
                    self.mark_safe(cell)
                    checkFlag = True

                # mark all cells that's known to be mine
                for cell in knownMines.copy():
                    self.mark_mine(cell)
                    checkFlag = True

                # remove all empty knowledge as those serve no purpose other than wasting memory
                if len(sentence.cells) == 0:
                    self.knowledge.remove(sentence)

        print("All Sentence:")
        for sentence in self.knowledge:
            print(f"Sentence: {sentence}")
        print("\n")

        # iterate all knowledge and check is there any cell that could be inferred from existing knowledge
        for s1 in self.knowledge:
            for s2 in self.knowledge:
                # create a new sentence if s1 is s2's subset,
                # I.E: one/more cells appears in both sentence at the same time
                if s1.cells.issubset(s2.cells):
                    newSentenceCell = s2.cells - s1.cells
                    newSentenceCount = s2.count - s1.count
                    newSentence = Sentence(newSentenceCell, newSentenceCount)

                    # append the new sentence to the knowledge if isn't empty and not already in knowledge
                    if newSentenceCell and newSentence not in self.knowledge:
                        print(f"Sentence 1: {s1}, count {s1.count}")
                        print(f"Sentence 2: {s2}, count {s2.count}")
                        print(f"Appending {newSentence.__str__()} to Knowledge \n")
                        self.knowledge.append(newSentence)
                        safes = newSentence.known_safes()
                        mines = newSentence.known_mines()

                        # mark all cells that's known to be safe
                        for cell in safes.copy():
                            self.mark_safe(cell)

                        # mark all cells that's known to be mine
                        for cell in mines.copy():
                            self.mark_mine(cell)

    # Function modified from the nearby_mines method of class Minesweeper
    def getNearbyCells(self, inputted_cell):
        cells = set()

        # Loop over all cells within one row and column
        for i in range(inputted_cell[0] - 1, inputted_cell[0] + 2):
            for j in range(inputted_cell[1] - 1, inputted_cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == inputted_cell:
                    continue

                # limit the search range of nearby cell to those that could be reached
                if 0 <= i < self.height and 0 <= j < self.width:
                    # add the nearby cell to the list
                    nearbyCell = (i, j)
                    cells.add(nearbyCell)

        # remove the cells that are already known to be safe or mine
        # for cell in cells.copy():
        #     if cell in self.mines or cell in self.safes:
        #         cells.remove(cell)

        return cells

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Loop through all known safe moves
        for move in self.safes:
            # return the move if it isn't been take before and isn't known to be mine
            if move not in self.moves_made and move not in self.mines:
                return move

        # No safe move can be guaranteed, return None
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Generate a random move
        randomMove = (random.randint(0, self.height - 1), random.randint(0, self.width - 1))

        if randomMove in self.moves_made or randomMove in self.mines:
            # Regenerate the move if it's already been chosen or known to be mines
            self.make_random_move()
        elif randomMove not in self.moves_made and randomMove not in self.mines:
            # return the move if it's available
            return randomMove

        # No possible move available, return None
        return None
