from typing import List
from fastapi import FastAPI
from fastapi import HTTPException
import uvicorn
import pandas as pd
from os import path
from datetime import datetime
from pydantic import BaseModel
import rule_based_clustering as rbc
import run_zsc as zsc
from tqdm import tqdm

app = FastAPI()

class Item(BaseModel):
    Full_text: str
    Tweet_id: str 
    Geo_loc: str

class Item(BaseModel):
    Full_text: str
    Tweet_id: str 
    Geo_loc: str
    



@app.get("/")
def read_root():
    return {}


@app.post("/items/")
async def Get_Indent(item: Item,Rules : list):
 
    if not item.Full_text:
        raise HTTPException(status_code=404, detail="Invalid Full_text type") 
    if len(Rules) <= 1:
        raise HTTPException(status_code=404, detail="Invalid Rules format(Rules lenght = {})".format(len(item.Rules))) 
    if not item.Tweet_id:
        raise HTTPException(status_code=404, detail="Invalid Tweet_id (empty dict)") 

    
    #Plotted indent rule data
    row = pd.DataFrame(dict(item), index=[0])
    #row = row.groupby("Full_text","Geo_loc")["Rules","Tweet_id"].apply(list)

    plot_data = {"key": rbc.labels, "count": [0] * len(rbc.labels)}

    rule_based_labels, plot_data = rbc.process_tweet(row, plot_data)

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

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)

