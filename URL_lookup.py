from flask import Flask,request,g,Response,jsonify
import mysql.connector
import json
import sys,os,urlparse

app = Flask(__name__)


