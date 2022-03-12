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
    mssegx = msg.text.split(":", 2)
    if msg.text.lower() in answers.user_answerstext_hello:
        await msg.answer('Hello! Cpu temperature: ' + str(cpu.temperature))
        await asyncio.sleep(5)
        await msg.answer('Cpu temperature: ' + str(cpu.temperature))

    elif msg.text.lower() == "help" or  msg.text.lower() == "/start":
        await msg.answer("Commands to use: Hello: just write (hello) and bot write to you server cpu temperature Alarm: just write time like (10:30) Helo: just write (help) and bot will show you this help")
        

    elif len(mssegx) >= 2:
        alarm_hour = mssegx[0]
        alarm_minutes = mssegx[1]
        try:
            alarm_text = mssegx[2]
        except:
            alarm_text = " "
        await msg.answer("Time on server: " + str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute) + ":" + str(datetime.datetime.now().second))
        timer_hour_in_sec = (int(alarm_hour) - datetime.datetime.now().hour)*3600
        timer_min_in_sec = (int(alarm_minutes) - datetime.datetime.now().minute)*60
        timer_sec = timer_hour_in_sec + timer_min_in_sec - datetime.datetime.now().second
        if int(timer_sec) > 0 and int(alarm_hour) <= 24 and int(alarm_minutes) <= 60:
            await msg.answer("hour in sec: " + str(timer_hour_in_sec) + " minutes in sec: " + str(timer_min_in_sec))
            await msg.answer("Alarm set on " + str(timer_sec) + "sec")
            await asyncio.sleep(timer_sec)
            await msg.answer("!!!alarm!!!" + str(alarm_text))
        else:
            await msg.answer("Something is wrong(in 99% you write wrong alarm time)")

    elif msg.text.lower() == "info":
        await msg.answer("Time on server: " + str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute) + ":" + str(datetime.datetime.now().second))
        await msg.answer('Cpu temperature: ' + str(cpu.temperature) + "℃")


    else:
            await msg.answer("Lol")

if __name__ == '__main__':
    executor.start_polling(dp)
