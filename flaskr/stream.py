import subprocess, os
from flask import Blueprint, Response, render_template, url_for, Flask

bp = Blueprint('stream', __name__, url_prefix='/accueil/stream')
app = Flask(__name__)

def save_image():
    output_directory = os.path.join(app.static_folder, 'images')
    os.makedirs(output_directory, exist_ok=True)
    output_filename = os.path.join(output_directory, 'image.jpg')
    command = ['rpicam-still', '-o', output_filename, '-t', '1000']

    try:
        subprocess.run(command, check=True)
        print(f"Image saved as {output_filename}")
    except subprocess.CalledProcessError as e:
        print(f"Error taking picture: {e}")

@bp.route('', methods=['GET'])
def view():
    #display the image
    save_image()
    image_path = url_for('static', filename='images/image.jpg')
    return render_template('stream/view.html', image_path=image_path)
    