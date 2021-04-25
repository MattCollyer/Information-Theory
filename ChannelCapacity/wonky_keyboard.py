'''
Problem 5.17 page 87 of Biggs

A simplified keypad has four keys 
arranged in two rows of two. If the intention is to press key x, 
there is probability f of pressing the other key in the same row 
and probability f of pressing the other key in the same column 
(and consequently probability 1 − 2f of pressing x). Write down 
the channel matrix for this situation and find its capacity 
(i.e. the maximum entropy, or information per symbol, that can 
be sent with this keyboard).

matthewcollyer@bennington.edu
'''

import math 
import numpy as np



'''

our keyboard is:

a  b
c  d

The 4 x 4 matrix is

P(y=a|x=a)  P(y=b|x=a)  P(y=c|x=a)  P(y=d|x=a)
P(y=a|x=b)  P(y=b|x=b)  P(y=c|x=b)  P(y=d|x=b)
P(y=a|x=c)  P(y=b|x=c)  P(y=c|x=c)  P(y=d|x=c)
P(y=a|x=d)  P(y=b|x=d)  P(y=c|x=d)  P(y=d|x=d)

We know that pressing the key correctly is p = 1 - 2f, so our diagonal will be that.
Likewise, their is a p = 0 chance of hitting a key not on the row or column, so the other diagonal will be zeros.
The remaining fields are keys adjacent to our intended key -- so they are p = f

1 - 2f    f     f    0
f     1 - 2f   0    f
f     0    1 - 2f   f
0    f     f   1 - 2f



This channel is symmmetric. We know then that the capacity must be at its max when each key is equally probable -- 1/4.



'''

def entropy(p):
  return p * math.log((1/p),2)


def H(probabilities):
  #TODO value checking

  probabilities = probabilities[probabilities != 0]
  entropies = [entropy(p) for p in probabilities]
  return sum(entropies)

def pxy(px,f):
  return np.array(([(1-2*f)*px[0], f*px[0], f*px[0], 0],
           [f*px[1], (1-2*f)*px[1], 0, f*px[1]],
           [f*px[2], 0, (1-2*f)*px[2], f*px[2]],
           [0, f*px[3], f*px[3], (1-2*f)*px[3]]))

if __name__ == '__main__':
  px = np.array(([0.25, 0.25, 0.25, 0.25]))
  py = np.array(([0.25, 0.25, 0.25, 0.25]))
  f = 0.1
  p_xy = pxy(px, f)
  print(H(p_xy))