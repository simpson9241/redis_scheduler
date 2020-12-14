import csv
import os
import sys

#다운로드 Job 함수
#entry는 input CSV 파일에서 한 줄을 읽어 저장한 변수 (link_url, filename)
def encode(entry):
    link=entry[0]
    filename=entry[1]

    #wget [link_url] String 변수 생성
    temp="wget '{0}'".format(link)
    # print(temp)

    #wget 명령어 실행해서 다운로드 진행
    error=os.system(temp)

    #처음 다운받을 때에는 url의 일부로 파일명이 저장되기 때문에 filename으로 파일명을 바꿔야함
    temp_link=link.split('/')
    temp_name_1=temp_link[-1].split('filename=')
    temp_name_2=temp_name_1[-1].split('&openfolder=')
    name=temp_name_1[0]+"filename="+filename+"&openfolder="+'&'.join(temp_name_2[1:])
    # print(name)

    #mv 명령문 완성시키기
    temp="mv "+'"'+name+'" '+ '"'+filename+'"'
    # print(temp)

    #파일명 변경
    os.system(temp)
