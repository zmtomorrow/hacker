from abc import ABC, abstractmethod
from typing import Union, Any, List, Optional
from numpy import array
import requests
import json
import numpy as np
import html2text
import datetime

def get_max_id():
    url="https://hacker-news.firebaseio.com/v0/maxitem.json"
    results = requests.get(url)
    max_id = json.loads(results.text)
    return max_id

def get_story_by_id(story_id):
    item_url="https://hacker-news.firebaseio.com/v0/item/"+str(story_id)+".json"
    results=json.loads(requests.get(item_url).text)
    if results['type']!='story':
        return None
    if 'dead' in results or 'deleted' in results or 'url' not in results: 
        return None
    print(results)
    request_page = requests.get(results['url'])
    if request_page.status_code!=200:
        return None
    page=request_page.text
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_maker.ignore_images = True
    text = text_maker.handle(page)
    item={
        'OfficalItemId':story_id,
        'title':results['title'],
        'url':results['url'],
        'time':datetime.datetime.fromtimestamp(results['time']),
        'text': text
    }
    return item 



if __name__ == "__main__":
    import sqlalchemy as db
    engine = db.create_engine("sqlite:///hacker.sqlite")
    metadata = db.MetaData()
    Story = db.Table('Story', metadata,
                db.Column('OfficalItemId', db.Integer(),primary_key=True),
                db.Column('title', db.String(255), nullable=False),
                db.Column('text', db.Text(), nullable=False),
                db.Column('url', db.String(255), nullable=False),
                db.Column('time', db.DateTime(), default=True)
                )

    query = db.insert(Story)
    
    cur_id=get_max_id()
    for i in range(0,100):
        item=get_story_by_id(cur_id)
        if item!=None:
            with engine.connect() as connection:
                try:
                    Result = connection.execute(query,[item])
                except Exception as E:
                    print (E)
                connection.commit()
        else:
            pass
    

        cur_id-=1


