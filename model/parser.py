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
    sentence_length = len(sentence)
    print("Sentence Length :",sentence_length)
    cky_matrix = [["" for x in range(sentence_length+1)] for x in range(sentence_length)]

    print("Number of rows : ",len(cky_matrix))
    print("Number of columns : ",len(cky_matrix[:][0]))

    assert cky_matrix[0][sentence_length] == ''
    
    for index, word in enumerate(sentence):
        cky_matrix[index][index] = word
        word_rules = grammar.productions(rhs = word)
        cky_matrix[index][index+1] = [(index,index,index+1,rule.lhs(),index,index) for rule in word_rules]
        
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
                
                for indx, x in enumerate(B):
                    for indy, y in enumerate(C):
                        # print(x,y)
                        lefts = [(i,i+k,i+b,rules.lhs(),indx,indy) for rules in all_rules if rules.rhs() == (x[3],y[3])]
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
            
            for indx, x in enumerate(B):
                for indy, y in enumerate(C):
                    # print(x,y)
                    lefts = [(i,i+k,i+b,rules.lhs(),indx,indy) for rules in all_rules if rules.rhs() == (x[3],y[3])]
                    lefts = list(set(lefts))
                    # print(lefts)
                    # print(lefts)
                    for left in lefts:
                        if left not in cky_matrix[i][i+b]:
                            cky_matrix[i][i+b].append(left)
                            
    terminal_list = [item for item in cky_matrix[0][sentence_length] if item[3] == nltk.grammar.Nonterminal("SIGMA")]

                            
    # if nltk.grammar.Nonterminal("SIGMA") in cky_matrix[0][sentence_length]:
        # print(f"True, there is the Start symbol in index {0},{sentence_length}")
        # return True
    # else:
        # print(f"False, there is no Start symbol in index {0},{sentence_length}")
        # return False
        
    end_list = set([(i,i+1) for i in range(sentence_length)])
    word_list = set([(i,i) for i in range(sentence_length)])
    all_trees = []

    for element in terminal_list:
        flag = True
        roots = [element]
        checked_list = []
        # limit = 100
        # i = 0
        
        while flag:
            # i+=1
            # if i > limit:
            #     break
            for root in roots:
                print(root)
                if type(root) != str:
                    if root[:2] in word_list:
                        print("oof")
                        checked_list.append(root[1:3])
                        continue
                    elif (root[0],root[2]) in checked_list:
                        print("oof2")
                        continue
                    else:
                        print(f"getting children for {root}")
                        next_x, next_y = get_children(cky_matrix, root)
                        checked_list.append((root[0],root[2]))
                        roots.append(next_x)
                        roots.append(next_y)
                        print(roots)
                        print(checked_list)
                    
            assert type(roots) == list
                
            final_list = [(root[0],root[2]) for root in roots]
            print("Checking")
            flag = not(set(end_list) == set([value for value in final_list if value in end_list]))
            print(flag)
            
        all_trees.append(roots)
        
        
def get_children(matrix, element):
    a,b,c,indx,indy = element[0],element[1],element[2],element[-2],element[-1]

    next_x = matrix[a][b][indx]
    next_y = matrix[b][c][indy]
    
    return next_x, next_y

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