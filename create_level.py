#!/usr/bin/env python3.4

import argparse
import os.path
import sys

# Get the directory of this script
script_dir = os.path.dirname(os.path.realpath(__file__))

outfile = ""

parser = argparse.ArgumentParser(description='Create a segi game level.')

parser.add_argument( '-o', nargs=1, action='store', help='set name of output file')

# Create a function that detects the supported file types
def file_types(suffixes,filename):
    suff = os.path.splitext(filename)[1][1:]
    if suff not in suffixes:
        parser.error( "File has none of the supported suffixes {}".format(suffixes))
    return filename

parser.add_argument('file',action='store',nargs='+',type=lambda s:file_types(("spr","scr","fnt","sid"),s),help='filenames of spr,fnt,scr,sid files')

args = parser.parse_args()

# Loop over the files and sort them into separate arrays.
typed_files = {}  # use a dictionary
for type in ["spr","fnt","scr","sid"]:
    typed_files[type] = []
#typed_files["spr"] = []
#typed_files["fnt"] = []
#typed_files["scr"] = []
#typed_files["sid"] = []
for fname in args.file:
    suff=os.path.splitext(fname)[1][1:]
    typed_files[suff].append(fname)

with open( str(args.o[0]), "wb") as f:
    cur_sprite=0
    for sprfile in typed_files["spr"]:
        spr_data=sprfile.split('=') # syntax = 0=hngr.spr , where 0 is the sprite register
        if len(spr_data)==2:
            spr_register=spr_data[0]
            spr_filename=spr_data[1]
        else:
            spr_filename=spr_data[0]
            spr_register=cur_sprite
        f.write(bytes((0x11,)))
        f.write(bytes((spr_register,)))
        with open( spr_filename, "rb") as spr_input:
            f.write( spr_input.read());
        cur_sprite+=1
    for fntfile in typed_files["fnt"]:
        f.write(bytes((0x22,)))
        os.system(script_dir + '/rle_enc.py ' + fntfile + ' ' + fntfile + '.rle') # Compress font
        with open( fntfile+'.rle',"rb") as fnt_input:  # todo: check, if compressed font is smaller!
            f.write( fnt_input.read());
        fnt_input.close()
        os.system('rm ' + fntfile + '.rle')
    for scrfile in typed_files["scr"]:
#        f.write(bytes((0x13,)))  # Type = 3 (screen), subtype = 1 (uncompressed)
#        with open( scrfile, "rb") as scr_input:
#            f.write( scr_input.read());
         f.write(bytes((0x23,)))  # Type = 3 (screen), subtype = 2 (RLE compressed)
         os.system(script_dir + '/rle_enc.py ' + scrfile + ' ' + scrfile + '.rle') # Compress screen
         with open( scrfile+'.rle',"rb") as scr_input:  # todo: check, if compressed screen is smaller!
             f.write( scr_input.read());
         scr_input.close()
         os.system('rm ' + scrfile + '.rle')
    for sidfile in typed_files["sid"]:
            f.write(bytes((0x14,)))  # Type = 4 (sid file), subtype = 1 (uncompressed)
            sid_size = os.path.getsize(sidfile)  # get the number of bytes to write
            f.write(bytes((sid_size & 0xff,))) # Write the sid size as little endian
            f.write(bytes(((sid_size >> 8) & 0xff,)))
            with open( sidfile, "rb") as sid_input:
                f.write( sid_input.read());  
