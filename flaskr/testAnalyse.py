from time import sleep, time
from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for
)
from flaskr.auth import login_required
from . import mongo, gpio
import cv2
import subprocess
import os


bp = Blueprint('testAnalyse', __name__, url_prefix='/accueil/test')

def circulationPompe():
    
    #PAS RAPPORT AVEC LE TEST
    gpio.setup(2, gpio.OUT)
    gpio.output(2, True)
    sleep(5)

    #valve alimentation flacon en eau
    gpio.setup(6, gpio.OUT)
    gpio.output(6, True)
    sleep(2)
    gpio.output(6, False)

    return 'Pompe testée'

def testChlorine():
    # Valve réservoir chlore
    gpio.setup(13, gpio.OUT)
    gpio.output(13, True)
    sleep(2)
    # Pompe doseuse chlore
    gpio.setup(17, gpio.OUT)
    gpio.output(17, True)
    sleep(5)
    gpio.output(17, False)
    gpio.output(13, False)

    # Moteur agitation
    gpio.setup(10, gpio.OUT)
    pwm = gpio.PWM(10, 1)
    pwm.start(0)
    pwm.ChangeDutyCycle(50)
    sleep(5)
    pwm.stop()
    gpio.output(10, False)

    return 'Chlore testé'

def testPh():
    #Valve réservoir ph
    gpio.setup(19, gpio.OUT)
    gpio.output(19, True)
    sleep(2)
    # Pompe doseuse ph
    gpio.setup(27, gpio.OUT)
    gpio.output(27, True)
    sleep(5)
    gpio.output(27, False)
    gpio.output(19, False)

    # Moteur agitation
    gpio.setup(9, gpio.OUT)
    pwm = gpio.PWM(9, 50)
    pwm.start(0)
    pwm.ChangeDutyCycle(50)
    sleep(5)
    pwm.stop()
    gpio.output(9, False)

    return 'Ph testé'

def testAlcalinite():
    # Valve réservoir alcalinité
    gpio.setup(22, gpio.OUT)
    gpio.output(22, True)
    sleep(2)
    # Pompe doseuse alcalinité
    gpio.setup(26, gpio.OUT)
    gpio.output(26, True)
    sleep(5)
    gpio.output(26, False)
    gpio.output(22, False)

    # Moteur agitation
    gpio.setup(11, gpio.OUT)
    pwm = gpio.PWM(11, 50)
    pwm.start(0)
    pwm.ChangeDutyCycle(50)
    sleep(5)
    pwm.stop()
    gpio.output(11, False)

    return 'Alcalinité testé'

def priseImage():
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

def drainage():
    # Valve drainage
    gpio.setup(18, gpio.OUT)
    gpio.output(18, True)
    sleep(1)
    gpio.output(6, True)
    sleep(30)
    gpio.output(6, False)
    sleep(5)
    gpio.output(18, False)





    return '5 Images sauvegardées'

@bp.route('/analyse', methods=['POST'])
def analyse():
    test = circulationPompe()
    test1 = testChlorine()
    test2 = testPh()
    test3 = testAlcalinite()
    result = priseImage()




    #result = analyseTest()
    return jsonify({'message': test+test1+test2+test3+result})

@bp.route('', methods=['GET'])
@login_required
def pageTest():
    return render_template('analyse/testAnalyse.html')
