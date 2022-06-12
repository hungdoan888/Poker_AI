# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 08:15:33 2022

@author: hungd
"""



import multiprocessing
import time
   
  
def useless_function(sec = 1):
     print(f'Sleeping for {sec} second(s)')
     time.sleep(sec)
     print('Done sleeping')
   

start = time.perf_counter()
pool = multiprocessing.Pool()
pool = multiprocessing.Pool(processes=4)
inputs = [3]
pool.map(useless_function, inputs)
end = time.perf_counter()
print(f'Finished in {round(end-start, 2)} second(s)') 