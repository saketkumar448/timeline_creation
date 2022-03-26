# Streamlit Timeline Component Example
import streamlit as st
from streamlit_timeline import timeline
import datetime

import json
import re


class LazyDecoder(json.JSONDecoder):
    def decode(self, s, **kwargs):
        regex_replacements = [
            (re.compile(r'([^\\])\\([^\\])'), r'\1\\\\\2'),
            (re.compile(r',(\s*])'), r'\1'),
        ]
        for regex, replacement in regex_replacements:
            s = regex.sub(replacement, s)
        return super().decode(s, **kwargs)


from timeline import *


@st.cache(allow_output_mutation=True)
def load_timeline_object():
    '''
    this fucntion avoids loading of timeline object again and again
    '''
    timeline_obj = Timeline()
    return timeline_obj


def create_timeline(topic, start_date, end_date, content_size):
    '''
    whenever create timeline button is clicked
    args: topic, str, timeline entity
          start_date,  datetime object, start date of timeline
          end_date, datetime object, end date of timeline
          content_size, integer, number of headlines per block
    '''
    timeline_obj = load_timeline_object()
    
    timeline_obj.set_topic(topic)
    timeline_obj.set_date_interval(start_date, end_date)
    timeline_obj.set_headlines_per_point(content_size)
    return eval(timeline_obj.get_timeline_json())


def gui_sidebar():
    '''
    creating sidebar of gui
    '''
    # creating heading "Timeline"
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Timeline</h2>
    </div>
    """
    st.sidebar.markdown(html_temp, unsafe_allow_html=True)

    # taking topic for the Timeline
    topic = st.sidebar.text_input(label = 'Topic', value="Enter Text")

    # Timeline start date
    start_date = st.sidebar.date_input("Start date", datetime.date(2019, 7, 6))

    # Timeline end date
    end_date = st.sidebar.date_input("End date", datetime.date(2019, 7, 25))

    # Numbers of headlines block
    content_size = st.sidebar.number_input("No. of headlines", value=3) 

    # "Create Timeline" button
    if st.sidebar.button("Create Timeline"):

        # create timeline data
        timeline_data = create_timeline(topic, start_date, end_date, content_size)

        # render timeline
        timeline(timeline_data, height=750)
        



def main():


    # use full page width
    st.set_page_config(page_title="Timeline Example", layout="centered")

    # creating sidebar
    gui_sidebar()


if __name__ == '__main__':
    main()