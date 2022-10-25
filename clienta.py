import paho.mqtt.client as mqtt
import time,logging
broker="192.168.1.68"
home_topic="client_a"
port=1883
QOS=0

CLEAN_SESSION=True
logging.basicConfig(level=logging.INFO) #error logging
#use DEBUG,INFO,WARNING
def on_subscribe(client, userdata, mid, granted_qos):   #create function for callback
   #print("subscribed with qos",granted_qos, "\n")
   time.sleep(1)
   logging.info("sub acknowledge message id="+str(mid))
   pass

def on_disconnect(client, userdata,rc=0):
    logging.info("DisConnected result code "+str(rc))


def on_connect(client, userdata, flags, rc):
    logging.info("Connected flags"+str(flags)+"result code "+str(rc))



def on_message(client, userdata, message):
    msg=str(message.payload.decode("utf-8"))
    print("topic= "+message.topic)
    topics=(message.topic).split("/")
    print("message received  "  +msg+ " from " +topics[2])
    if topics[1]==home_topic: #is it for me
       reply_topic="base/" +home_topic+"/"+topics[2]
       client.publish("received your message")
    
def on_publish(client, userdata, mid):
    logging.info("message published "  +str(mid))

send_topic ="house/client_b/" +home_topic
client= mqtt.Client("ClientA",False)       #create client object

client.on_subscribe = on_subscribe   #assign function to callback
client.on_disconnect = on_disconnect #assign function to callback
client.on_connect = on_connect #assign function to callback
client.on_message=on_message
client.connect(broker,port)           #establish connection
time.sleep(1)
client.loop_start()
client.subscribe("house/#")
count=1
while True: #runs forever break with CTRL+C
   print("publishing on topic ",send_topic)
   msg="message " +str(count) + " from client A"
   client.publish(send_topic,msg)
   count +=1
   time.sleep(5)
client.disconnect()

client.loop_stop()

