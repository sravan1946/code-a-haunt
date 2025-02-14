import re
from flask import Flask
from flask import render_template, send_from_directory, request, redirect, url_for, send_file
import asyncio
import shutil
import os
import requests


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, port=8000)

