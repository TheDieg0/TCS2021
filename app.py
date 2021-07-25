from flask import Flask, render_template, jsonify, Response
from flask_cors import CORS
from main import init, metodo_codo,dbscan_model,transform

app= Flask(__name__)
CORS(app)
PORT= 5000
DEBUG=True

@app.route('/', methods=['GET'])
def index ():
    return '''<h1>TCS 2021 - RUTAS</h1>
                <ul>
                <li>datos</li>
                <li>metodo_codo</li>
                <li>transform</li>
                <li>dbscan_model</li>
                </ul>'''

@app.route('/datos', methods=['GET'])
def index2 ():
    return init()


@app.route('/metodo_codo', methods=['GET'])
def index3 ():
    return metodo_codo()


@app.route('/transform', methods=['GET'])
def index4 ():
    return transform()  

@app.route('/dbscan_model', methods=['GET'])
def index5 ():
    return dbscan_model() 

if __name__=="__main__":
    app.run(port=PORT, debug=DEBUG)
