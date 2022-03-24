from ast import excepthandler
import random
import values
import config
import datetime
from gpiozero import CPUTemperature
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import time
import asyncio
import sqlite3
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'bot.sqlite')

conn = sqlite3.connect(my_file)
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
cpu = CPUTemperature()
scheduler = AsyncIOScheduler()


@dp.message_handler(content_types=['text'])
async def get_text_messages(msg: types.Message):
    #for alarm
    #msg_alarm_day = msg.text.split("/", 0)[:1]
    #msg_alarm_time = msg.text.split(":", 1)[:2]
    #msg_alarm_text = msg.text.split(" ", 0)
    msg_alarm_helper = msg.text.split(" ", 1)#split text on 2 parts (day/ h:m) and (alarm_text)
    msg_alarm_helper2 = msg_alarm_helper[0].split("/", 1)#split msg_alarm_helper(day/ h:m) on 2 parts (day) and (h:m)
    if len(msg_alarm_helper2) > 1:
        msg_alarm_time = msg_alarm_helper2[1].split(":", 1)
        alarm_day = msg_alarm_helper2[0]
    else:
        msg_alarm_time = msg_alarm_helper2[0].split(":", 1)
        alarm_day = 0
    
    #bot answer on hello message
    if msg.text.lower() in values.user_answerstext_hello:
        await msg.answer(random.choice(values.bot_text_hello) + '! Cpu temperature: ' + str(cpu.temperature))
    
    #bot answer on help message
    elif msg.text.lower() == "help" or  msg.text.lower() == "/start":
        await msg.answer("Commands to use: Hello: just write (hello) and bot write to you server cpu temperature Alarm: just write time like (10:30) Helo: just write (help) and bot will show you this help")
        
    
    
    #############################################info command#################################################
    elif msg.text.lower() == "info":
        await msg.answer("Time on server: " + str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute) + ":" + str(datetime.datetime.now().second))
        await msg.answer('Cpu temperature: ' + str(cpu.temperature) + "℃")

    #####################################database############################################################################
    elif msg.text.lower() == "testdb":
        cursor = conn.cursor()
        day_of_week = datetime.datetime.today().weekday()+1 #day of week
    

        cursor.execute("SELECT * FROM Plan_lekcji_2PT WHERE dzien LIKE :dzien", {"dzien": day_of_week})

        results = cursor.fetchall()
        await msg.answer(results)
        #conn.close()
    #########"Plan Lekcji"#####################
    elif msg_alarm_helper[0] == "plan":
        cursor = conn.cursor()

        msg_alarm_time = msg_alarm_helper[1].split(":", 1)
        day_of_week = datetime.datetime.today().weekday()+1 #day of week
        time_hour_now = datetime.datetime.today().hour
        time_min_now = datetime.datetime.today().minute
        
        if (int(msg_alarm_time[0]) < 10): msg_alarm_time[0] = "0" + str(msg_alarm_time[0])
        if (int(msg_alarm_time[1]) < 10): msg_alarm_time[1] = "0" + str(msg_alarm_time[1])

        if (time_hour_now < 10): time_hour_now = "0" + str(time_hour_now)
        if (time_min_now < 10): time_min_now = "0" + str(time_min_now)
        #syeta
        try:
            time_lekcja_now = (values.time_lekcja[msg_alarm_helper[1]])
            #if (time_lekcja_now < 10): time_lekcja_now = "0" + str(time_lekcja_now)
        except:
            try:
                time_now = str(time_hour_now)+":"+str(time_min_now)
                time_lekcja_now = (values.time_lekcja[time_now])
            except:
                await msg.answer("error 404, time_lekcja or incorrect date")

        await msg.answer(str(time_lekcja_now)+"test")


        sql2 = "SELECT "+time_lekcja_now+" FROM Plan_lekcji_2PT"+" WHERE dzien LIKE "+str(day_of_week)
        cursor.execute(sql2)
        results2 = cursor.fetchall()
        
        #########
        alarm_hour = msg_alarm_time[0]
        alarm_minutes = msg_alarm_time[1]
        #try to set alarm text
        try:
            alarm_text = results2
        except:
            alarm_text = " "
        await msg.answer("Time on server: " + str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute) + ":" + str(datetime.datetime.now().second))
        timer_hour_in_sec = (int(alarm_hour) - datetime.datetime.now().hour)*3600
        timer_min_in_sec = (45+int(alarm_minutes) - datetime.datetime.now().minute)*60
        timer_day_in_sec = int(alarm_day)*86400
        await msg.answer("day in sec: " + str(timer_day_in_sec) + ", hour in sec: " + str(timer_hour_in_sec) + ", minutes in sec: " + str(timer_min_in_sec))
        timer_sec = timer_day_in_sec + timer_hour_in_sec + timer_min_in_sec - datetime.datetime.now().second#-30
        await msg.answer("Alarm set on " + str(timer_sec) + "sec")
        if int(timer_sec) > 0 and int(alarm_hour) <= 24 and int(alarm_minutes) <= 60:
            await asyncio.sleep(timer_sec)
            await msg.answer("Next lection: " + str(alarm_text))
        else:
            await msg.answer("Something is wrong(in 99% you write wrong alarm time)")
        ##########
        
        await msg.answer(str(results2)+"db, "+alarm_hour+alarm_minutes)

    
    #################################################alarm command###############################################################
    
    elif len(msg_alarm_helper) >= 1 and len(msg_alarm_helper2) >= 0:
        alarm_hour = msg_alarm_time[0]
        alarm_minutes = msg_alarm_time[1]
        #try to set alarm text
        try:
            alarm_text = msg_alarm_helper[1]
        except:
            alarm_text = " "
        await msg.answer("Time on server: " + str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute) + ":" + str(datetime.datetime.now().second))
        timer_hour_in_sec = (int(alarm_hour) - datetime.datetime.now().hour)*3600
        timer_min_in_sec = (int(alarm_minutes) - datetime.datetime.now().minute)*60
        timer_day_in_sec = int(alarm_day)*86400
        await msg.answer("day in sec: " + str(timer_day_in_sec) + ", hour in sec: " + str(timer_hour_in_sec) + ", minutes in sec: " + str(timer_min_in_sec))
        timer_sec = timer_day_in_sec + timer_hour_in_sec + timer_min_in_sec - datetime.datetime.now().second
        await msg.answer("Alarm set on " + str(timer_sec) + "sec")
        if int(timer_sec) > 0 and int(alarm_hour) <= 24 and int(alarm_minutes) <= 60:
            await asyncio.sleep(timer_sec)
            await msg.answer("!!!alarm!!!" + str(alarm_text))
        else:
            await msg.answer("Something is wrong(in 99% you write wrong alarm time)")

    else:
            await msg.answer("Lol")



if __name__ == '__main__':
    executor.start_polling(dp)
