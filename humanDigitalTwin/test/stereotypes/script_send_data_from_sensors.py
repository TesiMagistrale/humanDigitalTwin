import random
import pika
import json
import time

decimals = 4
start = 0
s = 5  # initial speed

# Callback function to process received messages
def callback(ch, method, properties, body):
    pass  # Replace with your message processing logic

# Connection parameters
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost', 5672, credentials=credentials)

# Establish a connection to RabbitMQ
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Declare an exchange for the publish-subscribe pattern
exchange_name = 'ftdStereotype'
channel.exchange_declare(exchange=exchange_name, exchange_type='topic')

for name in ["NP_UNIPR_AROUSAL", "Emotions", "RL_VehicleDynamics", "NP_UNITO_DCDC", "AITEK_EVENTS"]:
    channel.queue_declare(queue=name, auto_delete=True)

#time.sleep(10) #used for starting the client

for i in range(5):
    for k in range(4):
        s = s + 5

        anger = round(random.random(),decimals) # num casuale tra 0 e 1
        disgust = round(random.uniform(0, 1-anger), decimals)
        fear = round(random.uniform(0, 1-(anger + disgust)), decimals)
        joy = round(random.uniform(0, 1-(anger + disgust + fear)), decimals)
        neutral = round(random.uniform(0, 1-(anger + disgust + fear + joy)), decimals)
        sadness = round(random.uniform(0, 1-(anger + disgust + fear + joy + neutral)), decimals)
        surprise = round(1 - (anger + disgust + fear + joy + neutral + sadness), decimals)

        emotion = json.dumps({"neutral": str(neutral), "happiness": str(joy), "surprise": str(surprise), "sadness": str(sadness), "anger": str(anger), "disgust": str(disgust), "fear": str(fear)})
        speed = json.dumps({"speed": str(s)})
        arousal_topic = [
            json.dumps({"arousal": 0}),
            json.dumps({"arousal": round(random.random(), decimals)}),
            json.dumps({"arousal": 1}),
        ]
        arousal = random.choice(arousal_topic)

        # Publish messages
        channel.basic_publish(exchange=exchange_name, routing_key='NP_UNIPR_AROUSAL', body=arousal)
        channel.basic_publish(exchange=exchange_name, routing_key='Emotions', body=emotion)
        channel.basic_publish(exchange=exchange_name, routing_key='RL_VehicleDynamics', body=speed)

    DC = random.randint(0, 1)
    eyesOffRoad = random.randint(0, 1)
    confidence_value = [0.0, round(random.random(), 1)]
    DC_topic = json.dumps({"timestamp": 1690467368112, "eyesOffRoad": eyesOffRoad, "cognitive_distraction": DC,
                            "eyesOffRoad_confidence": random.choice(confidence_value),
                            "cognitive_distraction_confidence": random.choice(confidence_value),
                            "eyesOffRoad_pred_1s": 0.0, "cognitive_distraction_pred_1s": 0.0})
    channel.basic_publish(exchange=exchange_name, routing_key='NP_UNITO_DCDC', body=DC_topic)

    DV = random.randint(0, 1)
    if DV != start:
        start = DV
    DV_topic = json.dumps({"timestamp": 1690467368112, "visual_distraction": str(DV)})

    channel.basic_publish(exchange=exchange_name, routing_key='AITEK_EVENTS', body=DV_topic)

    time.sleep(5)
    print(f"cicle {i}")
    
connection.close()
