import sys
import codecs
import sys, time, argparse, logging

def createParser ():
    parser = argparse.ArgumentParser(description='PY-Brainflayer')
    parser.add_argument ('-in', '--infile', action='store', type=str, help='infile', default='')
    parser.add_argument ('-out', '--outfile', action='store', type=str, help='outfile', default='')
    return parser.parse_args().infile, parser.parse_args().outfile




if __name__ == "__main__":
    co = 0
    c=100000
    coo = 0
    in_file, out_file  = createParser()
    out = codecs.open(out_file,'a', encoding='utf-8')
    with codecs.open(in_file, 'r', encoding='utf-8', errors = 'ignore') as file:
        for line in file:
            line = line.strip()
            if line == '' or line == ' ': continue
            #print(line)
            out.write(f'{line}\n')
            if co == c:
                print(co)
                c += 100000
            co +=1
    out.close
