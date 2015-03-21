__author__ = 'kra869'
from collections import namedtuple

import struct
import math
import sys
import os
import urlparse

Message = namedtuple('Message', ['msg', 'params'])
Push = namedtuple('Push', "package, hash");

HEADER_STRUCT = "BL"

NAME=str(os.getpid())

def debug(msg):
    sys.stderr.write(NAME+":"+msg+"\n")

def write_msg(output, msg):
    n = output.write(msg+"\n")
    output.flush()
    return n
    
    
def read_msg(input):
    line = input.readline()
    line = line.split();
    params = []
    if len(line) < 1:
        return Message(msg="error", params=params)
        
    if len(line) > 1:
        params = line[1:]
    
    return Message(msg=line[0], params=params)
    
def write_file(output, file, hash):
    BLOCKSIZE = 65000
    pack_size = os.path.getsize(file)
    header = struct.pack(HEADER_STRUCT, 10, pack_size)
    output.write(header);
    output.flush();
    
    with open(file, 'rb') as f:
        buf = f.read(BLOCKSIZE)
        while len(buf) > 0:
            output.write(buf)
            output.flush()
            buf = f.read(BLOCKSIZE)
            
            
    return pack_size
    
def write_empty_file(output, hash):
    pack_size = 0
    header = struct.pack(HEADER_STRUCT, 10, pack_size)
    output.write(header);
    output.flush();
    
    return pack_size
    
def read_file(input, dest_file, hash):
    
    BLOCKSIZE = 65000

    header_size = struct.calcsize(HEADER_STRUCT)
    header = struct.unpack(HEADER_STRUCT, input.read(header_size));
    
    remaining = header[1];
    
    with open(dest_file, "w+") as f:
        while remaining > 0:
            
            N = min(BLOCKSIZE, remaining)
            buf = input.read(N);
            remaining -= len(buf);
            f.write(buf)
    
    return header[0]