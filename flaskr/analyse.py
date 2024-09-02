from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.auth import login_required
from . import mongo
import numpy as np
import cv2

bp = Blueprint('analyse', __name__, url_prefix='/accueil/analyse')


def analyse():
    #using opencv, analyse the image to find the color of the image
    img = cv2.imread('image/img.png')
    #convert the image to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)








# this is a post used to create a new analysis
@bp.route('', methods=['POST'])
@login_required
def newAnalyse():

    return redirect(url_for('analyse.pageHistorique'))

