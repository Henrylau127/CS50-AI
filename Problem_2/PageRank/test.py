import random
from numpy.random import choice
from pagerank import transition_model


def test():
    corpus0 = {'1.html': {'2.html'},
               '2.html': {'3.html', '1.html'},
               '3.html': {'4.html', '2.html'},
               '4.html': {'2.html'}}

    corpus1 = {'bfs.html': {'search.html'}, 'dfs.html': {'search.html', 'bfs.html'},
               'games.html': {'tictactoe.html', 'minesweeper.html'},
               'minesweeper.html': {'games.html'},
               'minimax.html': {'search.html', 'games.html'},
               'search.html': {'minimax.html', 'dfs.html', 'bfs.html'},
               'tictactoe.html': {'minimax.html', 'games.html'}}

    corpus2 = {'ai.html': {'algorithms.html', 'inference.html'},
               'algorithms.html': {'programming.html', 'recursion.html'}, 'c.html': {'programming.html'},
               'inference.html': {'ai.html'}, 'logic.html': {'inference.html'},
               'programming.html': {'c.html', 'python.html'}, 'python.html': {'programming.html', 'ai.html'},
               'recursion.html': set()}

    damping_factor = 0.85
    n = 1000

    randomChoiceStr = ""
    sample = dict()

    # initialize a page list for the random picker to choose from
    for page in corpus1:
        sample[page] = 0

    # start sampling the probability
    for sampleNumber in range(0, n):
        # first sample, choose randomly
        if sampleNumber == 0:
            randomChoiceStr = random.choice(tuple(sample))
            sample[randomChoiceStr] = sample.get(randomChoiceStr, 0) + 1

        # choose according to the current sampled probability
        else:
            # get the probability distribution of the previous sample
            propDist = transition_model(corpus1, randomChoiceStr, damping_factor)

            # convert the probability distribution to list for the random pick to reference from
            propDistList = list(propDist.values())

            print(propDistList)

            # randomly pick a page based on the probability distribution
            # randomChoice = random.choices(tuple(sample), propDistList)
            randomChoice = choice(tuple(sample), 1, propDistList)

            # convert the choice to string
            randomChoiceStr = " ".join(randomChoice)

            # increment the visit counter of the picked page
            sample[randomChoiceStr] = sample.get(str(randomChoiceStr), 0) + 1

    # normalize to the value of the sample to 1
    for results in sample:
        sample[results] = sample.get(results) / n

    print(sample)


if __name__ == "__main__":
    test()
