from typing import List
from fastapi import FastAPI,HTTPException
import uvicorn
import pandas as pd
from os import path
from datetime import datetime
from pydantic import BaseModel
#import ml_modules.rule_based_clustering as rbc
from ml_modules.rule_based_clustering import RuleBasedClassifier
import ml_modules.run_zsc as zsc
from tqdm import tqdm
import traceback
from aiokafka import AIOKafkaConsumer
import asyncio

rbc = RuleBasedClassifier()
app = FastAPI()

class Item(BaseModel):
    Full_text: str
    Tweet_id: str 
    Geo_loc: str
#modify when output princibles ok
class responseItem (BaseModel):
    out_data: str
    out_data1: str 
    out_data2: str

@app.post("/items/")
async def Get_Indent(item: Item,Rules : list):
    try: 
        if not item.Full_text:
            raise HTTPException(status_code=404, detail="Invalid Full_text type") 
        if len(Rules) <= 1:
            raise HTTPException(status_code=404, detail="Invalid Rules format(Rules lenght = {})".format(len(item.Rules))) 
        if not item.Tweet_id:
            raise HTTPException(status_code=404, detail="Invalid Tweet_id (empty dict)") 

        
        #Plotted indent rule data
        row = pd.DataFrame(dict(item), index=[0])
        #row = row.groupby("Full_text","Geo_loc")["Rules","Tweet_id"].apply(list)

        rule_based_labels = rbc.classify(row["Full_text"].values[0])

        intent_results = ",".join(rule_based_labels) if rule_based_labels else ""
        
        #Check indent result
        if not intent_results:

            zsc_result = zsc.query(
                {
                    "inputs": row[1],
                    "parameters": {"candidate_labels": rbc.labels},
                })

            if zsc_result is not None:
                # sequence, labels, scores
                if "scores" in zsc_result:
                    
                    label_scores = zsc_result["scores"]
                    labels_filtered = [zsc_result["labels"][i] for i in range(len(label_scores)) if label_scores[i] > 0.3]
                    intent_results = ",".join([label for label in labels_filtered])                
                    plot_data = rbc.update_plot_data(plot_data, labels_filtered)
        
        templated_output = { "Tweet_id" : item.Tweet_id,
                                "Rules" : Rules,
                                "Full_text" : item.Full_text,
                                "data" : intent_results             
                            }
        
        return templated_output

    except Exception as e:
        print(e)

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
    #app.add_event_handler("startup", start_kafka_consumer)

    uvicorn.run(app, host="0.0.0.0", port=8000)

