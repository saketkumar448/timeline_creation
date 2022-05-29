from typing import Optional
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from timeline import *
from datetime import datetime

# instance of Timeline() class
timeline_obj = Timeline()


class RequestBody(BaseModel):
    topic: str
    start_date: str    # '25/03/2015'
    end_date: str
    content_size: int
        

app = FastAPI()


@app.post("/timeline/")
async def root(request_body: RequestBody):
    
    # extracting and transforming arguments from request_body
    start_date = datetime.strptime(request_body.start_date, '%d/%m/%Y')
    end_date = datetime.strptime(request_body.end_date, '%d/%m/%Y')
    topic = request_body.topic
    content_size = request_body.content_size
    
    # setting variables of Timeline() object
    timeline_obj.set_topic(topic)
    timeline_obj.set_date_interval(start_date, end_date)
    timeline_obj.set_headlines_per_point(content_size)
    
    # creating timeline
    timeline_obj.headlines_grpd_by_pts()
    
    return timeline_obj.filtered_headlines_pointwise
    
    
if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8090, reload=True)


'''
url = 'http://0.0.0.0:8090/timeline/'
input_dict = {"topic": 'topic of choice',
             "start_date": '25/03/2015',
             "end_date": '30/03/2015',
             "content_size": 5,
             }
requests.post(url, json = input_dict).json()
'''

