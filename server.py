"""Ted Talks"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Talk, Speaker, Rating, Talk_Rating


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route("/talks")
def talk_list():
    """Show list of talks."""

    talks = Talk.query.all()
    
    return render_template("talk_list.html", talks=talks)

@app.route("/speakers")
def speaker_list():
    """Show list of speakers."""

    speakers = Speaker.query.all()
    return render_template("speaker_list.html", speakers=speakers)

@app.route("/find_speaker")
def find_speaker():
    """Find speaker."""

    return render_template("find_speaker.html")

@app.route("/find_speaker/<speaker>")
def speaker(speaker):
    """Find speaker."""
    speaker=speaker.split("-")
    speaker=" ".join(speaker)
    speakers=Speaker.query.filter(Speaker.speaker_name == speaker).first()
    talks=Talk.query.filter(Talk.speakerID==speakers.speaker_id).all()
    talk_list=[]
    for talk in talks:
        talk_list.append(talk.talk_name)

    if speakers:
        return jsonify({"status": "success",
                        "speaker_job": speakers.speaker_job,
                        "speaker_id": speakers.speaker_id,
                        "talks": talk_list})
    else:
        return jsonify({"status": "error",
                        "message": "No talk found with that ID"})


@app.route("/compare/<int:talk1_id>/<int:talk2_id>")
def compare_talks(talk1_id, talk2_id):
    """Compare talks."""
    talk1=Talk.query.get(int(talk1_id))
    talk2=Talk.query.get(int(talk2_id))
    
    rating_dict1_complete={}
    rating_dict1_complete["name"]=talk1.talk_name
    rating_list1=[]
    for r, t in db.session.query(Rating, Talk_Rating).filter(Talk_Rating.rating_id == Rating.rating_id).filter(Talk_Rating.ted_talk_id == talk1_id).all():
        rating_dict1={}
        rating_name=r.rating_name
        rating_count=t.rating_count
        rating_dict1['rating']=rating_name
        rating_dict1['count']=rating_count
        rating_list1.append(rating_dict1)
    rating_dict1_complete["values"]= rating_list1
    
    rating_dict2_complete={}
    rating_dict2_complete["name"]=talk2.talk_name
    rating_list2=[]
    for r, t in db.session.query(Rating, Talk_Rating).filter(Talk_Rating.rating_id == Rating.rating_id).filter(Talk_Rating.ted_talk_id == talk2_id).all():
        rating_dict2={}
        rating_name=r.rating_name
        rating_count=t.rating_count
        rating_dict2['rating']=rating_name
        rating_dict2['count']=rating_count
        rating_list2.append(rating_dict2)
    rating_dict2_complete["values"]= rating_list2

    rating_list=[]
    rating_list.append(rating_dict1_complete)
    rating_list.append(rating_dict2_complete)
    duration1=[]
    duration1.append(talk1.duration_min)
    duration1.append(talk1.duration_sec)
    duration2=[]
    duration2.append(talk2.duration_min)
    duration2.append(talk2.duration_sec)
    if talk1 and talk2:
        return jsonify({"status": "success",
                        "talk_name1": talk1.talk_name,
                        "num_comments1": (f"{talk1.num_comments:,d}"),
                        "num_views1": (f"{talk1.num_views:,d}"),
                        "duration1": duration1,
                        "talk_name2": talk2.talk_name,
                        "num_comments2": (f"{talk2.num_comments:,d}"),
                        "num_views2": (f"{talk2.num_views:,d}"),
                        "duration2": duration2,
                        "rating_list" : rating_list
        })
    else:
        return jsonify({"status": "error",
                        "message": "No talk found with that ID"})

    #return render_template("compare.html", talk1=talk1, talk2=talk2)

@app.route("/compare")
def compare():
    return render_template("compare.html")

@app.route("/talks/<int:talk_id>", methods=['GET'])
def talk_detail(talk_id):
    """Show information of talk."""

    rating_list=[]
    talk=Talk.query.get(talk_id)
    for r, t in db.session.query(Rating, Talk_Rating).filter(Talk_Rating.rating_id == Rating.rating_id).filter(Talk_Rating.ted_talk_id == talk_id).all():
        rating_dict={}
        rating_name=r.rating_name
        rating_count=t.rating_count
        rating_dict['name']=rating_name
        rating_dict['count']=rating_count
        rating_list.append(rating_dict)

    return render_template("talk.html", talk=talk, rating_list=rating_list)

@app.route("/speakers/<int:speaker_id>", methods=['GET'])
def speaker_detail(speaker_id):
    """Show information of ."""

    speaker=Speaker.query.get(speaker_id)

    return render_template("speaker.html", speaker=speaker)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
