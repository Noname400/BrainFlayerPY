# #!/usr/bin/python3
# encoding=utf8
# -*- coding: utf-8 -*-
"""
@author: Noname400
@GitHub https://github.com/Noname400
"""

from multiprocessing import Pool, freeze_support, cpu_count, Array
import sys, time, argparse, logging
from filter import BloomFilter
import signal
import bitcoin, requests, os
import secp256k1_lib
from logging import Formatter
from colorama import Back, Fore, Style, init
init(autoreset = True)


def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

class inf:
    version:str = '* PY-Brainflayer v1.4 beta *'
    th = 1
    in_file = ''
    balance:bool = False
    bal_server:list = ['https://api.blockcypher.com/v1/btc/main/addrs/', 'https://rest.bitcoin.com/v2/address/details/', 'https://sochain.com/api/v2/address/BTC/', \
        'https://blockchain.info/rawaddr/']
    ETH_bal_server:list = ['https://api.blockchair.com/ethereum/dashboards/address/','https://api.etherscan.io/api?module=account&action=balance&address=']
    bal_srv_count:int = 0
    bal_all_err = 0
    mode:str = ''
    bf_dir = ''
    bf:BloomFilter
    telegram = False
    telegram_err = 0
    #mail
    mail:bool = False
    mail_err:str = 0
    #debug
    debug:bool = False
    
def createParser ():
    parser = argparse.ArgumentParser(description='PY-Brainflayer')
    parser.add_argument ('-th', '--threading', action='store', type=int, help='threading', default='1')
    parser.add_argument ('-db', '--database', action='store', type=str, help='File BF', default='')
    parser.add_argument ('-in', '--infile', action='store', type=str, help='infile', default='')
    parser.add_argument ('-m', '--mode', action='store', type=str, help='mode sha256,dsha256', default='s')
    parser.add_argument ('-bal', '--balance', action='store_true', help='check balance')
    return parser.parse_args().threading, parser.parse_args().database, parser.parse_args().infile, parser.parse_args().mode, parser.parse_args().balance

current_path = os.path.dirname(os.path.realpath(__file__))
logger_found = logging.getLogger('FOUND')
logger_found.setLevel(logging.INFO)
handler_found = logging.FileHandler(os.path.join(current_path, 'found.log'), 'a' , encoding ='utf-8')
handler_found.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger_found.addHandler(handler_found)

logger_info = logging.getLogger('INFO')
logger_info.setLevel(logging.INFO)
handler_info = logging.FileHandler(os.path.join(current_path, 'info.log'), 'a' , encoding ='utf-8')
handler_info.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger_info.addHandler(handler_info)

logger_dbg = logging.getLogger('DEBUG')
logger_dbg.setLevel(logging.DEBUG)
handler_dbg = logging.FileHandler(os.path.join(current_path, 'debug.log'), 'w' , encoding ='utf-8')
logger_dbg.addHandler(handler_dbg)

logger_err = logging.getLogger('ERROR')
logger_err.setLevel(logging.DEBUG)
handler_err = logging.FileHandler(os.path.join(current_path, 'error.log'), 'w' , encoding ='utf-8')
handler_err.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger_err.addHandler(handler_err)

def get_balance(address):
    time.sleep(11) 
    try:
        if inf.bal_srv_count == 0:
            response = requests.get(inf.bal_server[inf.bal_srv_count] + str(address))
            return int(response.json()['n_tx']), float(response.json()['balance'])
        elif inf.bal_srv_count == 1:
            response = requests.get(inf.bal_server[inf.bal_srv_count] + str(address))
            return int(response.json()['txApperances']), float(response.json()['balance'])
        elif inf.bal_srv_count == 2:
            response = requests.get(inf.bal_server[inf.bal_srv_count] + str(address))
            return int(response.json()['data']['total_txs']), float(response.json()['data']['balance'])
        elif inf.bal_srv_count == 3:
            response = requests.get(inf.bal_server[inf.bal_srv_count] + str(address))
            return int(response.json()['n_tx']), float(response.json()['final_balance'])
    except:
        logger_err.error('[E][BRAIN] NOT connect balance server')
        print('[E][BRAIN] NOT connect balance server')
        if inf.bal_err < 10:
            inf.bal_err += 1
        else:
            if inf.bal_srv_count < 3:
                inf.bal_srv_count += 1
            else:
                inf.bal_srv_count = 0
        inf.bal_all_err += 1
        if inf.bal_all_err == 40:
            inf.balance = False
        return -1


