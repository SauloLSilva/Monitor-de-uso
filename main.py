from multiprocessing import Pool
import os
import time

def run_process(process):
    os.system('python3 {0}'.format(process))
    time.sleep(2.5)

# process = ('identificador.py', 'run.py','monitoramento.py')
# pool = Pool(processes=3)
process = ('identificador.py', 'run.py', 'monitoramento.py')
pool = Pool(processes=2)
pool.map(run_process, process)