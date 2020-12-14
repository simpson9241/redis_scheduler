import os
import time
import sys
import csv
from redis import Redis
from rq import Connection, Queue
from job import encode
from rq.job import Job
import time

if __name__ == '__main__':
    #Input CSV 파일 열기
    #Input CSV 파일 이름은 프로그램을 실행할 때 인자로 받음
    #Example. python3 server.py showbox.csv
    input_csv=open(sys.argv[1],'r',encoding="utf-8")

    #input CSV 파일 이름 저장
    input=sys.argv[1]

    #input CSV 파일의 확장자 분리
    #Example. input filename="showbox.csv" -> input="showbox"
    temp_input=input.split('.')
    input=temp_input[0]

    #output CSV 파일의 이름 생성
    #Example. input filename="showbox.csv" -> output filename="showbox_output.csv"
    output_name=input+"_output"

    #input CSV 파일을 읽어들이는 변수 생성
    reader=csv.reader(input_csv)

    #생성된 Job 들의 Job ID와 Job Status를 저장해놓을 리스트 변수 생성
    #하나의 Entry는 다음과 같이 구성됨 (Job_ID, Job_Status)
    job_list=[]

    #다운로드 큐 생성
    encode_q=Queue(connection=Redis())

    #input CSV에서 값을 읽어들여 download_q에 하나씩 추가
    #input CSV의 한 entry는 (link, filename)으로 이루어져있음
    for entry in reader:
        job=encode_q.enqueue(encode,entry,job_timeout=10800)

        #job_list에 생성된 Job의 ID와 큐에 추가되었다는 뜻의 메시지를 한 Tuple로 job_list에 추가
        job_list.append((job.id,"queued"))

    #큐에 들어있던 Job이 모두 끝나고 프로그램이 종료되도 된다는 신호를 주는 Flag 생성
    done=False

    #프로그램이 종료될 때까지 큐의 진행상황을 output CSV 파일에 업데이트 시켜주는 코드
    #while 문은 60초 마다 반복
    while not done:
        #input CSV 파일을 읽어들임
        input_csv=open(sys.argv[1],'r',encoding="utf-8")
        reader=csv.reader(input_csv)

        #output CSV 파일을 생성하고 CSV 파일을 작성해주는 writer 변수 생성
        #여러번 생성되면 있던 CSV 파일에 그대로 덮어씌워지므로 CSV 파일이 업데이트되는 것과 같은 효과를 보여줌
        output_csv=open(output_name,'w',encoding='utf-8')
        writer=csv.writer(output_csv)

        #job list의 인덱스 생성
        i=0
        for entry in reader:
            job_id=job_list[i][0]
            job_status=job_list[i][1]

            #job_status가 finished 이거나 failed 이면 큐에서 Job id로 Job을 호출하지 않고 CSV 파일에 기존 내용을 그대로 작성
            #그렇지 않은 경우 job list에 저장되어 있던 Job ID로 Job을 호출해서 현재 상태를 가지고 와서 상태를 업데이트 해줌
            #큐의 마지막 Job까지 모두 finished로 업데이트 되면 done=True가 되어서 while문을 탈출 후 프로그램 종료
            if job_status=="finished":
                writer.writerow([entry[0],entry[1],job_status])
                done=True
            elif job_status=="failed":
                writer.writerow([entry[0],entry[1],job_status])
                done=True
            else:
                #Job의 상태가 바뀐 경우 Job ID로 Job을 가지고 와서 현재 상태를 받아온 후 output CSV 파일과 job_list에 업데이트를 해준다.
                job=Job.fetch(job_id,connection=Redis())
                current_status=job.get_status()
                writer.writerow([entry[0],entry[1],current_status])
                job_list[i]=(job_id,current_status)
                done=False
            i+=1
        time.sleep(60)
