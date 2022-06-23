import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    propDist = dict()
    linkedPageNum = len(corpus[page])
    totalPageNum = len(corpus)
    randomProp = (1 - damping_factor) / totalPageNum

    if linkedPageNum != 0:
        # The page have outgoing links, set the probability of each page
        for linkedPage in corpus:
            if linkedPage in corpus[page]:
                # set the probability of the user randomly choose that link
                propDist[linkedPage] = (damping_factor / linkedPageNum) + randomProp
            else:
                # set the random probability to the page itself
                propDist[linkedPage] = randomProp
    else:
        # The page had no outgoing links, treat each link equally
        for page in corpus:
            propDist[page] = 1 / totalPageNum

    return propDist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    randomChoiceStr = ""
    sample = dict()

    # initialize a page list for the random picker to choose from
    for page in corpus:
        sample[page] = 0

    # start sampling the probability
    for sampleNumber in range(n):
        # first sample, choose randomly
        if sampleNumber == 0:
            randomChoiceStr = random.choices(list(corpus.keys()), k=1)[0]

        # choose according to the current sampled probability
        else:
            # get the probability distribution of the previous sample
            propDist = transition_model(corpus, randomChoiceStr, damping_factor)

            # convert the probability distribution to list for the random pick to reference from
            propDistList = list(propDist.values())

            # randomly pick a page based on the probability distribution
            randomChoice = random.choices(tuple(sample), propDistList)

            # convert the choice to string for dictionary manipulation
            randomChoiceStr = " ".join(randomChoice)

            # increment the visit counter of the picked page
            sample[randomChoiceStr] = sample.get(str(randomChoiceStr), 0) + 1

    # normalize to the value of the sample to 1
    for results in sample:
        sample[results] = sample.get(results) / n

    return sample


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    prValue = dict()
    totalPageNum = len(corpus)

    # Assign an initial rank of 1/total number of page to each page
    for page in corpus:
        prValue[page] = 1 / totalPageNum

    return prValue


if __name__ == "__main__":
    main()
