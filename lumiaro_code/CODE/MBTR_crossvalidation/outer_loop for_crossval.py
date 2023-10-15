import numpy as np
import os



w1 = [0,0.2,0.4,0.6,0.8,1.0,1.2,1.4]


for we1 in w1:
	os.system('python3 crossvalidation.py {}'.format(we1))
