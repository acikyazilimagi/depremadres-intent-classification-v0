from typing import List
from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import argparse
import uvicorn

# ML modules
from ml_modules.rule_based_clustering import RuleBasedClassifier
from ml_modules.bert_classifier import BertClassifier
# import ml_modules.run_zsc as zsc

# Define command line arguments to control which classifiers to run.
parser = argparse.ArgumentParser()
parser.add_argument('--run_rule_based_classifier',
                    action=argparse.BooleanOptionalAction, default=True)
parser.add_argument('--run_bert_classifier',
                    action=argparse.BooleanOptionalAction, default=True)
args = parser.parse_args()

# Initialize classifiers
rule_based_classifier = None
if args.run_rule_based_classifier:
    rule_based_classifier = RuleBasedClassifier()

bert_classifier = None
if args.run_bert_classifier:
    bert_classifier = BertClassifier()

# Initialize fastapi.
app = FastAPI()


# Data models.
class Request(BaseModel):
    text: str

class Response(BaseModel):
    intents: List[str]


@app.post("/get_intents/")
async def Get_Intent(item: Request) -> Response:
    if not item.text:
        raise HTTPException(status_code=400, detail="Bad request, no text")

    try:
        intents = []

        if args.run_rule_based_classifier:
            assert rule_based_classifier
            intents.extend(rule_based_classifier.classify(item.text))

        if args.run_bert_classifier:
            assert bert_classifier
            intents.extend(bert_classifier.classify(item.text))

        # Remove duplicates.
        intents = list(set(intents))
        return intents

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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


if __name__ == '__main__':
    # app.add_event_handler("startup", start_kafka_consumer)
    uvicorn.run(app, host="0.0.0.0", port=8000)
