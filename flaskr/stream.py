import subprocess
from flask import Blueprint, Response

bp = Blueprint('stream', __name__, url_prefix='/accueil/stream')

def generate_stream():
    # Start the subprocess to get the video stream
    process = subprocess.Popen(['rpicam-vid', '--width', '640', '--height', '480', '--framerate', '30'], 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        frame = process.stdout.readline()
        if not frame:
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@bp.route('/', methods=('GET', 'POST'))
def stream():
    return Response(generate_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/view', methods=['GET'])
def view():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Video Stream</title>
    </head>
    <body>
        <h1>Live Video Stream</h1>
        <img src="/accueil/stream/" alt="Video Stream">
    </body>
    </html>
    """