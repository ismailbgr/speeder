from math import ceil
import os
import hashlib
import random
from unsilence import Unsilence
from flask import Flask, render_template, url_for, request, send_file
import threading
from yt_dlp import YoutubeDL

finishedDir = "finished/"
videosDir = "videos/"
PAGE_SUCCESS = "success.html"
PAGE_CONFIRM = "confirm.html"

currentlyworking = []

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        # take sha of file
        sha = hashlib.sha256()
        sha.update(file.read())
        print("uploaded file sha: " + sha.hexdigest())

        file.seek(0)

        if not os.path.exists(finishedDir + sha.hexdigest() + ".mp4"):
            print("File Exists")
            return render_template(PAGE_SUCCESS, random_number=sha.hexdigest())

        #if there is no directory called videos, create one
        if not os.path.exists("videos"):
            os.makedirs("videos")
        #if there is no directory called finished, create one
        if not os.path.exists("finished"):
            os.makedirs("finished")

        file.save(videosDir+str(sha.hexdigest())+'.mp4')

        # u = Unsilence(videosDir+str(sha.hexdigest())+".mp4")
        # u.detect_silence(short_interval_threshold=0.05,stretch_time=0.01,on_silence_detect_progress_update=printer)  


        # print(u.estimate_time(audible_speed=1, silent_speed=99))

        # return render_template('confirm.html', renderid=sha.hexdigest() , sec=ceil(abs(u.estimate_time(audible_speed=1, silent_speed=99)["delta"]["silent"][0])))
        return render_template('confirm.html', renderid=sha.hexdigest())
    else:
        return render_template('index.html')

def printer(current, total):
    print("Progress: " + str(current) + "/" + str(total))

def render(sha):
    print("Rendering video")
    print(sha)
    u = Unsilence(videosDir+str(sha)+".mp4")
    u.detect_silence(short_interval_threshold=0.05,stretch_time=0.01,on_silence_detect_progress_update=printer) 
    print("Detected silence") 
    u.render_media(finishedDir+str(sha) +
                   ".mp4", audible_speed=1, silent_speed=99,on_render_progress_update=printer,on_concat_progress_update=printer)
    print("Rendered video")


@app.route('/check/<id>', methods=['GET'])
def check(id):


    # check if file exists named request.form['check'].mp4
    if os.path.isfile(finishedDir+id+'.mp4'):
        return "1"
    else:
        if id not in currentlyworking:
            return "-1"
        else:
            return "0"


@app.route('/download/<id>', methods=['GET'])
def download(id):
    # download file named finished/id.mp4
    print("Downloading file")
    print(id)
    return send_file(finishedDir+id+".mp4", as_attachment=True)


@app.route('/ytdl/<id>', methods=['GET'])
def ytdl(id):
    # download url using yt-dlp

    #generate random number
    sha = hashlib.sha256()
    sha.update(str(random.randint(0, 1000000)).encode('utf-8'))
    

    ydl_opts = {'format': '22',
    'outtmpl': 'videos/'+sha.hexdigest()+'.%(ext)s',
     'external_downloader': 'aria2c',
        'external-downloader-args': '--header="Referer: https://www.youtube.com/" -x 16 -s 16 -k 1M'
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(["https://www.youtube.com/watch?v="+str(id)])


    threading.Thread(target=render, args=(sha,)).start()


    return render_template('success.html', random_number=sha.hexdigest())

@app.route('/render_video/<vid_id>', methods=['GET'])
def render_video(vid_id):

        #add to currently working list
        currentlyworking.append(vid_id)
    
        #check if vid_id.mp4 exists in videos directory
        if not os.path.isfile(videosDir+vid_id+".mp4"):
            return "Hatalı Video ID: " + vid_id
        
        threading.Thread(target=render, args=(vid_id,)).start()

        # print(u.estimate_time(audible_speed=1, silent_speed=99))

        return render_template('success.html', random_number=vid_id)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
