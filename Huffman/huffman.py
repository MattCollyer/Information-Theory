from graphviz import Graph
import math



def get_bits(filename = 'entropy/stream2.txt'):
  bits = []
  with open (filename) as file:
    for line in file:
      for bit in line:
        if(bit == "0" or bit == '1'):
          bits.append(bit)
  return bits



def pairs(bits):
  pairs = []
  [pairs.append(bits[i] + bits[i+1]) for i in range(int(len(bits)/2))]
  return pairs


def txt_to_list(filename, ignore_chars):
  txt = []
  with open (filename) as file:
    for line in file:
      for char in line:
        if(char not in ignore_chars):
          txt.append(char)
  return txt

def string2list(string):
  txt = []
  for char in string:
    txt.append(char)
  return txt


def analyze(text):
  ##Accepts list of strings, assumes strings to be one "character"
  #Returns dictionary of all used elements with their count.(probability?)
  total = len(text)
  dictionary = {}
  for elem in text:
    if(elem not in dictionary):
      dictionary[elem] = 1
    else:
      dictionary[elem] += 1
  return [(dictionary[elem]/total, elem) for elem in dictionary]


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


def build_huffman_tree(probabilities):
  nodes = NodeQueue(probabilities)
  while (nodes.len() > 1):
    parent = TreeNode()
    parent.adopt(left = nodes.pop(), right = nodes.pop())
    nodes.push(parent)
  return nodes.pop()
  

def calculate_entropy(probabilities):
  source = 0
  for elem in probabilities:
    source += -(elem[0]) * math.log(elem[0], 2)
  return source


def percent_decrease(original, new):
  return round( ((original - new) /original) * 100, 2)

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




if (__name__ == '__main__'):
  filename = '../texts/dune.txt'
  ignore_chars = ['1', '2', '3', '4', '5','6','7','8','9','0','\n']
  all_chars = txt_to_list(filename, ignore_chars)
  summary('Dune',all_chars, graph=True, export_codex=True)

