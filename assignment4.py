import argparse
import nltk

from nltk.tree import Tree
from model.recognizer import recognize
from model.parser import parse, count

GRAMMAR_PATH = './data/atis-grammar-cnf.cfg'


def main():
    parser = argparse.ArgumentParser(
        description='CKY algorithm'
    )

    parser.add_argument(
        '--structural', dest='structural',
        help='Derive sentence with structural ambiguity',
        action='store_true'
    )

    parser.add_argument(
        '--recognizer', dest='recognizer',
        help='Execute CKY for word recognition',
        action='store_true'
    )

    parser.add_argument(
        '--parser', dest='parser',
        help='Execute CKY for parsing',
        action='store_true'
    )

    parser.add_argument(
        '--count', dest='count',
        help='Compute number of parse trees from chart without \
              actually computing the trees (Extra Credit)',
        action='store_true'
    )

    args = parser.parse_args()

    # load the grammar
    grammar = nltk.data.load(GRAMMAR_PATH)
    # load the raw sentences
    s = nltk.data.load("grammars/large_grammars/atis_sentences.txt", "auto")
    # extract the test sentences
    t = nltk.parse.util.extract_test_sentences(s)

    if args.structural:
        # YOUR CODE HERE
        #     TODO:
        #         1) Like asked in the instruction, derive at least two sentences that
        #         exhibit structural ambiguity and indicate the different analyses
        #         (at least two per sentence) with a syntactic tree.
        pass
    elif args.recognizer:
        # YOUR CODE HERE
        #     TODO:
        #         1) Provide a list of grammatical and ungrammatical sentences (at least 10 each)
        #         and test your recognizer on these sentences.
        grammatical = []
        ungrammatical = []

        for sents in grammatical:
            val = recognize(grammar, sents)
            if val:
                print("{} is in the language of CFG.".format(sents))
            else:
                print("{} is not in the language of CFG.".format(sents))

        for sents in ungrammatical:
            val = recognize(grammar, sents)
            if val:
                print("{} is in the language of CFG.".format(sents))
            else:
                print("{} is not in the language of CFG.".format(sents))

    elif args.parser:
        # We test the parser by using ATIS test sentences.
        print("ID\t Predicted_Tree\tLabeled_Tree")
        for idx, sents in enumerate(t):
            tree = parse(grammar, sents[0])
            print("{}\t {}\t \t{}".format(idx, len(tree), sents[1]))

        # YOUR CODE HERE
        #     TODO:
        #         1) Choose an ATIS test sentence with a number of parses p
        #         such that 1 < p < 5. Visualize its parses. You can use `draw` 
        #         method to do this.

    elif args.count:
        print("ID\t Predicted_Tree\tLabeled_Tree")
        for idx, sents in enumerate(t):
            num_tree = count(grammar, sents[0])
            print("{}\t {}\t \t{}".format(idx, num_tree, sents[1]))


if __name__ == "__main__":
    main()
