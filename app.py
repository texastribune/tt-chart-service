from subprocess import Popen, PIPE, STDOUT

from flask import Flask, Response, request, abort
from flask_heroku import Heroku

app = Flask(__name__)
heroku = Heroku(app)


@app.route('/render/', methods=['POST'])
def render():
    svg = request.form.get('svg')
    if not svg:
        abort(400)
    command = ['convert', 'svg:-', 'png:-']
    process = Popen(command, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    png_bin = process.communicate(input=svg)[0]
    return Response(png_bin, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
