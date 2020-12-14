import os
import time
import sys
import csv
from redis import Redis
from rq import Connection, Queue
from test_job import job
from rq.job import Job
import time

if __name__ == '__main__':
    #다운로드 큐 생성
    q=Queue(connection=Redis())

    job=q.enqueue(job,job_timeout=10800)