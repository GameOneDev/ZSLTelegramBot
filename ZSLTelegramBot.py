import random   
import answers
import config
import datetime
from gpiozero import CPUTemperature
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import time
import asyncio


bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
cpu = CPUTemperature()


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
    if msg.text.lower() in answers.user_answerstext_hello:
        await msg.answer(random.choice(answers.bot_text_hello) + '! Cpu temperature: ' + str(cpu.temperature))
    
    #bot answer on help message
    elif msg.text.lower() == "help" or  msg.text.lower() == "/start":
        await msg.answer("Commands to use: Hello: just write (hello) and bot write to you server cpu temperature Alarm: just write time like (10:30) Helo: just write (help) and bot will show you this help")
        
    #alarm
    
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
        await msg.answer("day in sec: " + str(timer_day_in_sec) + "hour in sec: " + str(timer_hour_in_sec) + " minutes in sec: " + str(timer_min_in_sec))
        
        timer_sec = timer_day_in_sec + timer_hour_in_sec + timer_min_in_sec - datetime.datetime.now().second
        await msg.answer("Alarm set on " + str(timer_sec) + "sec")
        if int(timer_sec) > 0 and int(alarm_hour) <= 24 and int(alarm_minutes) <= 60:
            await asyncio.sleep(timer_sec)
            await msg.answer("!!!alarm!!!" + str(alarm_text))
        else:
            await msg.answer("Something is wrong(in 99% you write wrong alarm time)")
    
    #bot answer on info message
    elif msg.text.lower() == "info":
        await msg.answer("Time on server: " + str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute) + ":" + str(datetime.datetime.now().second))
        await msg.answer('Cpu temperature: ' + str(cpu.temperature) + "℃")


    else:
            await msg.answer("Lol")

if __name__ == '__main__':
    executor.start_polling(dp)
