import pytz
from datetime import datetime
import random
import csv

zn = []
times=[] #промежутки рассылки
next_send = 0 #следующее время рассылки
id_send=0 #id временного промежутка

def get_time():	
	hour = int(datetime.now(pytz.timezone('Europe/Moscow')).strftime("%H"))
	minute = int(datetime.now(pytz.timezone('Europe/Moscow')).strftime("%M"))
	return hour*60+minute


def update_conf():
	zn.clear()
	times.clear()
	with open("conf.csv", encoding='utf-8') as r_file:
		file_reader = csv.reader(r_file, delimiter = ";")
		for i in file_reader:
			zn.append(i)
		for i in range(len(zn[0])):
			if('время вопроса' in zn[0][i]):
				times.append(zn[1][i])


def update_time():
	global id_send
	global next_send
	time1=int(times[id_send].split('-')[0].split(':')[0])*60+int(times[id_send].split('-')[0].split(':')[1])
	time2=int(times[id_send].split('-')[1].split(':')[0])*60+int(times[id_send].split('-')[1].split(':')[1])
	next_send = random.randint(time1,time2)
	if(id_send!=len(times)-1):
		id_send+=1
	else:
		id_send=0


update_conf()
update_time()