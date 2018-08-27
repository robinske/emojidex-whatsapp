import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request
from requests_html import HTMLSession
from twilio.rest import Client


load_dotenv(find_dotenv())
app = Flask(__name__)



if __name__ == "__main__":
    app.run(debug=True)