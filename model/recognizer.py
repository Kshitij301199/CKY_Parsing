import nltk

from typing import List


def recognize(grammar: nltk.grammar.CFG, sentence: List[str]) -> bool:
    """
    Recognize whether a sentence in the language of grammar or not.

    Args:
        grammar: Grammar rule that is used to determine grammaticality of sentence.
        sentence: Input sentence that will be tested.

    Returns:
        truth_value: A bool value to determine whether if the sentence
        is in the grammar provided or not.
    """
    # YOUR CODE HERE
    #     TODO:
    #         1) Implement the CKY algorithm and use it as a recognizer.

    ############################ STUDENT SOLUTION ###########################
    pass
    #########################################################################