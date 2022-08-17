from quart import Quart, jsonify
from hypercorn.config import Config
from hypercorn.asyncio import serve
import asyncio

import argparse
import numpy as np

import matplotlib.pyplot as plt

from mandelbrot import calc_mandelbrot


config = Config()
app = Quart(__name__)


@app.route('/mandelbrot/<min_c_re>/<min_c_im>/<max_c_re>/<max_c_im>/<x>/<y>/<inf_n>', methods=['GET'])
async def mandelbrot(min_c_re, min_c_im, max_c_re, max_c_im, x, y, inf_n):
    '''
    Arguments:
    min_c_re:   Minimum complex real number
    min_c_im:   Minimum complex imaginary number
    max_c_re:   Maximum complex real number
    max_c_im:   Maximum complex imaginary number
    x:          Grid X dimension
    y:          Grid Y dimension
    inf_n:      Number of maximum iterations
    '''
    
    try:
        # Quick solution to handle negative numbers in URL
        min_c_re = float(min_c_re)
        min_c_im = float(min_c_im)
        max_c_re = float(max_c_re)
        max_c_im = float(max_c_im)
        x = int(x)
        y = int(y)
        inf_n = int(inf_n)

    except ValueError as e:
        return 'Invalid argument values and/or types', 400
    
    # Get plotting points for X and Y axis
    re_axis = np.linspace(min_c_re, max_c_re, x)
    im_axis = np.linspace(min_c_im, max_c_im, y)

    # Calculate mandelbrot set
    response = calc_mandelbrot(re_axis, im_axis, inf_n)


    # Send response
    return jsonify({
        'c_real': {'min': min_c_re, 'max': max_c_re},
        'c_imag': {'min': min_c_im, 'max': max_c_im},
        'data': response.tolist(),
        }), 200


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mandelbrot')
    parser.add_argument('port', type=int, help='The port on which the server should listen.')
    args = parser.parse_args()

    config.bind = [f'localhost:{args.port}']

    asyncio.run(serve(app, config))