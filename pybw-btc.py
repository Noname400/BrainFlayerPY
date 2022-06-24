# #!/usr/bin/python3
# encoding=utf8
# -*- coding: utf-8 -*-
"""
@author: Noname400
@GitHub https://github.com/Noname400
"""
# from typing import AnyStr, List, TypeVar, Union
from multiprocessing import Pool, freeze_support, cpu_count, Array
import sys, time, argparse, logging
from libraries.filter import BloomFilter
import codecs
import signal
import requests, os
import sha3
import hashlib
from libraries.secp256k1_lib import privatekey_to_h160, privatekey_to_ETH_address, hash_to_address, pubkey_to_h160, get_sha256
from logging import Formatter

current_path = os.path.dirname(os.path.realpath(__file__))
logger_found = logging.getLogger('FOUND')
logger_found.setLevel(logging.INFO)
handler_found = logging.FileHandler(os.path.join(current_path+'/log', 'found.log'), 'a' , encoding ='utf-8')
logger_found.addHandler(handler_found)

logger_err = logging.getLogger('ERROR')
logger_err.setLevel(logging.DEBUG)
handler_err = logging.FileHandler(os.path.join(current_path+'/log', 'error.log'), 'w' , encoding ='utf-8')
logger_err.addHandler(handler_err)

def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

class inf:
    version:str = '* PY-Brainflayer v2.3 BTC*'
    th = 1
    in_file = ''
    mode:str = ''
    bf_dir = ''
    bf:BloomFilter
    
def createParser ():
    parser = argparse.ArgumentParser(description='PY-Brainflayer')
    parser.add_argument ('-th', '--threading', action='store', type=int, help='threading', default='1')
    parser.add_argument ('-db', '--database', action='store', type=str, help='File BF', default='')
    parser.add_argument ('-in', '--infile', action='store', type=str, help='infile', default='')
    return parser.parse_args().threading, parser.parse_args().database, parser.parse_args().infile

def bw(text):
    f1 = []
    sha = get_sha256(text.encode("utf-8"))
    pvk = int(sha.hex(),16)
    # print(f'get_sha256  {pvk}')
    f1.append([text,pvk,privatekey_to_h160(0, False, pvk)])
    f1.append([text,pvk,privatekey_to_h160(0, True, pvk)])
    return f1

def load_BF(load):
    try:
        fp = open(load, 'rb')
    except FileNotFoundError:
        print(f'[E] File: {load} not found.')
        sys.exit()
    else:
        return BloomFilter.load(fp)

if __name__ == "__main__":
    freeze_support()
    end = False
    inf.th, inf.bf_dir, inf.in_file = createParser()
    print('-'*70,end='\n')
    print('Thank you very much: @iceland2k14 for his libraries!')

    if inf.in_file != '':
        pass
    else:
        print('[E] Empty imput file')
        exit(1)

    if inf.th < 1:
        print('[E] The number of processes must be greater than 0')
        inf.th = 1

    if inf.th > cpu_count():
        print('[I] The specified number of processes exceeds the allowed')
        print('[I] FIXED for the allowed number of processes')
        inf.th = cpu_count()-1

    print('-'*70,end='\n')
    print(f'[I] Version: {inf.version}')
    print(f'[I] Input file: {inf.in_file}')
    print(f'[I] Total kernel of CPU: {cpu_count()}')
    print(f'[I] Used kernel: {inf.th}')
    print(f'[I] Database Bloom Filter: {inf.bf_dir}')
    print('-'*70,end='\n')

    l = []
    inf.bf = load_BF(inf.bf_dir)
    print('BF загружен...')
    print('Загрузка словаря...')
    line_co = 0
    co = 0
    l = []
    file = ''
    list_line = 50000
    total_count = 0
    total_st = time.time()
    with codecs.open(inf.in_file, 'r', encoding='utf-8') as file:
        for line in file:
            line_co += 1
            l.append(line.strip())
            if line_co == list_line:
                total_count += list_line
                line_co = 0
                st = time.time()
                with Pool(inf.th, init_worker) as pool:
                    results = pool.map(bw, l)
                    for ii in range(len(results)):
                        for iii in range(len(results[ii])):
                            #print(results[ii][iii][2].hex())
                            if results[ii][iii][2].hex() in inf.bf:
                                addr = hash_to_address(0,False,results[ii][iii][2])
                                print(f' \n FOUND - {addr} word - {results[ii][iii][0]} PVK - {hex(results[ii][iii][1])} \n')
                                logger_found.info(f' \n FOUND - {addr} word - {results[ii][iii][0]} PVK - {hex(results[ii][iii][1])} \n')
                            co += 1
                print(f'Total time: {time.time()-total_st:.2f}, count: {total_count}, speed: {int(co/(time.time()-st))} key/sec')
                co = 0
                l = []
                pool.terminate()
                pool.join()
    print ("Файл закончился...")

