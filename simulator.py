'''
CS5250 Assignment 4, Scheduling policies simulator
Sample skeleton program
Author: Minh Ho
Input file:
    input.txt
Output files:
    FCFS.txt
    RR.txt
    SRTF.txt
    SJF.txt

Apr 10th Revision 1:
    Update FCFS implementation, fixed the bug when there are idle time slices between processes
    Thanks Huang Lung-Chen for pointing out
Revision 2:
    Change requirement for future_prediction SRTF => future_prediction shortest job first(SJF), the simpler non-preemptive version.
    Let initial guess = 5 time units.
    Thanks Lee Wei Ping for trying and pointing out the difficulty & ambiguity with future_prediction SRTF.
'''
import sys
from collections import deque

input_file = 'input.txt'

class Process:
    last_scheduled_time = 0
    def __init__(self, id, arrive_time, burst_time):
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time
    #for printing purpose
    def __repr__(self):
        return ('[id %d : arrive_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))

def FCFS_scheduling(process_list):
    #store the (switching time, proccess_id) pair
    schedule = []
    current_time = 0
    waiting_time = 0
    for process in process_list:
        if(current_time < process.arrive_time):
            current_time = process.arrive_time
        schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + process.burst_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

#Input: process_list, time_quantum (Positive Integer)
#Output_1 : Schedule list contains pairs of (time_stamp, proccess_id) indicating the time switching to that proccess_id
#Output_2 : Average Waiting Time
def RR_scheduling(process_list, time_quantum):
    '''
    1. Keep track of curr_time and wait_time similar to FCFS
    2. For each process
        If can finish within time_quantum
            Finish it
        Else
            Finish part of it
        Update curr_time and wait_time
    '''
    num_process = len(process_list)
    schedule = []
    current_time = 0
    waiting_time = 0
    while(len(process_list) > 0):
        process = process_list.pop(0)

        if(current_time < process.arrive_time):
            current_time = process.arrive_time
        schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + min(time_quantum, process.burst_time)

        if process.burst_time > time_quantum:
            # Decide where to append the process. This is a bit more sophisticated than the 
            # actual implementation because here the processes doesn't 'come in.'
            # We have to specifically check the process entries
            ioi = len(process_list)  # index of insertion
            exec_time = 0
            for i, o_process in enumerate(process_list):
                if o_process.arrive_time > current_time:
                    ioi = i
                    break
                exec_time += min(time_quantum, o_process.burst_time)

            process_list.insert(ioi, Process(process.id, current_time, process.burst_time - time_quantum))

    average_waiting_time = waiting_time/float(num_process)
    return schedule, average_waiting_time

def RR_scheduling2(process_list, time_quantum):
    '''
    RR_scheduling with an actual queue
    '''
    schedule = []
    current_time = 0
    waiting_time = 0
    ready_queue = deque() # First process should be inside the ready queue

    curr = 0
    while(len(ready_queue) > 0 or curr < len(process_list)):  # while there's still processes to be executed or there's incoming processes
        # Execute the first process in the queue
        try:
            process = ready_queue.popleft()
        except IndexError:
            # Means ready_queue is empty but there are incoming processes
            ready_queue.append(process_list[curr])
            curr += 1
            continue

        if (current_time < process.arrive_time):
            current_time = process.arrive_time
        schedule.append((current_time, process.id))
        waiting_time += (current_time - process.arrive_time)
        current_time += min(time_quantum, process.burst_time)

        # After execution, check if new processes should go into the ready queue
        while (curr < len(process_list) and process_list[curr].arrive_time <= current_time):
            ready_queue.append(process_list[curr])
            curr += 1

        if process.burst_time > time_quantum:
            ready_queue.append(Process(process.id, current_time, process.burst_time - time_quantum))

    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time
    

def SRTF_scheduling(process_list):
    return (["to be completed, scheduling process_list on SRTF, using process.burst_time to calculate the remaining time of the current process "], 0.0)

def SJF_scheduling(process_list, alpha):
    return (["to be completed, scheduling SJF without using information from process.burst_time"],0.0)


def read_input():
    result = []
    with open(input_file) as f:
        for line in f:
            array = line.split()
            if (len(array)!= 3):
                print ("wrong input format")
                exit()
            result.append(Process(int(array[0]),int(array[1]),int(array[2])))
    return result
def write_output(file_name, schedule, avg_waiting_time):
    with open(file_name,'w') as f:
        for item in schedule:
            f.write(str(item) + '\n')
        f.write('average waiting time %.2f \n'%(avg_waiting_time))


def main(argv):
    process_list = read_input()
    print ("printing input ----")
    for process in process_list:
        print (process)
    print ("simulating FCFS ----")
    FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
    write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )
    print ("simulating RR ----")
    RR_schedule, RR_avg_waiting_time =  RR_scheduling2(process_list,time_quantum = 2)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
    print ("simulating SRTF ----")
    SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
    print ("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )

if __name__ == '__main__':
    main(sys.argv[1:])
