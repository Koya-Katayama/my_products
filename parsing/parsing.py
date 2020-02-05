# coding: utf-8

import sys
from graphviz import Graph

G = Graph(format = 'png', filename = 'formationtree')
G.attr('node', shape = 'box')
no = False

class Node():
    def __init__(self, root = None):
        self.value = root
        self.left = None
        self.right = None
        self.id = None
    
    def lappend(self, x):
        self.left = Node(x)
    
    def rappend(self, y):
        self.right = Node(y)
        

def notparsing(node):
    global no
    if len(node.value) == 4 and node.value[2] == 'A' and node.value[3] == ')':
        node.lappend(['A'])
        node.left.id = node.id + '1'
        G.node(node.left.id, ' '.join(node.left.value))
        G.edge(node.id, node.left.id)
        return
    
    flag = True
    exind = -1
    
    while flag == True:   
        left = 0
        right = 0
        for i in range(2, len(node.value) - 1):
            if node.value[i] == '(':
                left += 1
            elif node.value[i] == ')':
                right += 1
                        
            if left != 0 and left == right:
                exind = i
                flag = False
                break
            elif (i == len(node.value) - 2 and  left != right) or left == right == 0:
                print('これは整式ではありません')
                no = True
                return
    
                        
        node.lappend(node.value[2:exind+1])
        node.left.id = node.id + '1'
        G.node(node.left.id, ' '.join(node.left.value))
        G.edge(node.id, node.left.id)
        
        return
    
            
def binaryparsing(node):
    global no
    
    if len(node.value) == 5 and node.value[1] == 'A' and node.value[2] in ['and','or','=>','<=>'] \
    and node.value[3] == 'A' and node.value[4] == ')':
        node.lappend(['A'])
        node.rappend(['A'])
        node.left.id = node.id + '1'
        G.node(node.left.id, ' '.join(node.left.value))
        node.right.id = node.id + '2'
        G.node(node.right.id, ' '.join(node.right.value))
        G.edge(node.id, node.left.id)
        G.edge(node.id, node.right.id)
        return
    
    if node.value[1] != '(' and node.value[1] != 'A':
        print('これは整式ではありません')
        no = True
        return
    
    flag = True
    exind = -1
    lefthalf = None
    righthalf = None
    
    if node.value[1] == 'A':
        lefthalf = ['A']
        exind = 1
    else:
        while flag == True:   
            left = 0
            right = 0
            for i in range(1, len(node.value) - 1):
                if node.value[i] == '(':
                    left += 1
                elif node.value[i] == ')':
                    right += 1
                        
                if left != 0 and left == right:
                    exind = i
                    flag = False
                    break
                elif (i == len(node.value) - 2 and  left != right) or left == right == 0:
                    print('これは整式ではありません')
                    no = True
                    return
                        
            lefthalf = node.value[1:exind+1]
            break
        
    if not node.value[exind+1] in ['and','or','=>','<=>']:
        print('これは整式ではありません')
        no = True
        return
    
    flag = True
    
    try:
        if node.value[exind+2] == 'A' and node.value[exind+3] == ')' and len(node.value) == exind+4:
            righthalf = ['A']
            node.lappend(lefthalf)
            node.rappend(righthalf)
            node.left.id = node.id + '1'
            G.node(node.left.id, ' '.join(node.left.value))
            node.right.id = node.id + '2'
            G.node(node.right.id, ' '.join(node.right.value))
            G.edge(node.id, node.left.id)
            G.edge(node.id, node.right.id)
            return
    except:
        pass
            
    while flag == True:   
        left = 0
        right = 0
        for i in range(exind + 2, len(node.value) - 1):
            if node.value[i] == '(':
                left += 1
            elif node.value[i] == ')':
                right += 1
                        
            if left != 0 and left == right:
                flag = False
                break
            elif (i == len(node.value) - 2 and  left != right) or left == right == 0:
                print('これは整式ではありません')
                no = True
                return
                
        righthalf = node.value[exind+2:len(node.value)-1]
        break
    
    node.lappend(lefthalf)
    node.rappend(righthalf)
    node.left.id = node.id + '1'
    G.node(node.left.id, ' '.join(node.left.value))
    node.right.id = node.id + '2'
    G.node(node.right.id, ' '.join(node.right.value))
    G.edge(node.id, node.left.id)
    G.edge(node.id, node.right.id)
    return
    
fomula = Node([i for i in input('整式かどうか判定したい文字列を入力してください').split()])
fomula.id = '0'
vertices = [fomula]
newvertices = []
G.node(fomula.id, " ".join(fomula.value))

try:
    while True:
        end = True
        times = 0
    
        for i in vertices:
            if i.value != ['A']:
                end = False

        if end == True:
            print('これは整式です')
            G.view()
            break
    
        for i in vertices:
            if i.value[0] != '(' and i.value != ['A']:
                sys.exit()
        
            if i.value != ['A'] and i.value[1] == 'not':
                notparsing(i)
                newvertices.append(i.left)
            elif i.value != ['A']:
                binaryparsing(i)
                newvertices.append(i.left)
                newvertices.append(i.right)
            
            if no == True:
                break
    
        if no == True:
            break
            
        vertices = newvertices
        newvertices = []

except:
    print('これは整式ではありません')
