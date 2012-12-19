from subprocess import Popen, PIPE, STDOUT
import os

from flask import Flask, Response, request, abort
from flask_heroku import Heroku

app = Flask(__name__)
heroku = Heroku(app)

TOKEN = os.environ['TT_CHART_SERVICE_TOKEN']


@app.route('/render/', methods=['POST'])
def render():
    # Require token for authorization
    if request.args.get('token') != TOKEN:
        abort(401)

    # Get svg body from POST parameter
    svg = request.form.get('svg')
    if not svg:
        abort(400)

    # Render PNG to response
    command = ['convert', 'svg:-', 'png:-']
    process = Popen(command, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    result = process.communicate(input=svg)
    if process.returncode != 0:
        abort(500)

    return Response(result[0], mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
