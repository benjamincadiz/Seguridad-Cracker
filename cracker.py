#!/usr/bin/env python
import os
import sys
import threading
import signal
import subprocess as s
import time 
import argparse

found = False

def createDictionary(minn,maxx,lower, upper, number):
    letter = 'qwertyuiopasdfghjklzxcvbnm'
    numbers = '1234567890'
    dictt = ''

    if (upper==False and number==False and lower==False): dictt = letter
    if (upper==False and number == False and lower == True): dictt = letter
    if (upper==False and number == True and lower == False): dictt = numbers
    if (upper==False and number ==True and lower == True): dictt = numbers + letter
    if (upper==True and number == False and lower == False): dictt = letter.upper()
    if (upper==True and number == False and lower == True): dictt = letter.upper() +letter
    elif (upper==True and number == True and lower == False): dictt = letter.upper() + numbers
    elif (upper==True and number==True and lower==True): dictt = letter + letter.upper() + numbers

    print('Generating dictionary with: '+dictt)
    os.system('crunch '+minn+' '+maxx+' '+dictt+' -o dict.txt')

def clean(word):
    password = word.strip()
    return password

def handler(signum, frame):
    for i in enumerate():
        if(thread.isAlive()):
            thread._Thread_stop()

def search(begin,end,password,onethread, gpg ):
    os.system('mkdir -p results')
    for ps in password[int(begin):int(end) + int(onethread)]:
        global found 
        if found == True: 
            time.sleep(2)
            exit()
        else:
            password = clean(ps)
            test = os.system('echo '+password+' | gpg --batch --yes --passphrase-fd 0 '+gpg+' 2> results/log.txt ')
            if test == 0:
                print(str(threading.current_thread().name)+' has found the pass')
                os.system('echo '+password+' > results/pass.txt')
                print('Closing trhreads...')
                os.system('mv '+gpg[:-4]+' results/')
                time.sleep(2)
                found = True

if __name__ == '__main__':
    lower = upper = number = False
    #Arguments 
    parser = argparse.ArgumentParser(description='Process some integers.') 
    parser.add_argument("-f", "--file",required = True,
                    help='file to crack')
    parser.add_argument("--min",required = True,
                    help='minimum of dictionary')
    parser.add_argument("--max",required = True,
                    help='maximum of dictionary')
    parser.add_argument("-t","--thread",required = True,
                    help='number of threads')
    parser.add_argument('-l','--lower',action='store_true',help='add minus to')
    parser.add_argument("-u", "--upper",action='store_true',
                    help='add mayus to')
    parser.add_argument("-n", "--number",action='store_true',
                    help='add number to dictionary')
    
    args = vars(parser.parse_args())
    if args['upper']:
        upper = True
    if args['lower']:
        lower = True
    if args['number']:
        number = True
   
    createDictionary(args['min'],args['max'],lower, upper, number)

    #Get data of dictionary
    fichero = open('dict.txt', 'r')
    password = fichero.readlines() 
    num_pass = len(password)
    
    #Get data of thread
    onethread = num_pass/int(args['thread'])
    begin = 0
    end = onethread
    threads = list()
    
    #Create the threads
    for i in range(int(args['thread'])):
        t = threading.Thread(name= 'Thread %s'%i, target=search,args=(begin,end,password,int(onethread),args['file']), daemon= True)
        begin += onethread
        end += onethread
        threads.append(t)
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]