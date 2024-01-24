"""
File: parser.py

This module defines functions for parsing sentences using a context-free grammar (CFG).

Functions:
    - parse(grammar: nltk.grammar.CFG, sentence: List[str]) -> Set[nltk.ImmutableTree]:
        Checks whether a sentence is in the language of a given grammar and parses it.
    - form_tree(node_list: List[Tuple[int, int, str]]) -> Dict[str, Union[str, List[str]]]:
        Forms a tree structure from a list of nodes representing the parse.
    - build_tree(grammar_dict: Dict[str, Union[str, List[str]]], start_symbol: str) -> nltk.Tree:
        Builds an nltk.Tree from a dictionary representation of a parse tree.
    - count(grammar: nltk.grammar.CFG, sentence: List[str]) -> int:
        Computes the number of parse trees without actually computing the parse tree.

Usage:
    import nltk
    from parser import parse, count

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
    
    # Parse the sentence and get the set of parse trees
    parse_trees = parse(cfg, sentence)
    
    print(f"Number of parse trees: {len(parse_trees)}")
    for tree in parse_trees:
        print(tree.pformat())
"""

import nltk
from nltk import Tree

from typing import Set, List

def parse(grammar: nltk.grammar.CFG, sentence: List[str]) -> Set[nltk.ImmutableTree]:
    """
    Check whether a sentence is in the language of a given grammar and parse it.

    Args:
        grammar: Grammar rule that is used to determine grammaticality of the sentence.
        sentence: Input sentence that will be tested.

    Returns:
        tree_set: Set of generated parse trees.
    """
    global sentence_length 
    global sentence_glob 
    sentence_glob = sentence
    sentence_length = len(sentence)
    print("Sentence Length :",sentence_length)
    cky_matrix = [[set() for _ in range(sentence_length+1)] for _ in range(sentence_length+1)]
    backpointers = [[[] for _ in range(sentence_length+1)] for _ in range(sentence_length+1)]

    # print("Number of rows : ",len(cky_matrix))
    # print("Number of columns : ",len(cky_matrix[:][0]))

    # assert cky_matrix[0][sentence_length] == ''
        
    for index, word in enumerate(sentence):
            cky_matrix[index][index] = word
            word_rules = grammar.productions(rhs = word)
            cky_matrix[index][index+1] = set([rule.lhs() for rule in word_rules])
            backpointers[index][index+1].append([(index,index,index+1,rule.lhs(),word,None) for rule in word_rules])
        
    # cky_matrix
    all_rules = grammar.productions()

    for width in range(2,sentence_length+1):
        # print(width)
        for start in range(sentence_length - width + 1):
            end = start + width
            for mid in range(start + 1, end):
                for rule in all_rules:
                    if len(rule.rhs()) == 2:
                        B, C = rule.rhs()
                        if B in cky_matrix[start][mid] and C in cky_matrix[mid][end]:
                            cky_matrix[start][end].add(rule.lhs())
                            backpointers[start][end].append((start,mid,end,rule.lhs(),B,C))
                            # print(backpointers[start][end][rule.lhs()])
                            # try:
                            #     backpointers[start][end].append((start,mid,end,B,C))
                                
                            # except KeyError:
                            #     backpointers[start][end][rule.lhs()] = []
                            #     backpointers[start][end][rule.lhs()].append((start,mid,end,B,C))
                                
    start_symbol = grammar.start()

    print(start_symbol in cky_matrix[0][sentence_length])
                         
    terminal_list = [item for item in backpointers[0][sentence_length] if item[3] == start_symbol]
    
    if terminal_list == []:
        # print(f"{sentence} is not in the language of the CFG")
        return None
    else:                        
        end_list = set([(i,i+1) for i in range(sentence_length)])
        word_list = set([(i,i) for i in range(sentence_length)])
        all_trees = []

        for element in terminal_list:
            flag = True
            roots = [element]
            checked_list = []
            
            while flag:
                for root in roots:
                    # print(root)
                    if type(root) != str:
                        if root[:2] in word_list:
                            # print("oof")
                            checked_list.append(root[1:3])
                            # roots.append(root[4])
                            continue
                        elif (root[0],root[2]) in checked_list:
                            # print("oof2")
                            continue
                        else:
                            # print(f"getting children for {root}")
                            next_x, next_y = root[-2:]
                            checked_list.append((root[0],root[2]))
                            if root[:2] in end_list:
                                roots.append([x for x in backpointers[root[0]][root[1]][0] if x[3] == next_x][0])
                            else:
                                roots.append([x for x in backpointers[root[0]][root[1]] if x[3] == next_x][0])
                            if root[1:3] in end_list:
                                roots.append([y for y in backpointers[root[1]][root[2]][0] if y[3] == next_y][0])
                            else:
                                roots.append([y for y in backpointers[root[1]][root[2]] if y[3] == next_y][0])
                            
                            # print(roots)
                            # print(checked_list)
                            
                    # assert type(roots) == list
                        
                    final_list = [(root[0],root[2]) for root in roots]
                    # print("Checking")
                    flag = not(set(end_list) == set([value for value in final_list if value in end_list]))
                    
            all_trees.append(roots) 
               
        imp_info = [[(leaf[0],leaf[2],leaf[3]) for leaf in tree] for tree in all_trees]
        
        out_set = []
        for index in imp_info:
            branch_dict = form_tree(index)
            tree = build_tree(branch_dict,start_symbol)
            out_set.append(nltk.ImmutableTree.convert(tree=tree))
        
        return set(out_set)
        
        
