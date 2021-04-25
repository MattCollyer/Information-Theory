




def curve_from_ip(ip):
  sections = ip.split('.')
  offset_code = {'0': -1, '1': -0.8, '2': -0.6, '3': -0.4, '4': -0.2, '5': 0.2, '6':0.4, '7': 0.6,'8':0.8, 9: 1}
  offset_vector = []
  for chunk in sections:
    for number in chunk:
      offset_vector.append(offset_code[number])
  return offset_vector

def ips_from_hex_stream(hex_stream):
  source = hex_stream[26*2:30*2]
  dest = hex_stream[30*2:34*2]
  return (source,dest)

def hex_to_ip(hex_ip):
  ip_addr = ''
  for i in range(len(hex_ip)/2):
    chunk = str(int(hex_ip[i*2:i*2+2], 16))
    if(len(chunk)==1):
      chunk = '00' + chunk
    elif(len(chunk) == 2):
      chunk = '0' + chunk
    ip_addr += chunk
    ip_addr+= '.'
  return ip_addr[:-1]


def hamming_distance(string1, string2):
	dist_counter = 0
	for n in range(len(string1)):
		if string1[n] != string2[n]:
			dist_counter += 1
	return dist_counter

def hex_to_bin(stream):
  bin_stream = []
  hex_stream = [stream[i:i+2] for i in range(0, len(stream))]
  for hex in hex_stream:
    i = int(hex, 16)
    bin_stream.append('{:0{length}b}'.format(i, length = 8))
  return bin_stream


def distances(stream, parity):
  d = []
  for i in range(len(stream)/2):
    distance = hamming_distance(stream[i*2], stream[(i*2)+1])
    d.append((float(distance) * parity[i])/10)
  return d 

def split_into_chunks(stream, chunksize):
  large_chunk_len = len(stream)/chunksize
  new = []
  chunk = ''
  for i in range(len(stream)):
    if(i % large_chunk_len == 0 and i != 0):
      new.append(chunk)
      chunk = ''
    chunk += stream[i]
  if(chunk != ''):
    #Append the rest if its not a perfect fit
    new[len(new)-1] += chunk
  return new


def parity(stream):
  p = []
  for byte in stream:
    if(int(byte,2) % 2 != 0):
      parity = 1
    else:
      parity = -1
    p.append(parity)
  return p


def get_parity_vector(stream, chunksize):
  large_stream = split_into_chunks(stream, chunksize)
  parities = parity(large_stream)
  elongated = []
  for p in parities:
    for i in range((len(stream)/2)/chunksize):
      elongated.append(p)
  #append the overhang
  for i in range((len(stream)/2)%chunksize):
    elongated.append(parities[len(parities)-1])
  return elongated



if(__name__ == '__main__'):
    stream = '01005e0000fb8e8c762f1aee08004500007ad98e0000ff11fec60a0af817e00000fb14e914e90066a566000000000001000000000001144d616961e2809973204d6163426f6f6b204169720f5f636f6d70'
    stream2 = '01005e0000fb8ef88104fc03080045000395e86a0000ff11ec8d0a0af859e00000fb14e914e9038190f70000000000040016000000010f5f636f6d70616e696f6e2d6c696e6b045f746370056c6f63616c00000c0001085f686f6d656b6974c01c000c00010c5f736c6565702d70726f7879045f756470c021000c000115536861616be2809973204d6163426f6f6b20416972c00c00108001c00c000c00010000119300191657616c746572e2809973204d6163426f6f6b20416972c00cc00c000c000100001193001815446162696ee2809973204d6163426f6f6b2050726fc00cc00c000c000100001193001d1a456c69736861e2809973204d6163426f6f6b2050726f20283329c00cc00c000c0001000011930017144d697261e2809973204d6163426f6f6b2050726fc00cc00c000c0001000011930018154c756379e2809973204d6163426f6f6b2050726f20c00cc00c000c0001000011930019164a6f73687561e2809973204d6163426f6f6b20416972c00cc00c000c0001000011940018154461726279e2809973204d6163426f6f6b20416972c00cc00c000c0001000011940013104d6163426f6f6b204169722028323329c00cc00c000c0001000011940002c053c00c000c00010000119400181557696c6c73e2809973204d6163426f6f6b2050726fc00cc00c000c000100001194001b18416b796c6169796de2809973204d6163426f6f6b2050726fc00cc00c000c00010000119400070442616368c00cc00c000c00010000119400171474657374e2809973204d6163426f6f6b20416972c00cc00c000c0001000011940014114be2809973204d6163426f6f6b2050726fc00cc00c000c0001000011940017144d616961e2809973204d6163426f6f6b20416972c00cc00c000c000100001194000a07464c6f57203131c00cc00c000c0001000011940018154a6f736965e2809973204d6163426f6f6b20416972c00cc00c000c000100001194001b18436f7572746e6579e2809973204d6163426f6f6b2050726fc00cc00c000c0001000011940018154b69616e61e2809973204d6163426f6f6b2050726fc00cc00c000c00010000119400151244616e692773204d6163426f6f6b2050726fc00cc02c000c00010000119400272433413243333432382d353935432d353730392d423846372d393430373230343435464642c02cc03b000c00010000119400151237302d33352d36302d36332e312042616368c03b00002905a00000119400120004000e005faabe27bdba4c8ef88104fc03'
    bin_stream = hex_to_bin(stream.strip())
    pv = get_parity_vector(bin_stream, 8)
    print(pv)
    d = distances(bin_stream, pv)
    print(d)