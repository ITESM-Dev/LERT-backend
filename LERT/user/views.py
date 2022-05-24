from flask import Blueprint, jsonify, request
from werkzeug import Response

user = Blueprint('user', __name__)

@user.route("/")
def hello():
    return "hello"

@user.route("/name")
def name():
    return "ricardo"

@user.route('/ajax_ddl')
def ajax_ddl():
    xml = 'foo'
    return Response(xml, mimetype='text/xml')