from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

print('I am in rank:'+str(rank)+' size:'+str(size)+'\n')
import multiprocessing
cpus = multiprocessing.cpu_count()
print('number of cpus:'+str(cpus))
