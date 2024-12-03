from time import sleep, time
from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for
)
from flaskr.auth import login_required
from . import mongo, gpio
from datetime import datetime
import cv2
import subprocess
import os
import numpy as np


bp = Blueprint('testAnalyse', __name__, url_prefix='/accueil/test')

def circulationPompe():
    
    #valve alimentation flacon en eau
    gpio.setup(6, gpio.OUT)
    gpio.output(6, False)
    gpio.setup(13, gpio.OUT)
    gpio.output(13, False)
    sleep(6.5)
    gpio.output(6, True)
    gpio.output(13, True)

    return 'Pompe testée'

def rincage():
    
    #Pompe circulationEau
    gpio.setup(6, gpio.OUT)
    gpio.output(6, False)
    gpio.setup(13, gpio.OUT)
    gpio.output(13, False)
    sleep(6)
    #Pompe evacuationEau
    gpio.setup(23, gpio.OUT)
    gpio.output(23, False)
    gpio.setup(24, gpio.OUT)
    gpio.output(24, False)
    sleep(10)
    gpio.output(6, True)
    gpio.output(13, True)
    sleep(24)
    gpio.setup(23, gpio.OUT)
    gpio.output(23, True)
    gpio.setup(24, gpio.OUT)
    gpio.output(24, True)

def evacuationEau():
    gpio.setup(23, gpio.OUT)
    gpio.output(23, False)
    gpio.setup(24, gpio.OUT)
    gpio.output(24, False)
    sleep(18)
    gpio.output(23, True)
    gpio.output(24, True)

def configurationInitial():
    # Valve réservoir chlore
    gpio.setup(19, gpio.OUT)
    gpio.output(19, False)
    # Pompe doseuse chlore
    gpio.setup(26, gpio.OUT)
    gpio.output(26, False)
    sleep(2)
    gpio.output(19, True)
    gpio.output(26, True)

    # Valve réservoir ph
    gpio.setup(16, gpio.OUT)
    gpio.output(16, False)
    # Pompe doseuse ph
    gpio.setup(20, gpio.OUT)
    gpio.output(20, False)
    sleep(2)
    gpio.output(16, True)
    gpio.output(20, True)
    rincage()
    

def testChlorine():
    # Valve réservoir chlore
    gpio.setup(19, gpio.OUT)
    gpio.output(19, False)
    # Pompe doseuse chlore
    gpio.setup(26, gpio.OUT)
    gpio.output(26, False)
    sleep(0.20)
    gpio.output(19, True)
    gpio.output(26, True)

    sleep(5)

    # Moteur agitation
    gpio.setup(10, gpio.OUT)
    pwm = gpio.PWM(10, 800)
    pwm.start(0)
    pwm.ChangeDutyCycle(50)
    for i in range(10):
        #quand gpio 5 est 1 =, nous sommes en reverse
        gpio.setup(9, gpio.OUT)
        gpio.output(9, False)
        sleep(.25)
        gpio.output(9, True)
        sleep(.25)
       
    pwm.stop()
    gpio.output(10, False)

    
    return 'Chlore testé'

def testPh():
    # Valve réservoir ph
    gpio.setup(16, gpio.OUT)
    gpio.output(16, False)

    # Pompe doseuse ph
    gpio.setup(20, gpio.OUT)
    gpio.output(20, False)
    sleep(0.20)
    gpio.output(16, True)
    gpio.output(20, True)

    sleep(5)

    # Moteur agitation
    gpio.setup(25, gpio.OUT)
    pwm = gpio.PWM(25, 800)
    pwm.start(0)
    pwm.ChangeDutyCycle(50)
    for i in range(10):
        #quand gpio 5 est 1 =, nous sommes en reverse
        gpio.setup(8, gpio.OUT)
        gpio.output(8, True)
        sleep(.25)
        gpio.output(8, False)
       
    pwm.stop()
    gpio.output(25, False)

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

    sleep(5)

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
    #attendre un peu que le mélange se stabilise (uniforme)
    sleep(5)
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

