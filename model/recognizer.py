"""
File: recognizer.py

This module defines a function for recognizing whether a given sentence belongs to the language defined by a given context-free grammar (CFG).

Functions:
    - recognize(grammar: nltk.grammar.CFG, sentence: List[str]) -> bool:
        Recognizes whether a sentence is in the language defined by the grammar.

Usage:
    import nltk
    from recognizer import recognize

    # Example usage with a context-free grammar and a sentence
    cfg = nltk.CFG.fromstring('''
        S -> NP VP
        NP -> Det N | 'John'
        VP -> V NP | V
        Det -> 'the' | 'a'
        N -> 'dog' | 'cat'
        V -> 'chased'
    ''')

    sentence = ['John', 'chased', 'the', 'dog']
    is_in_language = recognize(cfg, sentence)
    print(f"The sentence is in the language: {is_in_language}")
"""
from typing import List
import nltk

def recognize(grammar: nltk.grammar.CFG, sentence: List[str]) -> bool:
    """
    Recognize whether a sentence is in the language defined by a given context-free grammar.

    Args:
        grammar (nltk.grammar.CFG): Grammar rule that is used to determine the grammaticality of the sentence.
        sentence (List[str]): Input sentence that will be tested.

    Returns:
        bool: A boolean value indicating whether the sentence is in the grammar provided or not.
    """
    sentence_length = len(sentence)
    print("Sentence Length :",sentence_length)
    cky_matrix = [[set() for _ in range(sentence_length+1)] for _ in range(sentence_length+1)]

    print("Number of rows : ",len(cky_matrix))
    print("Number of columns : ",len(cky_matrix[:][0]))

    for index, word in enumerate(sentence):
        cky_matrix[index][index] = word
        word_rules = grammar.productions(rhs = word)
        cky_matrix[index][index+1] = set([rule.lhs() for rule in word_rules])
    
    all_rules = grammar.productions()
    
    for width in range(2,sentence_length+1):
        for start in range(sentence_length - width + 1):
            end = start + width
            for mid in range(start + 1, end):
                for rule in all_rules:
                    if len(rule.rhs()) == 2:
                        B, C = rule.rhs()
                        if B in cky_matrix[start][mid] and C in cky_matrix[mid][end]:
                            cky_matrix[start][end].add(rule.lhs())
                            
    start_symbol = grammar.start()
    return start_symbol in cky_matrix[0][sentence_length]

    # less efficient method that checks all rules to see if B and C produce a rhs. Above method goes throught the
    # set of production rules once only per spot in the matrix
    # # cky_matrix
    # all_rules = grammar.productions()

    # for b in range(2,sentence_length+2):
    #     for i in range(1,sentence_length-b+1):
    #         cky_matrix[i][i+b] = []
    #         for k in range(1,b):
    #             # print(b,i,k)
    #             B = cky_matrix[i][i+k]
    #             C = cky_matrix[i+k][i+b]
    #             # print(B)
    #             # print(C)
    #             # all_lhs = []
                
    #             for x in B:
    #                 for y in C:
    #                     # print(x,y)
    #                     lefts = [rules.lhs() for rules in all_rules if rules.rhs() == (x,y)]
    #                     lefts = list(set(lefts))
    #                     # print(lefts)
    #                     # print(lefts)
    #                     for left in lefts:
    #                         if left not in cky_matrix[i][i+b]:
    #                             cky_matrix[i][i+b].append(left)
                                
    # for b in range(2,sentence_length+1):
    #     i = 0
    #     cky_matrix[i][i+b] = []
    #     for k in range(1,b):
    #         # print(b,i,k)
    #         B = cky_matrix[i][i+k]
    #         C = cky_matrix[i+k][i+b]
    #         # print(B)
    #         # print(C)
    #         # all_lhs = []
            
    #         for x in B:
    #             for y in C:
    #                 # print(x,y)
    #                 lefts = [rules.lhs() for rules in all_rules if rules.rhs() == (x,y)]
    #                 lefts = list(set(lefts))
    #                 # print(lefts)
    #                 # print(lefts)
    #                 for left in lefts:
    #                     if left not in cky_matrix[i][i+b]:
    #                         cky_matrix[i][i+b].append(left)
                            
    # if nltk.grammar.Nonterminal("SIGMA") in cky_matrix[0][sentence_length]:
    #     # print(f"True, there is the Start symbol in index {0},{sentence_length}")
    #     return True
    # else:
    #     # print(f"False, there is no Start symbol in index {0},{sentence_length}")
    #     return False