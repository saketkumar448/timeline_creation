
class GUI_streamlit():
    
    
    def __init__(self):
        self.title = None
        self.events = None
        self.timeline_json = None
        
        
    def create_title(self, topic, date_interval):
        '''
        args: topic, str, title of the timeline
              date_interval, dict, time interval of the timeline
        '''
        timeline_start_dt = date_interval['start_date'].strftime('%B %d, %Y')
        timeline_end_dt = date_interval['end_date'].strftime('%B %d, %Y')
        timeline_range_display = timeline_start_dt + ' - ' + timeline_end_dt
        self.title = {
            "text": {
                "headline": topic.title(),
                "text": timeline_range_display
            }
        }
    
    
    def create_events(self, daywise_events):
        '''
        args: daywise_events, dict, {date: list of headlines}
        creating events for streamlit timeline
        '''
        
        self.events = []
        for point in daywise_events.keys():
            
            # creating start_date of an event
            day = point.strftime('%d')
            month = point.strftime('%m')
            year = point.strftime('%Y')
            
            # creating text of an event
            event_text = ''
            for headline in daywise_events[point]:
                event_text = event_text + '<p>' + headline[0] + '</p>'
            
            # creating an event
            event = {
                "start_date": {
                    "month": month,
                    "day": day,
                    "year": year
                },
                "text": {
                    "text": event_text
                }
            }
            
            # appending an event in the event list
            self.events.append(event)
            
        return self.events
    
    
    def get_timeline_json(self):
        '''
        returns: combines title and events into single json
        '''
        
        self.timeline_json = {
            "title": self.title,
            "events": self.events
        }
        
        return self.timeline_json
    
    