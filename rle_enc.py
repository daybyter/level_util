#!/usr/bin/env python3.4

import sys

if len(sys.argv) != 3:
    print ("Error: wrong number of arguments")
    print ("Syntax: rel_scr <inputfile> <outputfile>")
    sys.exit()

curlen = 1

with open( sys.argv[1],"rb") as f:
    with open( sys.argv[2], "wb") as f2:
        byte = f.read(1)
        curbyte = byte
        while byte != b"":
            byte = f.read(1)
            if byte != curbyte or curlen == 255:
                f2.write(curlen.to_bytes(1,byteorder='big'))
                f2.write(curbyte)
                curlen = 1
                curbyte = byte
            else:
                curlen += 1
                
