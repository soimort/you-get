#!/usr/bin/env python

import struct
from io import BytesIO

##################################################
# main
##################################################

def guess_output(inputs):
    import os.path
    inputs = map(os.path.basename, inputs)
    n = min(map(len, inputs))
    for i in reversed(range(1, n)):
        if len(set(s[:i] for s in inputs)) == 1:
            return inputs[0][:i] + '.ts'
    return 'output.ts'

def concat_ts(ts_parts, output = None):
    assert ts_parts, 'no ts files found'
    import os.path
    if not output:
        output = guess_output(ts_parts)
    elif os.path.isdir(output):
        output = os.path.join(output, guess_output(ts_parts))
    
    print('Merging video parts...')
    
    ts_out_file = open(output, "wb")
    for ts_in in ts_parts:
        ts_in_file = open(ts_in, "rb")
        ts_in_data = ts_in_file.read()
        ts_in_file.close()
        ts_out_file.write(ts_in_data)
    ts_out_file.close()
    return output

def usage():
    print('Usage: [python3] join_ts.py --output TARGET.ts ts...')

def main():
    import sys, getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:", ["help", "output="])
    except getopt.GetoptError as err:
        usage()
        sys.exit(1)
    output = None
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
        else:
            usage()
            sys.exit(1)
    if not args:
        usage()
        sys.exit(1)
    
    concat_ts(args, output)

if __name__ == '__main__':
    main()
