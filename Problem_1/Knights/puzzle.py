from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Knave always lies = false
# Knight always speaks the truth = true

# Puzzle 0
# A says "I am both a knight and a knave."
# Expected: A is a Knave
knowledge0 = And(
    # Conditions given by the puzzle
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # A cannot be both a knight and a knave at the same time
    # Therefore, he is lying and therefore a knave
    Implication(AKnight, AKnave)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
# Expected: A is a Knave
#           B is a Knight
knowledge1 = And(
    # Conditions given by the puzzle
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),

    # A claims both of them are knaves,
    # but he is clearly lying as B did not confirm or deny anything
    Biconditional(AKnight, And(AKnave, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
# Expected: A is a Knave
#           B is a Knight
knowledge2 = And(
    # Conditions given by the puzzle
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
# Expected: A is a knight
#           B is a knave
#           C is a knight
knowledge3 = And(
    # Conditions given by the puzzle
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
