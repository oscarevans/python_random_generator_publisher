#Application 3: Printer##

import paho.mqtt.client as mqtt
import datetime
import os

#set file size limit to 20MB
file_size_limit = 20000000

file_name = '/home/ubuntu/averages.log'

def on_message(client, userdata, msg):
    messageRecieved = datetime.datetime.now()
    averages = str(msg.payload).split('\'')[1]

    averagesList = averages.split(',')

    #check if file needs to be truncated
    logStats = os.stat(file_name)

    if logStats.st_size > file_size_limit:
        with open(file_name, 'w') as averagesLog:
            averagesLog.truncate()

    # print to console or save to a file
    with open(file_name, 'a') as averagesLog:
        # write data to file
        averagesLog.write("Updated averages recieved at: "+
                str(messageRecieved)+
                "\n | 1 minute average: "+averagesList[0]+
                " | 5 minute average: "+averagesList[1]+
                " | 30 minute average: "+averagesList[2]+
                "\n--------------------------------------------------------------------------------------------------------------------\n")

##mqtt connections:
client = mqtt.Client()
client.username_pw_set("oscar", "password1")
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.subscribe('averagesq')

client.loop_forever()