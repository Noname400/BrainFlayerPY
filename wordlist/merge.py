import sys
import base58
import codecs
import sys, time, argparse, logging

def createParser ():
    parser = argparse.ArgumentParser(description='PY-Brainflayer')
    parser.add_argument ('-in', '--infile', action='store', type=str, help='infile', default='')
    parser.add_argument ('-out', '--outfile', action='store', type=str, help='outfile', default='')
    return parser.parse_args().infile, parser.parse_args().outfile




if __name__ == "__main__":
    co = 0
    c=1000
    in_file, out_file  = createParser()
    out = open(out_file,'a')
    with open(in_file, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            line = line.strip()
            #print(str(line))
            try:
                out.write(f'{line}\n')
            except:
                continue
            if co == c:
                print(co)
                c += 100000
            co +=1
              
    out.close
