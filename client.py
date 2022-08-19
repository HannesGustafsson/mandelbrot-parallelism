import argparse
import grequests
import matplotlib.pyplot as plt
import numpy as np
import time

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

    try:
        # Start execution timer
        start_time = time.time()

        # Get plotting points for X and Y axis
        re_axis = np.linspace(args.min_c_re, args.max_c_re, args.x)
        im_axis = np.linspace(args.min_c_im, args.max_c_im, args.y)
        
        # Divide work on the Y axis into chunks
        chunks = np.array_split(re_axis, args.divisions)

        urls = []
        for i, chunk in enumerate(chunks):
            # Loop through the endpoints
            server = args.server_list[i % len(args.server_list) - 1] 

            url = f'http://{server}/mandelbrot/{chunk[0]}/{args.min_c_im}/{chunk[-1]}/{args.max_c_im}/{len(chunk)}/{args.y}/{args.max_n}'
            urls.append(url)

        print('Sending following requests:')
        for url in urls:
            print(url)


        # Send work and stitch together full image
        reqs = (grequests.get(url) for url in urls)
        responses = grequests.map(reqs)

        # Make sure requests were successful
        for res in responses:
            if res == None or res.status_code != 200:
                raise Exception('Incomplete data received from server.')

        # Stitch responses together
        mb = []
        for res in responses:
            json = res.json()
            mb_chunk = json['data']
            for chunk in mb_chunk:
                mb.append(chunk)

        # Render image
        print('Rendering image...')
        plt.imshow(mb, extent=[args.min_c_im, args.max_c_im, args.min_c_re, args.max_c_re])
        #plt.show()
        plt.savefig('mandelbrot.png', dpi=1000)
        print('Image saved.')

        # Print execution time
        print("--- %s seconds ---" % (time.time() - start_time))

    except Exception as e:
        print(e)

    


