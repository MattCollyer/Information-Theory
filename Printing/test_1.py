
import numpy as np
import matplotlib.pyplot as plt
import math 
import bezier

def stream_to_bytes(stream):
  return [stream[i:i+8] for i in range(0, len(stream))]

def hex_to_bin(stream):
  bin_stream = []
  hex_stream = [stream[i:i+2] for i in range(0, len(stream))]
  for hex in hex_stream:
    i = int(hex, 16)
    bin_stream.append('{:0{length}b}'.format(i, length = 8))
  return bin_stream



def bezier_curve(p1, p2, p3):
  nodes = np.array([
                    [p1[0], p2[0], p3[0]],
                    [p1[1], p2[1], p3[1]]
  ])
  b = bezier.Curve(nodes, degree = 2)
  return b



def graph(X,Y):
  plt.plot(X,Y)
  plt.show()






def get_bezier(p1,p2,p3,X,Y):
  b = bezier_curve(p1,p2,p3)
  small = float(min([p1[0], p3[0]]))
  large = float(max([p1[0], p3[0]]))
  s = np.linspace(small, large, 100)
  curve = b.evaluate_multi(s)
  for i in range(len(curve[0])):
    if(curve[0][i] > small and curve[0][i] < large):
      X.append(curve[0][i])
      Y.append(curve[1][i])
  





def test_bezier():
  p1 = [1, 0]
  p2 = [0, -3]
  p3 = [-1, 0]
  X = []
  Y = []
  get_bezier(p1,p2,p3,X,Y)
  graph(X,Y)

def draw_byte(byte, X, Y):
  r = 4
  arc_chunk = 360 / len(byte)
  arcs = [(arc_chunk * i, arc_chunk * (i+1)) for i in range(len(byte))]
  offset = 1
  print(byte)
  for i in range(len(byte)):
    if(byte[i] == '1'):
        x1 = r * math.cos(math.radians(arcs[i][0]))
        y1 = r * math.sin(math.radians(arcs[i][0]))
        mid_x = r * math.cos(math.radians((arcs[i][0] + (arcs[i][1]-arcs[i][0])/2)))
        mid_y = r * math.sin(math.radians((arcs[i][0] + (arcs[i][1]-arcs[i][0])/2)))
        x2 = r * math.cos(math.radians(arcs[i][1]))
        y2 = r * math.sin(math.radians(arcs[i][1]))
        stretch_x = offset * math.cos(math.atan(mid_y/mid_x)) + mid_x
        stretch_y = offset * math.sin(math.atan(mid_y/mid_x)) + mid_y
        p1 = np.array([x1,y1])
        p2 = np.array([stretch_x, stretch_y])
        p3 = np.array([x2, y2])
    #     get_bezier(p1,p2,p3,X,Y)
        X.append(x1)
        X.append(stretch_x)
        X.append(x2)
        Y.append(y1)
        Y.append(stretch_y)
        Y.append(y2)
    else:
      thetas = [0.25 * i for i in range(int(arcs[i][0]*4), int(arcs[i][1]*4))]
      for theta in thetas:
        X.append(r * math.cos(math.radians(theta)))
        Y.append(r * math.sin(math.radians(theta)))
  graph(X,Y)
  return X, Y



def get_paths(byte_stream):
  layer_height = 0.25
  layers = []
  layer_offset = 0
  for byte in byte_stream:
    layer_offset += layer_height
    X = []
    Y = []
    draw_byte(byte, X, Y)
    Z = [layer_offset for i in range(len(X))]
    layers.append(np.array((X,Y,Z)))


if __name__ == '__main__':
  stream = 'ffffffffffff3c22fb553740080600010800060400013c22fb5537400a0af8540000000000000a0af92a'
  reply = '3c22fb553740e6cb7c252a1108060001080006040002e6cb7c252a110a0af92a3c22fb5537400a0af854000000000000000000000000000000000000'
  bstream = hex_to_bin(stream)
  # get_paths(bstream)
  X = []
  Y = []
  # draw_byte(bstream[3],X,Y)
  # graph(X,Y)
  get_paths(bstream)
  # test_bezier()