def form_branch(node,node_list):
    """
    Form a branch in the parse tree given a node and the list of nodes.

    Args:
        node (tuple): Tuple representing the current node in the parse tree.
        node_list (List[tuple]): List of nodes representing the entire parse tree.

    Returns:
        tuple: A tuple containing information about the two children of the given node.
            The tuple format is (child1, child2, nltk.Tree).
    """
    a = node[0]
    c = node[1]
    # output_child1, output_child2 = 0, 0 
    candidate_children = [check_node for check_node in node_list if (check_node[0] == a or check_node[1] == c) and check_node != node]
    # print(candidate_children)
    for child1 in candidate_children:
        # print(child1)
        # x = child[0]
        common = child1[1]
        other_candidates = [x for x in candidate_children if x != child1 and x != node]
        for child2 in other_candidates:
            # print(child2)
            if common == child2[0]:
                output_child1 = child1
                output_child2 = child2
                                
                return output_child1[-1], output_child2[-1], nltk.Tree(node = str(node[-1]) , children = [str(output_child1[-1]),str(output_child2[-1])])
    # return output_child1, output_child2
    
def form_tree(node_list):
    """
    Form a parse tree from a list of nodes.

    Args:
        node_list (List[tuple]): List of nodes representing the entire parse tree.

    Returns:
        dict: A dictionary representing the parse tree structure with parent-child relationships.
    """
    end_list = set([(i,i+1) for i in range(sentence_length)])
    # start_node = [node for node in node_list if node[:2] == (0,sentence_length)][0]
    # print(start_node)
    checked_list = []
    parent_child = []
    for node in node_list:
        if node not in checked_list:
            # print(parent_child)
            # print(checked_list)
            # print(node)
            if node[:2] in end_list:
                checked_list.append(node)
                parent_child.append([node[-1],[sentence_glob[node[0]]]])
                # print("oof")
            else:
                child1, child2, _ = form_branch(node, node_list)
                checked_list.append(node)
                parent_child.append([node[-1],[child1,child2]])
            
    # print(parent_child)
    branch_dict = {}
    for branch in parent_child:
        branch_dict[branch[0]] = branch[-1]
    # print(branch_dict)
        
    return branch_dict

def build_tree(grammar_dict, start_symbol):
    """
    Build a parse tree from a dictionary representing the parse tree structure.

    Args:
        grammar_dict (dict): Dictionary representing the parse tree structure with parent-child relationships.
        start_symbol: Starting symbol of the parse tree.

    Returns:
        nltk.Tree: A parse tree represented using the nltk.Tree class.
    """
    if start_symbol not in grammar_dict:
        return start_symbol  # Terminal symbol

    children = grammar_dict[start_symbol]
    if len(children) == 1 and isinstance(children[0], str):
        return Tree(start_symbol, [children[0]])

    subtrees = [build_tree(grammar_dict, child) for child in children]
    return Tree(start_symbol, subtrees)

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