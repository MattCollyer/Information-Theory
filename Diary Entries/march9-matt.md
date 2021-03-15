

##Hello Hello

This has been a fun week. Generating this huffman tree was enjoyable.

That being said, I haven't had the time to fully figure out getting this as a jupyter notebook, 
so bear with me as I post the code here (also is attached)

Took me a while to figure out just how the hell to do this, but I got it all worked out.


I have many helper functions which I won't go over, but the bulk of the work is in all of this:


```

class TreeNode:
  def __init__(self, symbol = '', value = 0, parent = None, left = None, right = None):
    self.symbol = symbol
    self.value = value
    self.parent = parent
    self.left = left
    self.right = right

  def adopt(self, left, right):
    self.left = left
    self.right = right
    for child in [left, right]:
      if child: 
        child.parent = self
    self.value = self.left.value + self.right.value

  def graph(self, dot):
    #Graphs a possible tree with self as root
    if(self.left):
      self.left.graph(dot)
    if(self.right):
      self.right.graph(dot)
    label = self.symbol if self.symbol else str(round(self.value, 8))
    dot.node(str(id(self)), label = label)
    if(self.parent):
      dot.edge(str(id(self)), str(id(self.parent)))

  def make_graph(self, text_name):
    dot = Graph()
    self.graph(dot)
    dot.render('graphviz/'+text_name+'_huffman', view=True)  

  def find_code(self, codex, code):
    if(self.left):
      self.left.find_code(codex, code + '0')
    if(self.right):
      self.right.find_code(codex, code + '1')
    if(self.symbol != ''):
      codex.append({'Symbol': self.symbol, 'Probability': self.value, 'Huffman Code': code})
  
  def make_code(self):
    codex = []
    self.find_code(codex, '')
    codex.sort(key = lambda x: len(x['Huffman Code']))
    return codex


```
The above code is rather simple, it makes a node object which will act as a node in our tree, which we'll create later. 
Each node has a symbol (the particular character or word), and a value (its corresponding probability).
There are methods which can create a graph or a code using the node as a root.



Below we have a type of priority queue, which holds individual nodes. It just ensures that it is always ordered with the least probable node at the top.

```

class NodeQueue:
  def __init__(self, probabilities = []):
    self.nodes = []
    for pair in probabilities:
      self.nodes.append(TreeNode(symbol = pair[1], value = pair[0]))
  
  def push(self, node):
    self.nodes.append(node)
    self.sort()
  
  def sort(self):
    self.nodes.sort(key = lambda x: x.value, reverse = True)

  def pop(self):
    return self.nodes.pop()
  def len(self):
    return len(self.nodes)
    
```


This code builds the tree, and returns the root node.

```

def build_huffman_tree(probabilities):
  nodes = NodeQueue(probabilities)
  while (nodes.len() > 1):
    parent = TreeNode()
    parent.adopt(left = nodes.pop(), right = nodes.pop())
    nodes.push(parent)
  return nodes.pop()

```

The code below acts as a master function. It only requires the name of the text and all the characters in a list format.
It spits out a summary everything, and can optionally make a graph or a codex.


```

def summary(text_name, chars, graph = False, export_codex = False):

  original_size = len(all_chars)
  original_bit_length = original_size * 8 #ASSUMES ASCII. PERHAPS MAKE THIS DYNAMIC W/ OPTIONAL PARAM
  probability_queue = analyze(all_chars)
  #Build Huffman, make graph if desired. 
  root = build_huffman_tree(probability_queue)
  if(graph):
    root.make_graph(text_name)

  codex = root.make_code()

  #Calculate how many bits would be used with this text & codex
  new_size = 0
  for row in codex:
    new_size += (row['Probability']* original_size )* len(row['Huffman Code'])

  print('\n\n\n-------------------------------------')
  print("Text:",text_name)
  print("Original Source Entropy:", calculate_entropy(probability_queue))
  print("Amount of bits in ASCII:", original_bit_length)
  print("Amount of bits in Huffman :", int(new_size))
  print("With this codex, the original text can be shrunk by ", percent_decrease(original_bit_length, new_size), 'percent')
  print('-------------------------------------\n\n\n')

  if(export_codex):
    with open(text_name+'_codex.txt', 'w') as file:
      for row in codex:
        for key in row:
          file.write(key+' '+str(row[key])+' ')
        file.write('\n')


```







##Lets see how it works:


Using Jim's Wandering Inn text as a reference:

Output:

```
-------------------------------------
Text: Wandering inn
Original Source Entropy: 4.166746762972305
Amount of bits in ASCII: 2584
Amount of bits in Huffman : 1360
With this codex, the original text can be shrunk by  47.37 percent
-------------------------------------
```

Generated this codex and this graph


I also have been reading the Dune series, so I figured it would be cool to send in the entire first book:

```
Output:
-------------------------------------
Text: Dune
Original Source Entropy: 4.4641152985469885
Amount of bits in ASCII: 9235664
Amount of bits in Huffman : 5198643
With this codex, the original text can be shrunk by  43.71 percent
-------------------------------------
```

Generated this codex and this graph



