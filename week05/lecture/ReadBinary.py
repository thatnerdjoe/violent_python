'''
Reading Binary Files in Chunks
Exp-12.py
'''
from binascii import hexlify
CHUNK_SIZE = 40
with open('test.bin', 'rb') as binaryFile:
    while True:
        chunk = binaryFile.read(CHUNK_SIZE)
        if chunk:
            print(hexlify(chunk))
        else:
            break

print("Script Ended")
