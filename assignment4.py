import argparse
import random
import nltk

from nltk.tree import Tree
from nltk.treeprettyprinter import TreePrettyPrinter
from model.recognizer import recognize
from model.parser import parse
# from nltk.draw.tree import draw_trees


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
        sentence1 = "Simone caught the butterfly by the bush."
        sentence2 = "The child looked at the lady using the magnifying glass."

        print(f"First sentence : {sentence1} \n")
        sentence1_structure1 = "\
            (S  (NP (N Simone))\
                    (VP (V caught)\
                        (NP (Det the)\
                            (N butterfly))\
                        (PP (P by)\
                            (NP (Det the)\
                                (N bush))\
                            )\
                    )\
            )"
        tree1 = Tree.fromstring(sentence1_structure1)
        print(TreePrettyPrinter(tree1).text())
        print("\nMeaning : Simone caught the butterfly that was fluttering near the bush \n")
        sentence1_structure2 = "\
            (S\
                (VP (NP (N Simone))\
                    (VP (V caught))\
                    (NP (Det the)\
                        (N butterfly)))\
                (PP (P by)\
                    (NP (Det the)\
                        (N bush))\
                )\
            )"
                                
        tree2 = Tree.fromstring(sentence1_structure2)
        print(TreePrettyPrinter(tree2).text())
        print("\nMeaning : Simone caught the butterfly while she was next to the bush \n")
        
        print(f"Second sentence : {sentence2} \n")
        sentence2_structure1 = "\
            (S\
                (CP (TP (NP (Det the)\
                                (N child))\
                            (VP (V looked)\
                                (PP (P at)\
                                    (NP (Det the)\
                                        (N lady))))))\
                    (VP (V using)\
                        (NP (Det the)\
                            (Adj magnifying)\
                            (N glass)))\
            )"
            
        tree3 = Tree.fromstring(sentence2_structure1)
        print(TreePrettyPrinter(tree3).text())
        print("\nMeaning : The child is looking at the lady while using a magnifying glass \n")
        sentence2_structure2 = "\
            (S\
                (VP (NP (Det the)\
                            (N child))\
                            (V looked))\
                (PP (PP (P at)\
                        (NP (Det the)\
                            (N lady)))\
                    (VP (V using)\
                        (NP (Det the)\
                            (Adj magnifying)\
                            (N glass))))\
            )"
            
        tree4 = Tree.fromstring(sentence2_structure2)
        print(TreePrettyPrinter(tree4).text())
        print("\nMeaning : The child is looking at the lady who is using a magnifying glass \n")
        
        with open("./output/structural_ambiguity.txt", "w", newline="") as file:
            file.write(f"First sentence : {sentence1} \n")
            file.write(TreePrettyPrinter(tree1).text())
            file.write("\nMeaning : Simone caught the butterfly that was fluttering near the bush \n")
            file.write(TreePrettyPrinter(tree2).text())
            file.write("\nMeaning : Simone caught the butterfly while she was next to the bush \n")
            file.write(TreePrettyPrinter(tree3).text())
            file.write("\nMeaning : The child is looking at the lady while using a magnifying glass \n")
            file.write(TreePrettyPrinter(tree4).text())
            file.write("\nMeaning : The child is looking at the lady who is using a magnifying glass \n")
            
    
    elif args.recognizer:
        no_parse = [t[index][0] for index in range(len(t)) if t[index][1] == 0 and len(t[index][0]) <= 9]
        yes_parse = [t[index][0] for index in range(len(t)) if t[index][1] != 0 and len(t[index][0]) <= 7]
        
        random.seed(42)
        grammatical = random.sample(yes_parse,10)
        ungrammatical = random.sample(no_parse,10)
        with open("./output/recognizer.txt", "w", newline = "") as file:
            for sents in grammatical:
                print(f"Sentence : {' '.join(sents)}")
                file.write(f"Sentence : {' '.join(sents)}\n")
                val = recognize(grammar, sents)
                if val:
                    print(f"`{' '.join(sents)}` is in the language of CFG.")
                    file.write(f"`{' '.join(sents)}` is in the language of CFG.\n")
                else:
                    print(f"`{' '.join(sents)}` is not in the language of CFG.")
                    file.write(f"`{' '.join(sents)}` is not in the language of CFG.\n")

            for sents in ungrammatical:
                print(f"Sentence : {' '.join(sents)}")
                file.write(f"Sentence : {' '.join(sents)}\n")
                val = recognize(grammar, sents)
                if val:
                    print(f"`{' '.join(sents)}` is in the language of CFG.")
                    file.write(f"`{' '.join(sents)}` is in the language of CFG.\n")
                else:
                    print(f"`{' '.join(sents)}` is not in the language of CFG.")
                    file.write(f"`{' '.join(sents)}` is not in the language of CFG.\n")

    elif args.parser:
        with open("./output/parser.txt", "w", newline = "") as file:
        # We test the parser by using ATIS test sentences.
            print("ID\t Predicted_Tree\tLabeled_Tree")
            file.write("ID\t Predicted_Tree\tLabeled_Tree\n")
            for idx, sents in enumerate(t):
                print(f"Sentence : {' '.join(sents[0])}")
                file.write(f"Sentence : {' '.join(sents[0])}\n")
                tree = parse(grammar, sents[0])
                if tree is None:
                    print(f"{idx}\t 0\t \t{sents[1]}")
                    print(f"{' '.join(sents[0])} is not in the language of the CFG")
                    file.write(f"{idx}\t 0\t \t{sents[1]}\n")
                    file.write(f"{' '.join(sents[0])} is not in the language of the CFG\n")
                else:
                    print(f"{idx}\t {len(tree)}\t \t{sents[1]}\n")
                    file.write(f"{idx}\t {len(tree)}\t \t{sents[1]}\n")

            yes_parse_l5 = [t[index][0] for index in range(len(t)) if t[index][1] != 0 and len(t[index][0]) < 5]
            sentence = random.sample(yes_parse_l5,1)[0]
            
            print(f"Sentence : {' '.join(sentence)}")
            file.write(f"Sentence : {' '.join(sentence)}\n")
            trees = parse(grammar,sentence)
            for tree in trees:
                print(TreePrettyPrinter(Tree.fromstring(tree.pformat().replace("\n",""))).text())
                file.write(TreePrettyPrinter(Tree.fromstring(tree.pformat().replace("\n",""))).text())
            

    elif args.count:
        print("Counting")
        print("count not implemented")
        # print("ID\t Predicted_Tree\tLabeled_Tree")
        # for idx, sents in enumerate(t):
        #     num_tree = count(grammar, sents[0])
        #     print("{}\t {}\t \t{}".format(idx, num_tree, sents[1]))


if __name__ == "__main__":
    main()
