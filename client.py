import argparse
import grequests
import matplotlib.pyplot as plt
import numpy as np
import time


def divide_work(min_c_re, min_c_im, max_c_re, max_c_im, x, y, div, servers) -> list[str]:
    '''
    Divides the work into chunks and returns them as a list of endpoints.
    '''
    # Split into chunks on X axis
    re_axis = np.linspace(min_c_re, max_c_re, x)
    chunks = np.array_split(re_axis, div)

    urls = []
    for i, chunk in enumerate(chunks):
        # Loop through the endpoints starting at 0
        server = servers[i % len(servers) - 1] 

        url = f'http://{server}/mandelbrot/{chunk[0]}/{min_c_im}/{chunk[-1]}/{max_c_im}/{len(chunk)}/{y}/{max_n}'
        urls.append(url)

    return urls


def render_image(urls: list[str]) -> list:
    '''
    Asynchronously sends requests to a list of endpoints and stitches together the resulting image data.
    '''
    # Send requests
    reqs = (grequests.get(url) for url in urls)
    responses = grequests.map(reqs)

    # Make sure requests were successful
    for i, res in enumerate(responses):
        print(f'{urls[i]}: {res}')
        if res == None or res.status_code != 200:
            raise Exception('Incomplete data received from server.')

    # Stitch responses together
    result = []
    for res in responses:
        json = res.json()
        mb_chunk = json['data']
        for chunk in mb_chunk:
            result.append(chunk)

    return result



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mandelbrot Client')
    parser.add_argument('min_c_re', type=float)
    parser.add_argument('min_c_im', type=float)
    parser.add_argument('max_c_re', type=float)
    parser.add_argument('max_c_im', type=float)
    parser.add_argument('max_n', type=int)
    parser.add_argument('x', type=int)
    parser.add_argument('y', type=int)
    parser.add_argument('divisions', type=int, help='Number of divisions.')
    parser.add_argument('server_list', type=str, help='List of server addresses to send divisions.', nargs='+')
    args = parser.parse_args()

    min_c_re =  args.min_c_re
    min_c_im =  args.min_c_im
    max_c_re =  args.max_c_re
    max_c_im =  args.max_c_im
    max_n =     args.max_n
    x =         args.x
    y =         args.y
    div =       args.divisions
    servers =   args.server_list

    try:
        # Start execution timer
        print('Starting...')
        start_time = time.time()

        # Divide work
        urls = divide_work(min_c_re, min_c_im, max_c_re, max_c_im, x, y, div, servers)

        # Get image data
        mandelbrot = render_image(urls)

        print('Rendering image...')
        plt.imshow(mandelbrot, extent=[min_c_im, max_c_im, min_c_re, max_c_re])
        plt.savefig('mandelbrot.png', dpi=1000)
        print('Image saved.')

        # Print execution time
        print('--- %s seconds ---' % (time.time() - start_time))

    except Exception as e:
        print(e)

    


