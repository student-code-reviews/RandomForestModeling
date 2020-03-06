"""Utility file to seed ted talk data into tables"""

import datetime
from sqlalchemy import func
import pandas as pd
from model import Talk, Speaker, connect_to_db, db
from flask import Flask, render_template, request, flash, redirect, session
from server import app


talks=pd.read_csv("ted_main.csv")

def load_talks():
    """Load users from u.user into database."""

    print("Talks")
    
    i=0
    while i < talks.shape[0]:
        time=(datetime.datetime.fromtimestamp(int(talks.iloc[i][4])))
        published_month=int(time.strftime("%w"))
        published_day=int(time.strftime("%m"))
        speaker_name=talks.iloc[i,6]
        ID=db.session.query(Speaker.speaker_id)
        speaker_ID=ID.filter(Speaker.speaker_name==speaker_name).first()
        speakerID=int(speaker_ID[0])
        #speakerID=int(Speaker.query.filter(Speaker.speaker_name==speaker_name).first())
        #db.select([Speaker.columns.speaker_id]).where(Speaker.columSpeakns.speaker_name == speaker_name)
        published_year=int(time.strftime("%Y"))
        talk_name=talks.iloc[i,14]
        duration=int(talks.iloc[i,2])
        event=talks.iloc[i,3]
        languages=int(talks.iloc[i,5])
        num_views=int(talks.iloc[i,0])
        num_comments=int(talks.iloc[i,16])
        talk_id=i
        i+=1
        talk = Talk(talk_id=talk_id, speakerID=speakerID, published_month=published_month, talk_name=talk_name,
                    duration = duration, event=event, languages=languages, num_views=num_views,
                    num_comments=num_comments, published_day=published_day, published_year=published_year)

        # We need to add to the session or it won't ever be stored
        db.session.add(talk)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)

    # Once we're done, we should commit our work
    db.session.commit()

    

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

load_talks()