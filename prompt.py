import re
import time
import aquery_parser as parser
import engine
import subprocess
import mmap
import sys
import os
from engine.utils import base62uuid
import atexit

def rm():
    files = os.listdir('.')
    for f in files:
        if f.endswith('.shm'):
            os.remove(f)
atexit.register(rm)
    
shm = base62uuid()
if sys.platform != 'win32':
    import readline
    shm += '.shm'
    basecmd = ['bash', '-c', 'rlwrap k']
    mm = None
    if not os.path.isfile(shm):
        # create initial file
        with open(shm, "w+b") as handle:
            handle.write(b'\x01\x00') # [running, new job]
            handle.flush()
            mm = mmap.mmap(handle.fileno(), 2, access=mmap.ACCESS_WRITE, offset=0)
    if mm is None:
        exit(1)
else:
    basecmd = ['bash.exe', '-c', 'rlwrap ./k']
    mm = mmap.mmap(0, 2, shm)
    mm.write(b'\x01\x00')
    mm.flush()
subprocess.Popen(["./server.bin", shm])
test_parser = True

# code to test parser
ws = re.compile(r'\s+')

q = 'SELECT p.Name, v.Name FROM Production.Product p JOIN Purchasing.ProductVendor pv ON p.ProductID = pv.ProductID JOIN Purchasing.Vendor v ON pv.BusinessEntityID = v.BusinessEntityID WHERE ProductSubcategoryID = 15 ORDER BY v.Name;'

res = parser.parse(q)

print(res)


# else:f
#     if subprocess.call(['make', 'snippet']) == 0:
#         mm.seek(0)
#         mm.write(b'\x01\x01')
#         time.sleep(.1)
#         mm.seek(0)
#         print(mm.read(2))
        
#         mm.close()
#         handle.close()
#         os.remove(shm)
#     exit()
keep = False
cxt = None
while test_parser:
    try:
        q = input()
        if q == 'exec':
            if not keep or cxt is None:
                cxt = engine.initialize()
            stmts_stmts = stmts['stmts']
            if type(stmts_stmts) is list:
                for s in stmts_stmts:
                    engine.generate(s, cxt)
            else:
                engine.generate(stmts_stmts, cxt)
            print(cxt.ccode)
            with open('out.cpp', 'wb') as outfile:
                outfile.write((cxt.finalize()).encode('utf-8'))
            if subprocess.call(['make', 'snippet']) == 0:
                mm.seek(0,os.SEEK_SET)
                mm.write(b'\x01\x01')
            continue
        elif q == 'k':
            subprocess.call(basecmd)
            continue
        elif q == 'print':
            print(stmts)
            continue
        elif q == 'keep':
            keep = not keep
            continue
        elif q == 'exit':
            break
        elif q == 'r':
            if subprocess.call(['make', 'snippet']) == 0:
                mm.seek(0,os.SEEK_SET)
                mm.write(b'\x01\x01')
            continue
        trimed = ws.sub(' ', q.lower()).split(' ') 
        if trimed[0].startswith('f'):
            fn = 'stock.a' if len(trimed) <= 1 or len(trimed[1]) == 0 \
                            else trimed[1]
                
            with open(fn, 'r') as file:
                contents = file.read()
            stmts = parser.parse(contents)
            continue
        stmts = parser.parse(q)
        print(stmts)
    except (ValueError) as e:
        print(type(e), e)

mm.close()
handle.close()
os.remove(shm)