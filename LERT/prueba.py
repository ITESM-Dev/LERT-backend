from flask import Flask
import sys
sys.path.insert(0,'./lert_driver_db2/db2')

from db2_Connection import Db2Connection

app = Flask(__name__)

connection = Db2Connection()



@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)