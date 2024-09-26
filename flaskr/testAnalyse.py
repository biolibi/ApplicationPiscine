from time import sleep, time
from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for
)
from flaskr.auth import login_required
from . import mongo
import cv2
import subprocess
import os

bp = Blueprint('testAnalyse', __name__, url_prefix='/accueil/test')

def analyseTest():
    output_directory = os.path.expanduser('~/image/')
    os.makedirs(output_directory, exist_ok=True)

    for i in range(5):
        output_filename = os.path.join(output_directory, f'new_image_{i+1}.bmp')
        command = ['rpicam-still','-o', output_filename, '-t', '1000']

        try:
            subprocess.run(command, check=True)
            print(f"Image saved as {output_filename}")
        except subprocess.CalledProcessError as e:
            print(f"Error taking picture {i+1}: {e}")


    return '5 Images sauvegardées'

@bp.route('/analyse', methods=['POST'])
def analyse():
    result = analyseTest()
    return jsonify({'message': result})

@bp.route('', methods=['GET'])
@login_required
def pageTest():
    return render_template('analyse/testAnalyse.html')
