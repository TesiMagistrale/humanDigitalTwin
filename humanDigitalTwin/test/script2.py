import asyncio
from datetime import datetime
import random
import json
import time
import aio_pika
import numpy as np
from log_to_json import JsonFormatter
import logging

ftds = []
start_time = 0
decimals = 4

async def consume_messages():
    global start_time
    # Connect to RabbitMQ
    connection = await aio_pika.connect(
            host= "192.168.3.62", #"localhost",
            port=5675, #docker port
            login="guest",
            password="guest"
        )
    channel = await connection.channel()
    exchange = await channel.declare_exchange('ftdStereotype', 'topic') 
        
  # Declare queue
    queue = await channel.declare_queue("car", auto_delete=True)
    await queue.bind(exchange, "car")
    count = 0
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            data = json.loads(message.body)
            print(data)
            count += 1
            
            if count >= 10:
                await asyncio.sleep(20)
                global group
                group.cancel()
            
    

async def publish_messages(): 
    # Connect to RabbitMQ
    connection = await aio_pika.connect(
            host= "192.168.3.62", #"localhost",
            port=5675, #docker port
            login="guest",
            password="guest"
        )
    channel = await connection.channel()

    # Declare exchange
    exchange = await channel.declare_exchange('ftdStereotype', 'topic')
    for name in ["NP_UNIPR_AROUSAL", "Emotions", "RL_VehicleDynamics", "NP_UNITO_DCDC", "AITEK_EVENTS"]:
        queue = await channel.declare_queue(name+"1", auto_delete=True)
        await queue.bind(exchange, routing_key=name)
    s = 5  # initial speed
    w = 0
    x = 4
    # Publish loop  
    start = time.time()
    for i in range(10):
        for k in range(4):
            s = s + 5

            anger = round(random.random(),decimals) # num casuale tra 0 e 1
            disgust = round(random.uniform(0, 1-anger), decimals)
            fear = round(random.uniform(0, 1-(anger + disgust)), decimals)
            joy = round(random.uniform(0, 1-(anger + disgust + fear)), decimals)
            neutral = round(random.uniform(0, 1-(anger + disgust + fear + joy)), decimals)
            sadness = round(random.uniform(0, 1-(anger + disgust + fear + joy + neutral)), decimals)
            surprise = round(1 - (anger + disgust + fear + joy + neutral + sadness), decimals)

            emotion = {"neutral": neutral, "happiness": joy, "surprise": surprise, "sadness": sadness, "anger": anger, "disgust": disgust, "fear": fear}
            try: 
                for v in range(0, x):
                    await exchange.publish(
                            message=aio_pika.Message(json.dumps(emotion).encode("utf-8")),
                            routing_key="Emotions")
                    await asyncio.sleep(w)
            except Exception as e:
                print(e)
            
            speed = {"speed": str(s)}
            
            for v in range(0, x):
                await exchange.publish(
                        message=aio_pika.Message(json.dumps(speed).encode("utf-8")),
                        routing_key="RL_VehicleDynamics")
                await asyncio.sleep(w)
            
            arousal_topic = [
                {"arousal": 0},
                {"arousal": round(random.random(), decimals)},
                {"arousal": 1}
            ]
            arousal = random.choice(arousal_topic)
            for v in range(0, x):
                await exchange.publish(
                        message=aio_pika.Message(json.dumps(arousal).encode("utf-8")),
                        routing_key="NP_UNIPR_AROUSAL")
                await asyncio.sleep(w)
            
        DV = random.randint(0, 1)
        #if DV != start:
        #    start = DV
        DV_topic = {"timestamp": 1690467368112, "visual_distraction": DV}
            
        for v in range(0, x):
            await exchange.publish(
                        message=aio_pika.Message(json.dumps(DV_topic).encode("utf-8")),
                        routing_key="AITEK_EVENTS")
            await asyncio.sleep(w)
        
        DC = random.randint(0, 1)
        eyesOffRoad = random.randint(0, 1)
        confidence_value = [0.0, round(random.random(), 1)]
        DC_topic = {"timestamp": 1690467368112, "eyesOffRoad": eyesOffRoad, "cognitive_distraction": DC,
                                "eyesOffRoad_confidence": random.choice(confidence_value),
                                "cognitive_distraction_confidence": random.choice(confidence_value),
                                "eyesOffRoad_pred_1s": 0.0, "cognitive_distraction_pred_1s": 0.0}
        for v in range(0, x):
            await exchange.publish(
                        message=aio_pika.Message(json.dumps(DC_topic).encode("utf-8")),
                        routing_key="NP_UNITO_DCDC")
            await asyncio.sleep(w)
        
    end = time.time()
    await asyncio.sleep(5)
    print(f" ------- send time = {end - start} -------")

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
        for t in asyncio.all_tasks():
            t.cancel()
        print("finished")

asyncio.run(main())