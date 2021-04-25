def build_base_dictionary(cap = 128):
  #Builds disctionary. Assumes ASCII, can go farther if unicode. the chr func is interesting
  dictionary = { chr(i): i for i in range(cap)}
  return (cap-1, dictionary)


def reverse_dictionary(dictionary): #Stupid function that just reverses a dictionary.
  return {value: key for key, value in dictionary.items()}


def decode_with_dict(encoded, dictionary): #helpful for debugging
  decode_stream = ''
  dictionary = reverse_dictionary(dictionary)
  decoded = []
  for elem in encoded:
    decoded.append(dictionary[elem])
    decode_stream += dictionary[elem]
  print("\n\nDECODING WITH DICTIONARY. FOR DEBUGGING ")
  print(decoded)
  print(decode_stream)
  print('\n\n\n')


def encode_lzw(stream, max_bit_len):
  #Build our starting dictionary, get our starting code value
  (code_value, dictionary) = build_base_dictionary()
  encoded = [] 
  block = ''
  for character in stream:
    #Instantly add the newest char to our block. 
    #If it's not in our dictionary....  add the codeword for the prev block, put in dictionary if we can.
    block += character 
    if(block not in dictionary):
      encoded.append(dictionary[block[:-1]])
      if(code_value < (2 ** max_bit_len)):
        code_value += 1
        dictionary[block] = code_value
      block = character
  encoded.append(dictionary[block])
  return encoded




def decode_lzw(encoded_stream, max_bit_len):
  (code_value, dictionary) = build_base_dictionary()
  dictionary = reverse_dictionary(dictionary)
  code_value = 127
  decoded_stream = ''
  new_codeword = ''
  for code in encoded_stream:
    #look up dictionary 
    decoded_stream += dictionary[code]
    new_codeword += dictionary[code][:1]
    if (new_codeword not in dictionary.values() and code_value < (2 ** max_bit_len)):
      code_value += 1
      dictionary[code_value] = new_codeword
      new_codeword = dictionary[code]
  return decoded_stream


def encoded_to_bit_str_variable(encoded):
  bit_stream = []
  for num in encoded:
    bit_stream += str(bin(num))[2:]
  return bit_stream

def uncoded_to_bit_str_variable(stream):
  bit_stream = []
  for char in stream:
    bit_stream += str(bin(ord(char)))[2:]
  return bit_stream


def encoded_to_bit_str_fixed(encoded, max_bit_len):
  bit_stream = []
  for num in encoded:
    bit_stream += '{:0{length}b}'.format(num, length = max_bit_len)
  return bit_stream

def uncoded_to_bit_str_fixed(stream, max_bit_len = 7):
  bit_stream = []
  for char in stream:
    bit_stream += '{:0{length}b}'.format(ord(char), length = max_bit_len)
  return bit_stream


def percent_decrease(original, new):
  return round( ((original - new) /original) * 100, 2)

def summary(stream, max_bit_len = 10):
  encoded = encode_lzw(stream, max_bit_len)
  decoded = decode_lzw(encoded, max_bit_len)
  print('\n\n\n-------------------------------------')

  if(stream == decoded):
    print("Stream successfully encoded and is decodable")
  else:
    print("Stream was not successfully encoded and decoded")

  original_bit_length = len(uncoded_to_bit_str_fixed(stream))
  

  new_size_fixed = len(encoded_to_bit_str_fixed(encoded, max_bit_len))
  new_size_variable = len(encoded_to_bit_str_variable(encoded))

  print("Amount of bits using ASCII:", original_bit_length)
  print("Amount of bits using FIXED LENGTH LZW :", new_size_fixed)
  print("With this fixed length codex, the original text can be shrunk by ", percent_decrease(original_bit_length, new_size_fixed), 'percent')
  print("Amount of bits using VARIABLE LENGTH LZW:", new_size_variable)
  print("With this variable length codex, the original text can be shrunk by ", percent_decrease(original_bit_length, new_size_variable), 'percent')
  print('-------------------------------------\n\n\n')






if (__name__ == '__main__'):
  with open('../texts/dune.txt', 'r') as file:
    stream = file.read()
  # stream = 'TOBEORNOTTOBEORTOBEORNOT'
  # stream = 'At each stage, the decoder receives a code X; it looks X up in the table and outputs the sequence x it codes, and it conjectures x + ? as the entry the encoder just added - because the encoder emitted X for x precisely because x + ? was not in the table, and the encoder goes ahead and adds it. But what is the missing letter? It is the first letter in the sequence coded by the next code Z that the decoder receives. So the decoder looks up Z, decodes it into the sequence w and takes the first letter z and tacks it onto the end of x as the next dictionary entry.'

  summary(stream)





