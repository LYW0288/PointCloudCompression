#!/usr/bin/env python

import numpy as np
import math
from plyfile import (PlyData, PlyElement, make2d,
                     PlyHeaderParseError, PlyElementParseError,
                     PlyProperty)
np.set_printoptions(suppress=True)

def lossy(cut, arr, w1, w2, h1, h2, d1, d2, camera):
	print("Step 1")
	x = (w2-w1) / cut
	y = (h2-h1) / cut
	z = (d2-d1) / cut
	col = int(arr.size/arr[0].size)
	file = open("mid", "w")
	booln = np.zeros((cut, cut, cut))
	tmp = np.zeros((cut, cut, cut, 4))
	#sav = 0
	file.write("%d %f %f %f %f %f %f\n" % (cut, w1, w2, h1, h2, d1, d2))
	for i in range(21):
		file.write("%s " % str(camera[0][i]))
	file.write("\n")
	print("Step 2")
	for a in range(col):
		i = math.floor((arr[a][4] - w1) / x)
		if i >= 8:
			i = i-1
		elif i <= 0:
			i = i + 1
		j = math.floor((arr[a][5] - h1) / y)
		if j >= 8:
			j = j-1
		elif j <= 0:
			j = j + 1
		k = math.floor((arr[a][6] - d1) / z)
		if k >= 8:
			k = k-1
		elif k <= 0:
			k = k + 1
		booln[i][j][k] = 1
		tmp[i][j][k][0] = arr[a][0]
		tmp[i][j][k][1] = arr[a][1]
		tmp[i][j][k][2] = arr[a][2]
		tmp[i][j][k][3] = arr[a][3]
	times = 0
	acc = 0
	print("Step 3")
	for i in range(cut):
		for j in range(cut):
			for k in range(cut):
				if times < 3:
					acc = acc*2 + booln[i][j][k]
					times = times+1
				elif times == 3:
					acc = acc*2 + booln[i][j][k]
					file.write(chr(int(acc)))
					times = 0
					acc = 0
	for i in range(cut):
		for j in range(cut):
			for k in range(cut):
				if booln[i][j][k] != 1: continue
				file.write("%.5s" % str(("%.5f" % tmp[i][j][k][0])))
				file.write("%.5s" % str(("%.5f" % tmp[i][j][k][1])))
				file.write("%.5s" % str(("%.5f" % tmp[i][j][k][2])))
				file.write("%.5s" % str(("%.5f" % tmp[i][j][k][3])))
	print("fine.")
	file.close()


filename = input("please input in-file name: ")

ply0 = PlyData.read(filename)
test = ply0.elements[0].data
camera = ply0.elements[1].data
size = np.zeros(6)
col = int(test.size/test[0].size)
for i in range(col):
	if test[i][4] < size[0] :
		size[0] = test[i][4]
	if test[i][4] > size[1]:
		size[1] = test[i][4]
	if test[i][5] < size[2] :
		size[2] = test[i][5]
	if test[i][5] > size[3]:
		size[3] = test[i][5]
	if test[i][6] < size[4] :
		size[4] = test[i][6]
	if test[i][6] > size[5]:
		size[5] = test[i][6]
lossy(128, test, size[0], size[1], size[2], size[3], size[4], size[5], camera)

input()
