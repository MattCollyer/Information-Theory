#Hello
___

Another pretty good week.

###I Implemented LZW
and it went ok. took me long enough to get it running and looking good. I didn't go as far to literally compress the files or anything, I just got a working version of the encoding/decoding algorithm. 

Very neat. Nice contrast to Huffman.

I have more helper functions and stuff, but here's the basis of it: 


```


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

```

I didn't really worry about encoding it into binary for ease, I just later did to see how long the stream was shrunk by.



##Outputs
I was initially blown away by how good it was, and then I realized I wasnt ensuring a fixed length to my binary stream.

For example, using the same dune text I used for huffman (variable length):



```
-------------------------------------
Stream successfully encoded and is decodable
Amount of bits using ASCII: 7971152
Amount of bits using LZW : 4619597
With this codex, the original text can be shrunk by  42.05 percent
-------------------------------------
```

And this is when I ensured a fixed length.
```

-------------------------------------
Stream successfully encoded and is decodable
Amount of bits using ASCII: 8335033
Amount of bits using LZW : 5315341
With this codex, the original text can be shrunk by  36.23 percent
-------------------------------------
```

Still pretty good! 
I wanted to go and implement the Burrows-Wheeler transform to see how much better it could be.
Unfortunately my time didn't allow for that.
However I did have a blast looking into it. There's a super neat bijective variant of it such that you don't have to supply the index of the original string. Cool!


##ALSO
I created a public github repo for this class. Should I just link to my code or should I still upload files to umber? For now, here's a link to this LZW assignment.



Thats it for now.
