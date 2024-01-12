import nltk

from typing import Set, List


def parse(grammar: nltk.grammar.CFG, sentence: List[str]) -> Set[nltk.ImmutableTree]:
    """
    Check whether a sentence in the language of grammar or not. If it is, parse it.

    Args:
        grammar: Grammar rule that is used to determine grammaticality of sentence.
        sentence: Input sentence that will be tested.

    Returns:
        tree_set: Set of generated parse trees.
    """
    # YOUR CODE HERE
    #     TODO:
    #         1) Extend your CKY recognizer into a parser by adding backpointers. You
    #         should extract the set of all parse trees from the backpointers in the chart.
    #         2) Note that only 'ImmutableTree` can be used as elements of Python sets.
    ############################# STUDENT SOLUTION ##################################
    pass
    #################################################################################

def count(grammar: nltk.grammar.CFG, sentence: List[str]) -> int:
    """
    Compute the number of parse trees without actually computing the parse tree.

    Args:
        grammar: Grammar rule that is used to determine grammaticality of sentence.
        sentence: Input sentence that will be tested.

    Returns:
        tree_count: Number of generated parse trees.
    """
    ############################# STUDENT SOLUTION ##################################
    pass
    #################################################################################