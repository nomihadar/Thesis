import sys, os
import re
from ete3 import Tree

sys.path.append(os.path.dirname(sys.path[0]))

def reformat_num(number):
    num = float(number)
    reformatted_num = str("{0:.10f}".format(num))
    return reformatted_num


def reformat_branch(branch):
    fixed_branch = branch[0] + ":" + branch[1:]
    return fixed_branch


def read_tree(tree_path):
    tree_file = open(tree_path, 'r')
    tree_str = tree_file.read()
    tree_file.close()

    return tree_str


def rescale_branches(tree):
    tree_obj = Tree(tree)
    tree = tree_obj.write(format=1)

    tree_str_1 = tree
    tree_str_2 = ''
    current_tree = 1

    comb_branch = '\)[0-9]+\.[0-9]+'
    comb_branch_pattern = re.compile(comb_branch)
    for branch in re.findall(comb_branch_pattern, tree_str_1):
        reformatted_branch = reformat_branch(branch)
        if current_tree == 1:
            tree_str_2 = re.sub(re.escape(branch), reformatted_branch, tree_str_1)
            current_tree = 2
        else:
            tree_str_1 = re.sub(re.escape(branch), reformatted_branch, tree_str_2)
            current_tree = 1

    if current_tree == 1:
        tree_str_3 = tree_str_1
    else:
        tree_str_3 = tree_str_2

    # reformat small numbers
    reformatted_number = re.compile(r'\d+[\.\d+]*e\-\d+')
    tree_str_4 = tree_str_3
    tree_str_5 = ''
    current_tree = 4

    for number in reformatted_number.findall(tree_str_1):
        # print("number: " + number) #debug!!
        reformatted_num = reformat_num(number)
        # print("reformatted_num: " + reformatted_num) #debug!!
        if current_tree == 4:
            # print("tree before replacement: " + tree_str_4) #debug!!
            tree_str_5 = tree_str_4.replace(number, reformatted_num, 1)
            current_tree = 5
        # print("tree after replacement: " + tree_str_5) #debug!!
        else:
            # print("tree before replacement: " + tree_str_5) #debug!!
            tree_str_4 = tree_str_5.replace(number, reformatted_num, 1)
            current_tree = 4
        # print("tree after replacement: " + tree_str_4) #debug!!

    tree_str_6 = ""
    if current_tree == 4:
        tree_str_6 = tree_str_4
    else:
        tree_str_6 = tree_str_5

    # remove bootsrap numbers
    bootsrap_num_expr = re.compile(r"-{0,1}[0-9]+\.[0-9]+:")
    fixed_tree_str = bootsrap_num_expr.sub("", tree_str_6)

    return fixed_tree_str


def write_adjusted_tree(fixed_tree_str):
    with open("adjusted_tree.nw", "w") as f:
        f.write(fixed_tree_str)
        f.write("\n")


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print ("please insert argument")
        sys.exit(0)

    # get a path to file of list of paths to MSAs files
    tree_path = sys.argv[1]

    tree = read_tree(tree_path)

    fixed_tree_str = fix_tree(tree)

    write_adjusted_tree(fixed_tree_str)
