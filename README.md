# Speeder

Speeder is a simple POC webapp to cut silence from the video files. It's written in Python.

> This project is not actively maintained and it's not production ready. It's just a POC.
> if you want to contribute, please feel free to open an issue or a pull request.

## How to use

1. Upload a video file
2. Wait for the processing
3. Download the result

## How to Install and Run

```bash
git clone https://github.com/ismailbgr/speeder
cd speeder
pip install -r requirements.txt
gunicorn app:app
```