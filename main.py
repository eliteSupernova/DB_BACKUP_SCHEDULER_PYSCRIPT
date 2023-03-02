import gzip
import json
import os
import shutil
import subprocess
import time
import pipes
import datetime
import zipfile
import schedule

import mysql.connector

# DB VARIABLES FOR CMD QUERY

# DB_NAME = []
def backup():
    file=open('C:\\Users\\1003647\\Desktop\\FLASK_API\\Backup\\config.json','r')
    data=json.load(file)
    print(data["db"])
    DB_HOST = data["host"]
    DB_USER = data["user"]
    DB_USER_PASSWORD = data["password"]
    DB_NAME = data["db"]


    now = datetime.datetime.now()
    previous=now-datetime.timedelta(days=1)

    chdir=os.chdir("..\\..\\Documents\\Backup\\")

    dump='"C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysqldump.exe"'
    today_backup=str(now.date())+'\\'
    previous_backup=str(previous.date())

    print ("checking for databases names file.")
    try:
        os.stat(str(now.date()))
    except:
        os.mkdir(str(now.date()))

    if os.path.exists(today_backup):
        for i in DB_NAME:
            cmd_dump=dump+" -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + i + ' > '+today_backup+ i +"_"+str(now.date())+ '.sql"'
            subprocess.Popen(cmd_dump,shell=True)
            time.sleep(2)
            zip=zipfile.ZipFile(today_backup+i +"_"+str(now.date())+'.zip','w')
            zip.write(today_backup+i +"_"+str(now.date())+ '.sql')

            print("Backup done")
    # try:
    #     if os.stat(previous_backup):
    #         shutil.rmtree(previous_backup,ignore_errors=True)
    # except FileNotFoundError:
    #     print("file Not found")
    else:
        for i in DB_NAME:
            conn = mysql.connector.connect(user=data["user"], password=data["password"], host=data["host"], database=i)
            cmd_dump = dump + " -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + i + ' > "' + today_backup + "_" + "" + i + "_" + str(now.date())+'.sql"'
            print(cmd_dump)
            subprocess.Popen(cmd_dump, shell=True)
            time.sleep(1)
            zip = zipfile.ZipFile(today_backup + i + "_" + str(now.date()) + '.zip', 'w')
            zip.write(today_backup + i + "_" + str(now.date()) + '.sql')
        print("backup done")
    # try:
    #     if os.stat(previous_backup):
    #         shutil.rmtree(previous_backup,ignore_errors=True)
    # except FileNotFoundError:
    #     print("file Not found")
    if os.path.exists(previous_backup):
        shutil.rmtree(previous_backup)
        print(previous_backup+" folder is deleted")

schedule.every(10).seconds.do(backup)
while True:
    schedule.run_pending()
    time.sleep(1)
