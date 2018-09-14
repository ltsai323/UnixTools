#!/usr/bin/env python
# https://docs.python.org/2/library/threading.html

# Remark: Due to the GIL design of  python, multithreading benefits from only IO-bound jobs.

import os,sys,time
import re
import multiprocessing

def daemon():
    print 'Starting:', multiprocessing.current_process().name
    time.sleep(10)
    pass

def sleep_worker(iSeconds):
    print 'Starting:', multiprocessing.current_process().name
    time.sleep(iSeconds)
    print 'Exiting :', multiprocessing.current_process().name

if __name__ == '__main__':
    d = multiprocessing.Process(name='Multiprocessing daemon', target=daemon)
    d.daemon = True

    n1 = multiprocessing.Process(name='non-daemon Function 1', target=sleep_worker, args=(5,))
    n2 = multiprocessing.Process(name='non-daemon Function 2', target=sleep_worker, args=(3,))

    d.start()
    n1.start()
    n2.start()

    n1.join()
    n2.join()
    #d.join() # will wait to the end of 'joined' process
    print """End of main."""
