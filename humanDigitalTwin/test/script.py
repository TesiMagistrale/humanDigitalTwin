import asyncio
from datetime import datetime
import random
import json
import aio_pika
import numpy as np

random.seed(17)
decimals = 4

FTD = 1
ftds = []
istant = 0
infraction = []

def speed_function(time):
    time_seconds = time * 60  # Conversione in secondi
    if 0 <= time_seconds <= 20:
        return 30
    elif 20 < time_seconds <= 35:
        return 30 + (time_seconds - 20) * (55 - 30) / (35 - 20)
    elif 35 < time_seconds <= 43:
        return 55 - (time_seconds - 35) * (55 - 30) / (43 - 35)
    else:
        return 30

def cd_function(t):
  if 0 <= t <= 0.25 or t >= 0.6:
    return 0
  elif 0.25 < t <= 0.35:
    return 0
  elif 0.35 < t < 0.6:
    return 1

def vd_function(t):
  if 0 <= t <= 0.25 or t >= 0.6:
    return 0
  elif 0.25 < t <= 0.4:
    return 1
  elif 0.4 < t < 0.6:
    return 0

time_points = np.linspace(0, 2, num=240) #quattro campionamenti di velocità al secondo
speed_values = [speed_function(t) for t in time_points]

#cd_val = [cd_function(t) for t in time_points]
#vd_val = [vd_function(t) for t in time_points]


cd_val = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 
vd_val = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


async def consume_messages():
  
    # Connect to RabbitMQ
    connection = await aio_pika.connect(
            host="localhost",
            port=5672,
            login="guest",
            password="guest"
        )
    channel = await connection.channel()
    exchange = await channel.declare_exchange('ftdStereotype', 'topic')     
  # Declare queue
    queue = await channel.declare_queue("car", auto_delete=True)
    await queue.bind(exchange, "car")

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            data = json.loads(message.body)  

            global FTD, ftds, infraction
            FTD = int(data["ftd"])
            ftds.append(json.dumps(data))
            print(json.dumps(data) + ",")

            await message.ack()
            if len(ftds) == len(cd_val):
                global group
                group.cancel()

async def publish_messages():
    global FTD, istant, infraction

    # Connect to RabbitMQ
    connection = await aio_pika.connect(
            host="localhost",
            port=5672,
            login="guest",
            password="guest"
        )
    channel = await connection.channel()

    # Declare exchange
    exchange = await channel.declare_exchange('ftdStereotype', 'topic')
    for name in ["NP_UNIPR_AROUSAL", "Emotions", "RL_VehicleDynamics", "NP_UNITO_DCDC", "AITEK_EVENTS"]:
        queue = await channel.declare_queue(name, auto_delete=True)
        await queue.bind(exchange, routing_key=name)

    # Publish loop
    for i in range(0, len(speed_values)-1):
    
        anger = round(random.random(),decimals) # num casuale tra 0 e 1
        disgust = round(random.uniform(0, 1-anger), decimals)
        fear = round(random.uniform(0, 1-(anger + disgust)), decimals)
        joy = round(random.uniform(0, 1-(anger + disgust + fear)), decimals)
        neutral = round(random.uniform(0, 1-(anger + disgust + fear + joy)), decimals)
        sadness = round(random.uniform(0, 1-(anger + disgust + fear + joy + neutral)), decimals)
        surprise = round(1 - (anger + disgust + fear + joy + neutral + sadness), decimals)

        emotion = json.dumps({"neutral": str(neutral), "happiness": str(joy), "surprise": str(surprise), "sadness": str(sadness), "anger": str(anger), "disgust": str(disgust), "fear": str(fear)})
        speed = json.dumps({"speed": str(speed_values[i])})
        arousal_topic = [
            json.dumps({"arousal": 0}),
            #json.dumps({"arousal": round(random.random(), decimals)}),
            #json.dumps({"arousal": 1}),
        ]
        arousal = random.choice(arousal_topic)

        # Publish
        await exchange.publish(
            message=aio_pika.Message(arousal.encode("utf-8")),
            routing_key="NP_UNIPR_AROUSAL")
        await exchange.publish(
            message=aio_pika.Message(emotion.encode("utf-8")),
            routing_key="Emotions")
        await exchange.publish(
            message=aio_pika.Message(speed.encode("utf-8")),
            routing_key="RL_VehicleDynamics")
            
        if i % 4 == 0:
            DC = cd_val[int(i/4)]
            DV = vd_val[int(i/4)]
            DC_topic = json.dumps({"timestamp": int(datetime.now().timestamp() * 1000), "eyesOffRoad": 0, "cognitive_distraction": DC,
                                "eyesOffRoad_confidence": 0,
                                "cognitive_distraction_confidence": 0,
                                "eyesOffRoad_pred_1s": 0.0, "cognitive_distraction_pred_1s": 0.0}).encode("utf-8")    
            await exchange.publish(
                message=aio_pika.Message(DC_topic),
                routing_key="NP_UNITO_DCDC")
            
            DV_topic = json.dumps({"timestamp": int(datetime.now().timestamp() * 1000), "visual_distraction": str(DV)}).encode("utf-8")
            
            await exchange.publish(
                message=aio_pika.Message(DV_topic),
                routing_key="AITEK_EVENTS")

            await asyncio.sleep(1)

async def main():
    global group
    tasks = [
      consume_messages(),  
      publish_messages()
    ]
    try:
        group = asyncio.gather(*tasks)
        await group
    except asyncio.CancelledError:
        print("finished")
    
    

asyncio.run(main())