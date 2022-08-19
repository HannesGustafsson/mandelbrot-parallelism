import numpy as np
import numba


@numba.jit # Using JIT speeds up calculation process by more than 50x
def calc_mandelbrot(real: np.ndarray, imag: np.ndarray, max_n: int) -> np.ndarray:
    '''
    Calculates the mandelbrot set based on given real and imaginal axis.
    Determines a single value of magnitude for each point in the set.
    '''
    
    def calc_point(a: float, b: float) -> int:
        '''Calculate the magnitude of a single point in a mandelbrot set.'''

        c = complex(a, b)
        z = 0

        for n in range(max_n):
            z = (z * z) + c

            if np.abs(z) > 2:
                return int(n % 256)
            
        return (256)

    # Create empty NDArray
    result = np.zeros((len(real), len(imag)), dtype=numba.int64)

    # Calculate value of each point in the given set
    for re_index, re in enumerate(real):
        for im_index, im in enumerate(imag):
            result[re_index][im_index] = calc_point(re, im)

    return result