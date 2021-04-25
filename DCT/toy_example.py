import matplotlib.pyplot as plt
import numpy as np
import math

"""
Matt Collyer, DCT Toy exmaple <matthewcollyer@bennington.edu>
DCT toy image example
Jim Mahoney. https://cs.bennington.college/courses/spring2021/jims_tutorials/info_theory/linear_algebra/four_by_four.html
"""

def get_ij_basis_image(i,j, dct_basis):
  return np.outer(dct_basis[i,:], dct_basis[j,:])

def flatten(x):
  return x.flatten()

def flatdot(x, y):
  return np.dot(flatten(x), flatten(y))

def generate_dct_basis_images(N):
  # """
  # Takes a dimmension 
  # Returns numpy DCT basis matrix.
  # """
  dct = np.zeros((N,N))
  for i in range(N):
      dct[0,i] = math.sqrt(2.0/N) / math.sqrt(2.0)
  for i in range(1,N):
    for j in range(N):
      dct[i,j] = math.sqrt(2.0/N) * math.cos((math.pi/N) * i *(j + 0.5))
  return dct

def generate_toy_dct_basis():
  half = 1/2
  sqrt2 = 1/math.sqrt(2)
  dct = np.array([[half, half, half, half],
              [sqrt2, 0, -sqrt2, 0],
              [0, sqrt2, 0, -sqrt2],
              [half, -half, half, -half]
              ])
  return dct

def DCT_transform(image, N=4):
  """
  Given image, and optional dimm size (not in use as i'm using toy basis here)
  returns image transformed into DCT basis. 
  """
    basis = generate_toy_dct_basis()
    transformed = np.zeros((N,N))
    for i in range(N):
      for j in range(N):
        ijbasis_image =  get_ij_basis_image(i, j, basis)
        transformed[i,j] = flatdot(image, ijbasis_image)
    return transformed

def undo_transform(transformed_image):
  undo = np.zeros((transformed_image.shape))
  basis = generate_toy_dct_basis()
  for i in range(transformed_image.shape[0]):
    for j in range(transformed_image.shape[0]):
      ijbasis_image =  get_ij_basis_image(i, j, basis)
      undo += transformed_image[i,j] * ijbasis_image
  return undo


if (__name__ == '__main__'):
  # Now let's choose an toy "image" to work with :
  image = np.array([[0,0,0,0], [0, 100, 100, 0], [0, 100, 100, 0], [0,0,0,0]])

  transformed = DCT_transform(image, N=4)

  plt.imshow(transformed)

  #can we put it back?
  is_this_the_same = undo_transform(transformed)
  print(is_this_the_same)
  plt.imshow(is_this_the_same)
  plt.colorbar()
  plt.show()
  #Yeah, not exactly bc of rounding, but it is visually the same.

  #Now lets do the lossy part.

  #Remove its highest frequency.
  # This corresponds to the nonzero entry in the lowest right corner of the image.
  # in this case [2,2]
  transformed[2,2] = 0
  plt.colorbar()
  plt.show()
  new_image = undo_transform(transformed)
  plt.imshow(new_image)
  plt.colorbar()
  plt.show()