def analyseImage():
    output_directory = os.path.expanduser('~/image/')
    os.makedirs(output_directory, exist_ok=True)

    pH = 0
    chlore = 0
    alcalinite = 0
    temperature = 0

    #Analyse Chlore
    for i in range(5):
        input_filename = os.path.join(output_directory, f'new_image_{i+1}.bmp')
        image = cv2.imread(input_filename)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        lower = np.array([62, 44, 0])
        upper = np.array([80, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if len(contours) > 0:
            largest_contour = max(contours, key=cv2.contourArea)

            #cette partie sert a délimiter un cercle plus petit (la partie qui nous intéresse pour les tests)
            x, y, w, h = cv2.boundingRect(largest_contour)
            center_x, center_y = x + w // 2, y + h // 2
            #ajustement du centre du cercle
            new_center_x = int(center_x + 0.10 * w)
            new_center_y = int(center_y - 0.10 * h)
            #ratio du cercle
            radius = int(0.2 * min(w, h))  
            circular_mask = np.zeros_like(mask)
            cv2.circle(circular_mask, (new_center_x, new_center_y), radius, 255, thickness=cv2.FILLED)
            
            # calcul couleur moyenne
            mean_color = cv2.mean(image, mask=circular_mask)
            
            # Image pour validé, retirer lorsque les tests seront fonctionne
            output_image = cv2.bitwise_and(image, image, mask=circular_mask)
            output_filename = os.path.join(output_directory, f'new_image_{i+1}_output_chlore.bmp')
            cv2.imwrite(output_filename, output_image)

        else:
            print(f"Pas de contenant trouver pour l'image {i+1}")

    #Analyse Ph
    for i in range(5):
        input_filename = os.path.join(output_directory, f'new_image_{i+1}.bmp')
        image = cv2.imread(input_filename)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        lower = np.array([102, 63, 0])
        upper = np.array([128, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if len(contours) > 0:
            largest_contour = max(contours, key=cv2.contourArea)

            #cette partie sert a délimiter un cercle plus petit (la partie qui nous intéresse pour les tests)
            x, y, w, h = cv2.boundingRect(largest_contour)
            center_x, center_y = x + w // 2, y + h // 2
            #ajustement du centre du cercle
            new_center_x = int(center_x - 0.28 * w)
            new_center_y = int(center_y - 0.10 * h)
            #ratio du cercle
            radius = int(0.2 * min(w, h))  
            circular_mask = np.zeros_like(mask)
            cv2.circle(circular_mask, (new_center_x, new_center_y), radius, 255, thickness=cv2.FILLED)
            
            # calcul couleur moyenne
            mean_color = cv2.mean(image, mask=circular_mask)
            
            # Image pour validé, retirer lorsque les tests seront fonctionne
            output_image = cv2.bitwise_and(image, image, mask=circular_mask)
            output_filename = os.path.join(output_directory, f'new_image_{i+1}_output_ph.bmp')
            cv2.imwrite(output_filename, output_image)
        else:
            print(f"Pas de contenant trouver pour l'image {i+1}")

    mongo.db.analyses.insert_one({'ph': pH, 'chlore': chlore, 'alcalinite': alcalinite, 'date': datetime.now(), 'temperature' : temperature})
    
    return mongo.db.analyses.find_one(sort=[('_id', -1)])['_id']
    
@bp.route('/analyse', methods=['POST'])
@login_required
def analyse():
    
#appeler lors de la premiere configuration seulement faire une fonction pour s'assurer que c'est la premiere fois (produit dans tuyaux)
    #configurationInitial()
    
    #test = circulationPompe()
    #test1 = testChlorine()
    #test2 = testPh()
    #result = priseImage()

    #test4 = rincage()
    #test3 = testAlcalinite()
    
    result1 = analyseImage()

    #evacuer l'eau (sans les autres systemes)
    #test3 = evacuationEau()

    return jsonify({'message': test+test1+test2+test3+test4+result})

@bp.route('', methods=['GET'])
@login_required
def pageTest():
    return render_template('analyse/testAnalyse.html')
