from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # Conditions given by the puzzle
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # A cannot be both a knight and a knave at the same time
    # Thus, he is lying and therefore a knave
    Implication(AKnight, AKnave)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Conditions given by the puzzle
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),

    # As B did not confirm or deny anything
    # Therefore A's claim of they are both knaves is clearly a lie
    Biconditional(AKnight, And(AKnave, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # Conditions given by the puzzle
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),

    # Check B's claim , where he claims that he IS NOT the same kind as A
    # Which appeared to be the truth as the rule stated that the knight would not lie
    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    # Check A's claim, where he claims that he IS the same kind as B
    # Which appeared to be a lie, as B denied his claim, thus indicating that A is a knave
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # Conditions given by the puzzle
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),

    # If C is speaking the truth, then C and A are both Knight
    Biconditional(CKnight, AKnight),
    # If B is speaking the truth, then B is Knight and both C and A are Knave
    Biconditional(BKnight, And(CKnave, AKnave)),
    # We do not know what A said exactly, but if C is knight, then his claim on A is a Knight is true
    And(AKnight, Or(AKnight, AKnave), CKnight)
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
