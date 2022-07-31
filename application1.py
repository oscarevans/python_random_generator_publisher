#Application 1: Random Number Generator##

import random
import time
import paho.mqtt.client as mqtt

minVal = 1
maxVal = 100

minPub = 1
maxPub = 30

##mqtt connections
client = mqtt.Client()
client.username_pw_set("oscar", "password1")
client.connect("localhost", 1883, 60)

## loop forever
while True:
    # Generate random number
    rand = random.uniform(minVal, maxVal)

    #publish random number
    client.publish('randomq', rand)

    #wait for between 1 and 30 seconds to generate another number
    wait = random.randrange(minPub, maxPub + 1)
    time.sleep(wait)