from typing import List
import nltk

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
    
    # print(f"Sentence : {''.join(sentence)}")
    sentence_length = len(sentence)
    print("Sentence Length :",sentence_length)
    cky_matrix = [["" for x in range(sentence_length+1)] for x in range(sentence_length)]

    print("Number of rows : ",len(cky_matrix))
    print("Number of columns : ",len(cky_matrix[:][0]))

    assert cky_matrix[0][sentence_length] == ''

    for index, word in enumerate(sentence):
        cky_matrix[index][index] = word
        word_rules = grammar.productions(rhs = word)
        cky_matrix[index][index+1] = [rule.lhs() for rule in word_rules]
        
    # cky_matrix
    all_rules = grammar.productions()

    for b in range(2,sentence_length+2):
        for i in range(1,sentence_length-b+1):
            cky_matrix[i][i+b] = []
            for k in range(1,b):
                # print(b,i,k)
                B = cky_matrix[i][i+k]
                C = cky_matrix[i+k][i+b]
                # print(B)
                # print(C)
                # all_lhs = []
                
                for x in B:
                    for y in C:
                        # print(x,y)
                        lefts = [rules.lhs() for rules in all_rules if rules.rhs() == (x,y)]
                        lefts = list(set(lefts))
                        # print(lefts)
                        # print(lefts)
                        for left in lefts:
                            if left not in cky_matrix[i][i+b]:
                                cky_matrix[i][i+b].append(left)
                                
    for b in range(2,sentence_length+1):
        i = 0
        cky_matrix[i][i+b] = []
        for k in range(1,b):
            # print(b,i,k)
            B = cky_matrix[i][i+k]
            C = cky_matrix[i+k][i+b]
            # print(B)
            # print(C)
            # all_lhs = []
            
            for x in B:
                for y in C:
                    # print(x,y)
                    lefts = [rules.lhs() for rules in all_rules if rules.rhs() == (x,y)]
                    lefts = list(set(lefts))
                    # print(lefts)
                    # print(lefts)
                    for left in lefts:
                        if left not in cky_matrix[i][i+b]:
                            cky_matrix[i][i+b].append(left)
                            
    if nltk.grammar.Nonterminal("SIGMA") in cky_matrix[0][sentence_length]:
        # print(f"True, there is the Start symbol in index {0},{sentence_length}")
        return True
    else:
        # print(f"False, there is no Start symbol in index {0},{sentence_length}")
        return False