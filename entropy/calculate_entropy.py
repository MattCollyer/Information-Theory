'''
A quick script that will spit out entropy total as we go along the text.
just 4 fun

'''
import math 
import matplotlib.pyplot as plt
import numpy as np



def split_bits(stream, size = 8):
  return [stream[size*i:size*(i+1)] for i in range(len(stream)//size)]


def calculate_entropy(stream, dictionary, distance):
  source_entropy = 0
  for elem in dictionary:
    probability = dictionary[elem]/distance
    source_entropy += -(probability) * math.log(probability, 2)
  return source_entropy

def graph(x_len, Y):
  x = np.linspace(0, 1, x_len)
  plt.plot(x,Y, 'g')
  # plt.scatter(X,Y)
  plt.show()


dictionary = {}
entropy = 0
so_far = ''
distance = 0
# source = '01000001010000100100001101000100010001010100011001000111'
source = '0110100001100101011011000110110001101111001000000100100100100000011000010110110100100000011010100111010101110011011101000010000001100001001000000110110101100001011011100010110000100000011010000110111101110111011001010111011001100101011100100010000001001001001000000110000101101101001000000111001101100101011100100110100101101111011101010111001101101100011110010010000001101001011011100111010001100101011100100110010101110011011101000110010101100100001000000110100101101110001000000111001101100101011001010110100101101110011001110010000001101000011011110111011100100000011101000110100001100101001000000110010101101110011101000111001001101111011100000111100100100000011100100110010101100001011000110110100001100101011100110010000001100001001000000111001101110100011000010110001001101100011001010010000001110000011011110110100101101110011101000010000000101101001000000110000101110100001000000111011101101000011000010111010000100000011100000110111101101001011011100111010000100000011001000110111100100000011110010110111101110101001000000111010001101000011010010110111001101011001000000110100101110100001000000111011101101001011011000110110000100000011000100110010100111111'
# source = '01000001010000010100000101000001010000010100000101000001'
source = split_bits(source)
entropy_snapshots = []
for elem in source:
  distance += 1
  so_far += elem
  if(elem not in dictionary):
    dictionary[elem] = 1
  else:
    dictionary[elem] += 1
  entropy_snapshots.append(calculate_entropy(so_far, dictionary, distance))
graph(len(source),entropy_snapshots)