def bw(text):
    f1 = []
    pvk = int(bitcoin.sha256(text),16)
    f1.append([text,pvk,secp256k1_lib.privatekey_to_h160(0, True, pvk)])
    f1.append([text,pvk,secp256k1_lib.privatekey_to_h160(0, False, pvk)])
    pvk_d = int(bitcoin.dbl_sha256(text),16)
    f1.append([text,pvk_d,secp256k1_lib.privatekey_to_h160(0, True, pvk_d)])
    f1.append([text,pvk_d,secp256k1_lib.privatekey_to_h160(0, False, pvk_d)])
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
    inf.th, inf.bf_dir, inf.in_file, inf.mode, inf.balance  = createParser()
    logging.basicConfig(filename='general.log', level=logging.DEBUG, format='[%(asctime)s] - [%(name)s] - [%(levelname)s] - [%(message)s]')
    logging.info(f'Start PY-Brainflayer version {inf.version}')
    print('-'*70,end='\n')
    print('Thank you very much: @iceland2k14 for his libraries!')

    if inf.mode in ('sha256'): #, 'sha3'
        pass
    else:
        print('[E] Wrong mode selected')
        sys.exit()

    if inf.in_file != '':
        pass
    else:
        print('[E] Empty imput file')
        sys.exit()

    if inf.th < 1:
        print('[E] The number of processes must be greater than 0')
        sys.exit()

    if inf.th > cpu_count():
        print('[I] The specified number of processes exceeds the allowed')
        print('[I] FIXED for the allowed number of processes')
        inf.th = cpu_count()

    print('-'*70,end='\n')
    print(f'[I] Version: {inf.version}')
    print(f'[I] Input file: {inf.in_file}')
    print(f'[I] Total kernel of CPU: {cpu_count()}')
    print(f'[I] Used kernel: {inf.th}')
    print(f'[I] Work mode - {inf.mode}')
    print(f'[I] Database Bloom Filter: {inf.bf_dir}')
    if inf.balance: print('[I] Check balance BTC: On')
    else: print('[I] Check balance: Off')
    print('-'*70,end='\n')

    l = []
    inf.bf = load_BF(inf.bf_dir)
    print('BF загружен...')
    file = open(inf.in_file, "r")
    print('Загрузка словаря...')
    co = 0


    while True:
        l = []
        list_line = 50000
        st = time.time()
        for i in range(list_line):
            line = file.readline().strip()
            if not line:
                print('Конец файла либо в файле есть пустая строка...')
                end = True
                list_line = i
                break
            l.append(line)
        with Pool(inf.th, init_worker) as pool:
            results = pool.map(bw, l)
            for ii in range(len(results)):
                for iii in range(len(results[ii])):
                    #print(results[ii][iii][2].hex())
                    co +=1
                    if results[ii][iii][2].hex() in inf.bf:
                        addr = secp256k1_lib.hash_to_address(0,False,results[ii][iii][2])
                        if inf.balance: 
                            bal = get_balance(addr)
                            if bal > 0.0 : print(f' \n FOUND - {addr}  balance - {bal} word - {results[ii][iii][0]} PVK - {results[ii][iii][1]} \n')
                        else:
                            print(f' \n FOUND - {addr} word - {results[ii][iii][0]} PVK - {results[ii][iii][1]} \n')

            print(f'time: {time.time()-st:.2f}, count: {co}, speed: {int(co/(time.time()-st))}/sec')
            co = 0
            if end: 
                print ("Файл закончился...")
                pool.terminate()
                pool.join()
                file.close()
                exit(0)