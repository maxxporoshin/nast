import time
import Queue
from threading import Thread
import random


class Job:
    def __init__(self, id, type, st_time, finish=False):
        self.st_time =  st_time
        self.to_queue = 0
        self.start_process = 0
        self.finish_process = 0
        self.finish = finish
        self.id = id
        self.type = type
        self.conv_id = None

    def __str__(self):
        return "type " + str(self.type) + " conv_id " + str(self.conv_id) +  ", creation_time " + str(self.st_time)+ \
               ", start_time " + str(self.start_process) + ' - ' + str(self.finish_process)


class Converner:
    def __init__(self, id, process_time):
        self.id = id
        self.queue = Queue.Queue()
        self.mean_process_time = process_time
        self.last_process_time = 0

    def add_to_queue(self, job):
        job.conv_id = self.id
        self.queue.put(job)
        self.process()

    def process(self):
        job = self.queue.get(block = True)
        if job.finish:
            return
        job.start_process = max(self.last_process_time, job.st_time)
        job.finish_process = job.start_process + random.expovariate(1.0 / self.mean_process_time[job.type])
        self.last_process_time = job.finish_process

    def run(self):
        while True:
            job = self.queue.get(block = True)
            if job.finish:
                break
            job.start_process = max(self.last_process_time, job.st_time)
            job.finish_process = job.start_process + random.expovariate(1.0 / self.mean_process_time[job.type])

            self.last_process_time = job.finish_process
            #print job.id, job.start_process, job

    def empty(self, job):
        if job.st_time > self.last_process_time:
            return False
        return True


class Adapter:
    def __init__(self, convers):
        self.convers = convers

    def add_func(self, job):
        if job.type == 1 and not self.convers[1].empty(job):
            self.convers[0].add_to_queue(job)
        else:
            self.convers[job.type].add_to_queue(job)

    def finish(self):
        for conv in self.converts:
            f_job = Job(0, 0, True)
            conv.add_to_queue(f_job)


def main():
    conv1 = Converner(0, [15, 25])
    conv2 = Converner(1, [0, 20])

    adapter = Adapter([conv1, conv2])
    #th1 = Thread(target=conv1.run)
    #th2 = Thread(target=conv2.run)
    #th1.start()
    #th2.start()


    #Poisson time
    n = 10

    jobs = []
    t = 0
    creation = 0
    for i in range(n):
        t = random.expovariate(0.067)
        creation += t

        type = 0 if random.random() <= 0.4 else 1
        job = Job(i, type, creation)
        adapter.add_func(job)
        time.sleep(t * 0.01)
        jobs.append(job)

    delay = 0

    for job in jobs:
        print job
        delay += job.start_process - job.st_time

    print "Delay " + str(delay)

    #th1.join()
    #th2.join()

main()

