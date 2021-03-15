import math



bits = []
pairs = []


def probability(arr, elem):
  return float(arr.count(elem))/len(arr)


with open ('stream1.txt') as file:
  for line in file:
    for bit in line:
      if(bit == "0" or bit == '1'):
        bits.append(bit)



pairs = [(bits[i], bits[i+1]) for i in range(int(len(bits)/2))]



zero_prob = probability(bits, '0')
zero_entropy = -(zero_prob) * math.log(zero_prob, 2)


one_prob = probability(bits, '1')
one_entropy = -(one_prob) * math.log(one_prob,2)

zero_one_prob = probability(pairs, ('0','1'))
zero_one_entropy = -(zero_one_prob) * math.log(zero_one_prob, 2)

one_zero_prob = probability(pairs, ('1','0'))
one_zero_entropy = -(one_zero_prob) * math.log(one_zero_prob, 2)

zero_zero_prob = probability(pairs, ('0','0'))
zero_zero_entropy = -(zero_zero_prob) * math.log(zero_zero_prob, 2)

one_one_prob = probability(pairs, ('1','1'))
one_one_entropy = -(one_one_prob) * math.log(one_one_prob, 2)






print("\n\n\n")
print("Number of characters: ", len(bits))
print("Probablility of 0: ", zero_prob)
print("Entropy of 0: ",zero_entropy)
print("Probability of 1: ", one_prob)
print("Entropy of 1: ", one_entropy)

print("\n\n")

print("0 0 Entropy: ", zero_zero_entropy)
print("0 1 Entropy: ", zero_one_entropy)
print("1 0 Entropy: ", one_zero_entropy)
print("1 1 Entropy: ", one_one_entropy)
