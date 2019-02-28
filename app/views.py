# -*- coding: utf-8 -*-
import json
import os
from flask import Blueprint, jsonify, render_template, session, redirect, url_for, current_app, request

# Define the blueprint:
landing_page = Blueprint('landing_page', __name__)

@landing_page.route('/', methods=['GET'])
def home_page():
    return render_template('index.html')
