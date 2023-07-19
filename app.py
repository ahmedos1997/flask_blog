import functools
import sqlite3
from flask import Flask, request, redirect, session , url_for, render_template, flash, g 
from werkzeug.security import generate_password_hash , check_password_hash
from blog import bp as blogbp
from auth import bp as authbp

app = Flask(__name__)

app.config.from_mapping(SECRET_KEY = 'lsnlsnldsnlskdnklsdnfklsnfkldsn')
app.register_blueprint(blogbp)
app.register_blueprint(authbp)

app.add_url_rule('/', endpoint='blog.index')





        



