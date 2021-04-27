#!/usr/bin/env python

import numpy as np
import math
np.set_printoptions(suppress=True)

def decode(cut, w1, w2, h1, h2, d1, d2, line, line_list):
	txt = input("please input outfile name: ")
	txt = "%s-%s.ply" % (txt, str(cut))
	out = open(txt, "w")
	x = (w2-w1) / cut
	y = (h2-h1) / cut
	z = (d2-d1) / cut
	tmp = np.zeros( (cut, cut, cut) )
	now = 0
	times = 0
	vertex = 0

	for i in range(cut):
		for j in range(cut):
			for k in range(cut):
				b = ord(line[now])
				if times < 3:
					if b & (8>>times):
						tmp[i][j][k] = 1
						vertex = vertex + 1
					else:
						tmp[i][j][k] = 0
					times = times+1
				elif times == 3:
					if b & (8>>times):
						tmp[i][j][k] = 1
						vertex = vertex + 1
					else:
						tmp[i][j][k] = 0
					times = 0
					now = now + 1
	print("step 1 vertex: %d" % vertex)
	#HEADER#############
	out.write("ply\nformat ascii 1.0\ncomment PCL generated\nelement vertex ")
	out.write(str(vertex))
	out.write("\nproperty float nx\nproperty float ny\nproperty float nz\nproperty float curvature\nproperty float x\nproperty float y\nproperty float z\nelement camera 1\nproperty float view_px\nproperty float view_py\nproperty float view_pz\nproperty float x_axisx\nproperty float x_axisy\nproperty float x_axisz\nproperty float y_axisx\nproperty float y_axisy\nproperty float y_axisz\nproperty float z_axisx\nproperty float z_axisy\nproperty float z_axisz\nproperty float focal\nproperty float scalex\nproperty float scaley\nproperty float centerx\nproperty float centery\nproperty int viewportx\nproperty int viewporty\nproperty float k1\nproperty float k2\nend_header\n")
	####################
	for i in range(cut):
		for j in range(cut):
			for k in range(cut):
				px = x*i + w1
				py = y*j + h1
				pz = z*k + d1
				if tmp[i][j][k] == 1:
					out.write( str(float(line[now:now+5])) )
					out.write( " " )
					now = now + 5
					out.write( str(float(line[now:now+5])) )
					out.write( " " )
					now = now + 5
					out.write( str(float(line[now:now+5])) )
					out.write( " " )
					now = now + 5
					out.write( str(float(line[now:now+5])) )
					out.write( " " )
					now = now + 5
					out.write( str(("%f" % px)) )
					out.write( " " )
					out.write( str(("%f" % py)) )
					out.write( " " )
					out.write( str(("%f" % pz)) )
					out.write( "\n" )
	for i in range(21):
		if i == 17:
			out.write("%s " % str(vertex))
		elif i == 20:
			out.write("%s" % line_list[i])
		else:
			out.write("%s " % line_list[i])
	print("fine.")
	out.close()





size = np.zeros(6)
file = open("mid", "r")
line = file.readline()

line_list = line.split()
cut = int(line_list[0])
size[0] = float(line_list[1])
size[1] = float(line_list[2])
size[2] = float(line_list[3])
size[3] = float(line_list[4])
size[4] = float(line_list[5])
size[5] = float(line_list[6])
line = file.readline()
line_list = line.split()
content = file.read()
file.close()

decode(cut, size[0], size[1], size[2], size[3], size[4], size[5], content, line_list)
input()
