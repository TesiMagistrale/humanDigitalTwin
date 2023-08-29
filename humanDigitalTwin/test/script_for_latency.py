import asyncio
from datetime import datetime
import random
import json
import time
import aio_pika
import numpy as np
from log_to_json import JsonFormatter
import logging

def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)        

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger, handler


json_formatter = JsonFormatter(
    #keys=("message", "name")
)


# second file logger
logger_output, handler_output = None, None
logger_topic, handler_topic = None, None

ftds = []
start_time = 0

async def consume_messages():
    global start_time
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
            print(time.time() - start_time)

            global group
            group.cancel()
    

async def publish_messages():
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
        queue = await channel.declare_queue(name+"1", auto_delete=True)
        await queue.bind(exchange, routing_key=name)
    
    # Publish loop    
    import os
    file_name = "simu_log_elab.log"
    with open((os.path.dirname(os.path.abspath(__file__)) + "/"+ file_name).replace ('\\', '/'),'r') as file:
        for line in file:
            row = json.loads(line)
            topic = row["topic"]
            msg = row["msg"]
            if topic in ["RL_VehicleDynamics", "NP_UNITO_DCDC", "AITEK_EVENTS"]:
                await exchange.publish(
                    message=aio_pika.Message(json.dumps(msg).encode("utf-8")),
                    routing_key=topic)
            
            if topic == "NP_UNITO_DCDC":
                global start_time
                start_time = time.time()
                await asyncio.sleep(1)

async def main():
    global group, logger_output, logger_topic
    logger_output, handler_output = setup_logger('output_logger', 'person0_result2_new.log')
    handler_output.setFormatter(json_formatter)
    logger_topic, handler_topic = setup_logger('topic_logger', 'simu_log3.log')
    handler_topic.setFormatter(json_formatter)
    
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