import json
import logging
import os

from flask import Flask, Response, request, abort
from flask_heroku import Heroku
from wand.image import Image
from wand.exceptions import WandException

app = Flask(__name__)
heroku = Heroku(app)

logging.basicConfig()
logger = logging.getLogger(__name__)

app.config['token'] = os.environ['TT_CHART_SERVICE_TOKEN']


@app.route('/render/', methods=['POST'])
def render():
    # Require token for authorization
    if request.args.get('token') != app.config['token']:
        abort(401)

    # Get svg body from POST parameter
    svg = request.form.get('svg')
    if not svg:
        abort(400)

    # Render PNG to response
    try:
        with Image(blob=svg, format='svg') as image:
            with image.convert('png') as converted_image:
                png_bin = converted_image.make_blob()
    except WandException as e:
        logger.error(json.dumps({'svg': svg, 'exception': str(e)}))
        abort(500)

    return Response(png_bin, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
