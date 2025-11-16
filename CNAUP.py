# 1. BUILDING ADT

class Building:
    def __init__(self, bid, name, location):
        self.id = bid
        self.name = name
        self.location = location

    def __repr__(self):
        return f"{self.id} - {self.name} ({self.location})"


# 2. SIMPLE BST

class BSTNode:
    def __init__(self, b):
        self.b = b
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, b):
        if self.root is None:
            self.root = BSTNode(b)
        else:
            self._insert(self.root, b)

    def _insert(self, node, b):
        if b.id < node.b.id:
            if node.left is None:
                node.left = BSTNode(b)
            else:
                self._insert(node.left, b)
        else:
            if node.right is None:
                node.right = BSTNode(b)
            else:
                self._insert(node.right, b)

    def inorder(self, node):
        if node:
            self.inorder(node.left)
            print(node.b)
            self.inorder(node.right)

    def preorder(self, node):
        if node:
            print(node.b)
            self.preorder(node.left)
            self.preorder(node.right)

    def postorder(self, node):
        if node:
            self.postorder(node.left)
            self.postorder(node.right)
            print(node.b)

    def height(self, node):
        if not node:
            return 0
        return 1 + max(self.height(node.left), self.height(node.right))


# 3. SIMPLE AVL TREE

class AVLNode:
    def __init__(self, b):
        self.b = b
        self.left = None
        self.right = None
        self.h = 1

class AVL:
    def __init__(self):
        self.root = None

    def height(self, n):
        return n.h if n else 0

    def get_balance(self, n):
        return self.height(n.left) - self.height(n.right)

    def right_rotate(self, y):
        x = y.left
        t = x.right
        x.right = y
        y.left = t
        y.h = 1 + max(self.height(y.left), self.height(y.right))
        x.h = 1 + max(self.height(x.left), self.height(x.right))
        return x

    def left_rotate(self, x):
        y = x.right
        t = y.left
        y.left = x
        x.right = t
        x.h = 1 + max(self.height(x.left), self.height(x.right))
        y.h = 1 + max(self.height(y.left), self.height(y.right))
        return y

    def insert(self, node, b):
        if node is None:
            return AVLNode(b)

        if b.id < node.b.id:
            node.left = self.insert(node.left, b)
        else:
            node.right = self.insert(node.right, b)

        node.h = 1 + max(self.height(node.left), self.height(node.right))
        balance = self.get_balance(node)

        if balance > 1 and b.id < node.left.b.id:
            return self.right_rotate(node)

        if balance < -1 and b.id > node.right.b.id:
            return self.left_rotate(node)

        if balance > 1 and b.id > node.left.b.id:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        if balance < -1 and b.id < node.right.b.id:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node


# 4. SIMPLE GRAPH (BFS + DFS)

from collections import deque

class Graph:
    def __init__(self):
        self.adj = {}

    def add_node(self, id):
        if id not in self.adj:
            self.adj[id] = []

    def add_edge(self, u, v):
        self.adj[u].append(v)
        self.adj[v].append(u)

    def bfs(self, start):
        q = deque([start])
        visited = set([start])
        print("BFS:", end=" ")
        while q:
            node = q.popleft()
            print(node, end=" ")
            for nei in self.adj[node]:
                if nei not in visited:
                    visited.add(nei)
                    q.append(nei)
        print()

    def dfs(self, start, visited=None):
        if visited is None:
            visited = set()
            print("DFS:", end=" ")

        print(start, end=" ")
        visited.add(start)

        for nei in self.adj[start]:
            if nei not in visited:
                self.dfs(nei, visited)
        print()


# 5. SIMPLE DIJKSTRA

import heapq

def dijkstra(graph, src):
    dist = {node: float('inf') for node in graph}
    dist[src] = 0
    pq = [(0, src)]

    while pq:
        d, node = heapq.heappop(pq)
        for nei, wt in graph[node]:
            if d + wt < dist[nei]:
                dist[nei] = d + wt
                heapq.heappush(pq, (dist[nei], nei))

    return dist


# 6. SIMPLE KRUSKAL MST

def find(par, x):
    if par[x] != x:
        par[x] = find(par, par[x])
    return par[x]

def union(par, rank, a, b):
    ra, rb = find(par, a), find(par, b)
    if ra != rb:
        if rank[ra] < rank[rb]:
            par[ra] = rb
        else:
            par[rb] = ra
            if rank[ra] == rank[rb]:
                rank[ra] += 1
        return True
    return False

def kruskal(edges, n):
    edges.sort()
    par = {i: i for i in range(n)}
    rank = {i: 0 for i in range(n)}
    mst = []

    for w, u, v in edges:
        if union(par, rank, u, v):
            mst.append((u, v, w))

    return mst


# 7. SIMPLE EXPRESSION TREE

class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def build_expr(postfix):
    stack = []
    for x in postfix:
        if x not in "+-*/":
            stack.append(Node(float(x)))
        else:
            n = Node(x)
            n.right = stack.pop()
            n.left = stack.pop()
            stack.append(n)
    return stack[0]

def eval_expr(node):
    if node.left is None:
        return node.val
    a = eval_expr(node.left)
    b = eval_expr(node.right)
    if node.val == "+": return a + b
    if node.val == "-": return a - b
    if node.val == "*": return a * b
    if node.val == "/": return a / b

