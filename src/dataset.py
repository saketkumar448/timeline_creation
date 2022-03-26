from datasets import load_dataset
from datetime import date, timedelta


class Dataset_toi():
    
    def __init__(self):
        self.dataset = None
        self.datewise_start_idx = None
        
    def load_dataset(self, dataset_dir):
        '''
        loads the dataset from given directory
        args: data_dir string, 
        '''
        try:
            self.dataset = load_dataset("times_of_india_news_headlines", data_dir=dataset_dir)
            
            # creating datewise start index
            self.datewise_indexing()
        except:
            return 0
        
        return 1
    
    
    def datewise_indexing(self):
        '''
        create datewise_start_idx dictionary {date: start index}
        the articles in the dataset  are sorted on date
        '''
        
        self.datewise_start_idx = {}
        for idx, date in enumerate(self.dataset['train']['publish_date']):
            if date not in self.datewise_start_idx.keys():
                self.datewise_start_idx[date] = idx
                
    
    def proc_timeline_points(self, timeline_points):
        '''
        args: timeline_points, list of timestamp objects
        returns: dict, pointwise start and end index of articles in the dataset
        '''
        pointwise_start_end_idx = {}
        
        # converting timeline_points into "yyyymmdd" format
        timeline_points = list(map(lambda x: x.strftime("%Y%m%d"), timeline_points))
        
        for idx in range(len(timeline_points) - 1):
            # checking if points exist in dataset or not 
            if timeline_points[idx] not in self.datewise_start_idx:
                continue
            if timeline_points[idx + 1] not in self.datewise_start_idx:
                continue
            
            pointwise_start_end_idx[timeline_points[idx]] = {'start_idx': self.datewise_start_idx[timeline_points[idx]],
                                                            'end_idx': self.datewise_start_idx[timeline_points[idx + 1]] - 1}
        return pointwise_start_end_idx
    
        
    def all_headlines_pointwise(self, timeline_points):
        '''
        args: timeline_points, list of timestamp objects
        returns: dict, all headlines pointwise, {date point: list of all headlines}
        '''
        
        # computing pontwise start and end index of articles
        pointwise_start_end_idx = self.proc_timeline_points(timeline_points)
        
        # grouping headlines point-wise
        pointwise_headlines = {}
        for point in pointwise_start_end_idx.keys():
            start_idx = pointwise_start_end_idx[point]['start_idx']
            end_idx = pointwise_start_end_idx[point]['end_idx']
            yr, mth, day = int(point[:4]), int(point[4:6]), int(point[6:])
            pointwise_headlines[date(yr, mth, day)] = self.dataset['train'][start_idx: end_idx + 1]['headline_text']
            
        return pointwise_headlines
            
        