def info_command():
    msg.answer("Time on server: " + str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute) + ":" + str(datetime.datetime.now().second))
    msg.answer('Cpu temperature: ' + str(cpu.temperature) + "℃")