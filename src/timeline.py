import pandas
from datetime import date, timedelta
import json
from dataset import *
from matcher import *
from streamlit_ import *


class Timeline():
    
    def __init__(self):
        
        self.date_interval = {'start_date': None,
                              'end_date': None}
        self.headlines_per_point = 5
        self.topic = None
        
        # loading dataset
        self.dataset = Dataset_toi()
        self.dataset.load_dataset(dataset_dir='./data')
        
        # query based headline filter
        self.filter = Top_matches()
        
        # loading streamlit 
        self.gui = GUI_streamlit()
        
        
    def set_date_interval(self, start_date, end_date):
        '''
        set interval date for timeline creation
        args: both arguments should be 'datetime.date' object
        '''
        self.date_interval['start_date'] = start_date   # (year, month, day)
        self.date_interval['end_date'] = end_date
        
    
    def set_headlines_per_point(self, headlines_per_point):
        '''
        set value of headlines_per_point
        args: integer
        '''
        self.headlines_per_point = headlines_per_point
        
    
    def set_topic(self, topic):
        '''
        set topic on which timeline should be created
        args: topic, string
        '''
        self.topic = topic
        
    
    def timeline_points(self):
        '''
        compute points in date interval i.e. all the possible dates in the given date interval
        returns: list of Timestamp objects,
        '''
        try:
            return list(pandas.date_range(self.date_interval['start_date'],
                               self.date_interval['end_date']+timedelta(days=1),
                               freq='d'))
        except TypeError as te:
            return 0
    
    
    def headlines_grpd_by_pts(self):
        '''
        returns: headlines grouped by points, {date: headlines}
        '''
        
        # extracting all headlines point-wise
        all_headlines_pointwise = self.dataset.all_headlines_pointwise(self.timeline_points())
        
        # filtering top headlines based on topic/query
        self.filtered_headlines_pointwise = {}
        for point in all_headlines_pointwise.keys():
            self.filtered_headlines_pointwise[point] = self.filter.top_k_text(query=self.topic,
                                  texts=all_headlines_pointwise[point],
                                  k=self.headlines_per_point)
        
        return self.filtered_headlines_pointwise
    
    
    def get_timeline_json(self):
        '''
        returns: combines title and events into single json, 
                 used to create timeline in sreamlit
        '''
        
        # grouping headlines daywise
        self.headlines_grpd_by_pts()
        
        self.gui.create_title(self.topic, self.date_interval)
        self.gui.create_events(self.filtered_headlines_pointwise)
        
        
        timeline_json = self.gui.get_timeline_json()
        
        return json.dumps(timeline_json)
    
    