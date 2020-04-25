# coding: utf-8

import sys
from graphviz import Graph

G = Graph(format='png', filename='formation_tree')
G.attr('node', shape='box')
not_wff = False


class Node:
    def __init__(self, root=None):
        self.value = root
        self.left = None
        self.right = None
        self.id = None

    def left_append(self, x):
        self.left = Node(x)

    def right_append(self, y):
        self.right = Node(y)


def not_parsing(node):
    global not_wff

    if len(node.value) == 4 and node.value[2] == 'A' and node.value[3] == ')':
        node.left_append(['A'])
        node.left.id = node.id + '1'
        G.node(node.left.id, ' '.join(node.left.value))
        G.edge(node.id, node.left.id)
        return

    ind = -1

    while True:
        left = 0
        right = 0
        for i in range(2, len(node.value) - 1):
            if node.value[i] == '(':
                left += 1
            elif node.value[i] == ')':
                right += 1

            if left != 0 and left == right:
                ind = i
                break
            elif (i == len(node.value) - 2 and left != right) or left == right == 0:
                print('これは整式ではありません')
                not_wff = True
                return

        node.left_append(node.value[2:ind + 1])
        node.left.id = node.id + '1'
        G.node(node.left.id, ' '.join(node.left.value))
        G.edge(node.id, node.left.id)

        return


def binary_parsing(node):
    global not_wff

    if len(node.value) == 5 and node.value[1] == 'A' and node.value[2] in ['and', 'or', '=>', '<=>'] \
            and node.value[3] == 'A' and node.value[4] == ')':
        node.left_append(['A'])
        node.right_append(['A'])
        node.left.id = node.id + '1'
        G.node(node.left.id, ' '.join(node.left.value))
        node.right.id = node.id + '2'
        G.node(node.right.id, ' '.join(node.right.value))
        G.edge(node.id, node.left.id)
        G.edge(node.id, node.right.id)
        return

    if node.value[1] != '(' and node.value[1] != 'A':
        print('これは整式ではありません')
        not_wff = True
        return

    ind = -1

    if node.value[1] == 'A':
        left_half = ['A']
        ind = 1
    else:
        while True:
            left = 0
            right = 0
            for i in range(1, len(node.value) - 1):
                if node.value[i] == '(':
                    left += 1
                elif node.value[i] == ')':
                    right += 1

                if left != 0 and left == right:
                    ind = i
                    break
                elif (i == len(node.value) - 2 and left != right) or left == right == 0:
                    print('これは整式ではありません')
                    not_wff = True
                    return

            left_half = node.value[1:ind + 1]
            break

    if not node.value[ind + 1] in ['and', 'or', '=>', '<=>']:
        print('これは整式ではありません')
        not_wff = True
        return

    try:
        if node.value[ind + 2] == 'A' and node.value[ind + 3] == ')' and len(node.value) == ind + 4:
            right_half = ['A']
            node.left_append(left_half)
            node.right_append(right_half)
            node.left.id = node.id + '1'
            G.node(node.left.id, ' '.join(node.left.value))
            node.right.id = node.id + '2'
            G.node(node.right.id, ' '.join(node.right.value))
            G.edge(node.id, node.left.id)
            G.edge(node.id, node.right.id)
            return
    except IndexError:
        pass

    while True:
        left = 0
        right = 0
        for i in range(ind + 2, len(node.value) - 1):
            if node.value[i] == '(':
                left += 1
            elif node.value[i] == ')':
                right += 1

            if left != 0 and left == right:
                break
            elif (i == len(node.value) - 2 and left != right) or left == right == 0:
                print('これは整式ではありません')
                not_wff = True
                return

        right_half = node.value[ind + 2:len(node.value) - 1]
        break

    node.left_append(left_half)
    node.right_append(right_half)
    node.left.id = node.id + '1'
    G.node(node.left.id, ' '.join(node.left.value))
    node.right.id = node.id + '2'
    G.node(node.right.id, ' '.join(node.right.value))
    G.edge(node.id, node.left.id)
    G.edge(node.id, node.right.id)
    return

if __name__ == '__main__':
    formula = Node([i for i in input('整式かどうか判定したい文字列を入力してください').split()])
    formula.id = '0'
    vertices = [formula]
    new_vertices = []
    G.node(formula.id, ' '.join(formula.value))

    try:
        while True:
            end = True
            times = 0

            for i in vertices:
                if i.value != ['A']:
                    end = False

            if end:
                print('これは整式です')
                G.view()
                break

            for i in vertices:
                if i.value[0] != '(' and i.value != ['A']:
                    sys.exit()

                if i.value != ['A'] and i.value[1] == 'not':
                    not_parsing(i)
                    new_vertices.append(i.left)
                elif i.value != ['A']:
                    binary_parsing(i)
                    new_vertices.append(i.left)
                    new_vertices.append(i.right)

                if not_wff:
                    break

            if not_wff:
                break

            vertices = new_vertices
            new_vertices = []

    except IndexError:
        print('これは整式ではありません')
