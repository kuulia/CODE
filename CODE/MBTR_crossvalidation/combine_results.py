
size = 1500
version = str(0)
kernel_used = 'rbf'

w1 = [0,0.2,0.4,0.6,0.8,1.0,1.2,1.4]

best = []

for wee in range(len(w1)):
	we1 = w1[wee]
	outfilename = 'mbtr_results_train_1500_' + kernel_used +  '_' + str(we1) +'.txt'
	outfile = open('{}'.format(outfilename), 'r')
	line = outfile.readline()
	splitted = line.split()
	while not(splitted[0] == "Best"):
		line = outfile.readline()
		splitted = line.split()
	best.append(splitted)
	

sigma1 = []
sigma2 = []
wei2 = []
wei1 = []
score = []


for one in  best:
	sigma1.append(one[3])
	sigma2.append(one[5])
	wei1.append(one[7])
	wei2.append(one[9])	
	score.append(float(one[11]))



im1 = score.index(max(score))

file = open("Gridsearch_" + str(size) + "_version_" + version + ".txt",'w+')

for im in range(len(sigma1)):
	print("sigma1 {} sigma2 {} w1 {} w2 {} score {}".format(sigma1[im], sigma2[im], wei1[im], wei2[im], score[im]))

	
	file.write("sigma1 {} sigma2 {} w1 {} w2 {} score {} \n".format(sigma1[im], sigma2[im], wei1[im], wei2[im], score[im]))

file.write("BEEESTT: sigma1 {} sigma2 {} w1 {} w2 {} score {}".format(sigma1[im1], sigma2[im1], wei1[im1], wei2[im1], score[im1]))

file.close()
