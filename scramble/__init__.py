from flask import Flask
from flask import jsonify, render_template

from scramble import solver


W = solver.read_corpus()

P = { 0 : solver.Constants.TL,
      6 : solver.Constants.TL,
     10 : solver.Constants.TL,
     14 : solver.Constants.TW }


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/solve/<puzzle>')
def solve(puzzle):
    return jsonify(solver.solve(puzzle.lower(), P, W, fmt='dict'))
