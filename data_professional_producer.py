# Here I want to create a UI using streamlit for Data professionals
import json
import streamlit as st
from datetime import datetime
from confluent_kafka import Producer


kafka_conf = {    
'bootstrap.servers': 'Your_confluent_cloud_server', 
'security.protocol': 'SASL_SSL', 

'sasl.mechanism': 'PLAIN', 

'sasl.username': 'your_kafka_apikey_username', 
'sasl.password': 'your_kafka_apikey_password',
'group.id':'any_name_group',
'auto.offset.reset': 'earliest'

}

kafka_topic = "tech_data"
producer = Producer(kafka_conf)


st.title("Let's get to know more about your tech skills!")

tag_id = st.number_input("tag id", min_value = 1, max_value = 10000, step = 1)
tech_discipline = st.selectbox("tech discipline", ["Python Developer","Big Data", "Data Science", "Data Analyst","Generative AI"])
skills = st.multiselect("skills",["Python", "SQL", "Machine learning", "cloud platform", "API", "ETL", "Power BI", "Tableau"])
years_of_experience = st.selectbox("years of experince", ["0-2 years", "2-4 years","4-6 years","more than 6years"])
comment = st.text_area(" Tell us a little about your tech journey .......")

# Defining a function to activate the streamlit

def send_event():
    event= {
        "tagid" : tag_id,
        "tech discipline" : tech_discipline,
        "skills" : skills,
        "years of experience" : years_of_experience,
        "comment" : comment,
        "timestamp" : datetime.now().isoformat()
    }


    # To produce the data

    producer.produce(kafka_topic, key = str(tag_id), value = json.dumps(event))
    producer.flush()

    st.success(f"successfully sent the entry to kafka as: {event}")


if st.button("sent the data"):
    send_event()