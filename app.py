import os
import hashlib
import random
from unsilence import Unsilence
from flask import Flask, render_template, url_for, request, send_file
import threading
from yt_dlp import YoutubeDL

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        # take sha of file
        sha = hashlib.sha256()
        sha.update(file.read())

        print(sha.hexdigest())

        file.seek(0)

        file.save("videos/"+str(sha.hexdigest())+'.mp4')

        # copy file to finished directory

        # os.system("cp videos/"+str(sha.hexdigest())+".mp4 finished/")

        threading.Thread(target=render, args=(sha,)).start()

        return render_template('success.html', random_number=sha.hexdigest())
    else:
        return render_template('index.html')


def render(sha):
    # render video
    print("Rendering video")
    print(sha.hexdigest())
    u = Unsilence("videos/"+str(sha.hexdigest())+".mp4")
    u.detect_silence()
    u.render_media("finished/"+str(sha.hexdigest()) +
                   ".mp4", audible_speed=1, silent_speed=9)


@app.route('/check/<id>', methods=['GET'])
def check(id):
    # check if file exists named request.form['check'].mp4
    if os.path.isfile("finished/"+id+'.mp4'):
        return "1"
    else:
        return "0"


@app.route('/download/<id>', methods=['GET'])
def download(id):
    # download file named finished/id.mp4
    print("Downloading file")
    print(id)
    return send_file("finished/"+id+".mp4", as_attachment=True)


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


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
