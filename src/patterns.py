import numpy as np

patterns = [
    -1 * np.array([
        [0,0,0,1,0,0,1,0,0,0],
        [0,1,0,0,1,0,0,1,0,0],
        [0,0,1,0,0,1,0,0,1,0],
        [0,0,0,1,0,0,1,0,0,1],
        [0,1,0,0,1,0,0,1,0,0],
        [0,0,1,0,0,1,0,0,1,0],
        [0,0,0,1,0,0,1,0,0,1],
        [0,1,0,0,1,0,0,1,0,0],
        [0,0,1,0,0,1,0,0,1,0],
        [0,0,0,1,0,0,1,0,0,1]
    ]),
    -1 * np.array([
        [0,0,0,1,0,0,1,0,0,0],
        [0,0,1,0,0,1,0,0,1,0],
        [0,1,0,0,1,0,0,1,0,0],
        [1,0,0,1,0,0,1,0,0,0],
        [0,0,1,0,0,1,0,0,1,0],
        [0,1,0,0,1,0,0,1,0,0],
        [1,0,0,1,0,0,1,0,0,0],
        [0,0,1,0,0,1,0,0,1,0],
        [0,1,0,0,1,0,0,1,0,0],
        [1,0,0,1,0,0,1,0,0,0]
    ]),
     -1 * np.array([
        [0,0,0,1,0,0,0,1,0,0],
        [0,1,0,1,0,1,0,1,0,1],
        [0,1,0,1,0,1,0,1,0,1],
        [0,1,0,1,0,1,0,1,0,1],
        [0,1,0,1,0,1,0,1,0,1],
        [0,0,0,0,0,0,0,0,0,0],
        [0,1,0,1,0,1,0,1,0,1],
        [0,1,0,1,0,1,0,1,0,1],
        [0,1,0,1,0,1,0,1,0,1],
        [0,1,0,0,0,1,0,0,0,1]
    ]),
    -1 * np.array([
        [0,1,1,1,1,0,1,1,1,1],
        [0,0,0,0,0,0,0,0,0,0],
        [1,1,1,1,1,0,1,1,1,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,1,1,1,1,0,1,1,1,1],
        [0,0,0,0,0,0,0,0,0,0],
        [1,1,1,1,1,0,1,1,1,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,1,1,1,1,0,1,1,1,1],
        [0,0,0,0,0,0,0,0,0,0]
    ]),
]