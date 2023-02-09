from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer
import asyncio

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

async def start_kafka_consumer(app):
    consumer = AIOKafkaConsumer(
        "your_topic",
        bootstrap_servers="localhost:9092",
        group_id="your_group_id",
        auto_offset_reset="earliest"
    )

    # Start consuming
    await consumer.start()

    try:
        # Poll for new messages
        async for msg in consumer:
            print(f"Consumed message: {msg.value}")
    finally:
        # Close the consumer
        await consumer.stop()

app.add_event_handler("startup", start_kafka_consumer)
