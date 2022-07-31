#Application 2: Data analytics:


""" for X mins:
grab now - X mins of values, add them up and divide by count
execute this for 1, 5 and 30 minutes.
this application has to read from the queue, stores the data and calculate
1, 5 and 30 minute averages.
should then send back to broker on different queue
"""

import time
import datetime
import paho.mqtt.client as mqtt

data = []

# calculate averages over the period specified by periodMins (in minutes)
def average(time, periodMins):
    timeframe = (time-datetime.timedelta(minutes=periodMins))
    values=[]

    # new values are appended, so iterate through list backwards and stop when the condition is no longer true
    for row in data[::-1]:
        if row[0] > timeframe:
            values.append(row[1])

    # calculate and return the average
    average = sum(values) / len(values)
    return average

# keep the list manageable by removing values we are not interested in
def clean_list(time):
    timeframe = (time-datetime.timedelta(minutes=30))
    dataCopy = data
    for row in dataCopy:
        if row[0] < timeframe:
            data.remove(row)

# when a message is recieved on the queue, append it to the data, calculate the averages and publish these values
def on_message(client, userdata, msg):
    messageRecieved = datetime.datetime.now()
    randomNumber = msg.payload
    data.append([messageRecieved, float(str(msg.payload).split('\'')[1])])
    one_min_av = average(messageRecieved, 1)
    five_min_av = average(messageRecieved, 5)
    thirty_min_av = average(messageRecieved, 30)
    client.publish('averagesq',str(one_min_av)+','+str(five_min_av)+','+str(thirty_min_av))
    # clean up the list
    clean_list(messageRecieved)

##mqtt connections
client = mqtt.Client()
client.username_pw_set("oscar", "password1")
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.subscribe('randomq')
client.loop_forever()