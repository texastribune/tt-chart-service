from subprocess import Popen, PIPE, STDOUT

from flask import Flask, Response
from flask_heroku import Heroku

app = Flask(__name__)
heroku = Heroku(app)


@app.route('/render/')
def render():
    svg_bin = """<svg width="200px" height="100px">
<circle cx="100" cy="50" r="40" stroke="black" stroke-width="2" fill="red" />
</svg>"""
    command = ['convert', 'svg:-', 'png:-']
    process = Popen(command, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    png_bin = process.communicate(input=svg_bin)[0]
    return Response(png_bin, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
