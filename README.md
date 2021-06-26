#8-puzzle

BFS, DFS, A* and IDA* 8-puzzle implementation

### Requirements

Only standard Python 3 libraries are needed

### Algorithms
```
bfs (Breadth-First Search)
dfs (Depth-First Search)
ast (A-Star Search)
ida (Iterative-Deepening-ΑStar Search)
```
### Usage
```
python solver.py [ALGO] [BOARD]
python solver.py bfs 0,7,6,8,5,4,3,2,1
```
### Results
```
caminho: ['direita', 'direita', 'baixo', 'baixo', 'esquerda', 'cima', 'cima', 'direita', 'baixo',
'baixo', 'esquerda', 'cima', 'esquerda', 'baixo', 'direita', 'cima', 'cima', 'esquerda', 'baixo',
'direita', 'cima', 'direita', 'baixo', 'baixo', 'esquerda', 'cima', 'esquerda', 'cima']

custo do caminho: 28

nós expandidos: 180338

dimensão de margem: 863

dimensão máxima de margem: 24048

profundidade de busca: 28

profundidade máxima de busca: 29

tempo de execução: 2.66646192

uso máximo de memória: 64.89600000
```
### Solvability
A 8-puzzle has  9! = 362880 possible states, but only half of these states (9!/2) = 181440 are solvable.

If an unsolvable state is entered:
```
python solver.py ast 1,8,2,0,4,3,5,6,7

sem solução possível
```
### Why is the code in Portuguese?
This was originally a college assignment. Maybe I will translate it in the future. Maybe.
