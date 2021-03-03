from flask import Blueprint, Flask, render_template, url_for, jsonify, session, request, redirect
from elice_library.models import User, Book, Rental
from datetime import date, datetime
from elice_library import db

# 블루프린트 객체 생성. 이름('main'), 모듈명, URL_prefix의 값을 전달해준다.
bp = Blueprint('user', __name__, url_prefix='/user')