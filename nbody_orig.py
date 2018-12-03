#simple apoximation to nbody problem
from random import randint
import time
import math
import json

#global vars
body_list = []
body_new = []
CONST_N = 100

#__IDEMPOTENT__
def compute_body(single_body, iteration):
	global body_list
	global new_body
	
	fx=0.0
	fy=0.0
	for i in body_list:
		#print("i",i)
		delta_f = compute_contribution_force(single_body,i)
		fx = fx+delta_f[0]
		fy = fy+delta_f[1]
	ax = fx/float(single_body[0])
	ay = fy/float(single_body[0])
	vx = float(single_body[3])+ax
	vy = float(single_body[4])+ay
	x = float(single_body[1])+vx
	y = float(single_body[2])+vy
	
	
	new_single_body = (single_body[0],x,y,vx,vy)
	body_new.append(new_single_body)
	#print("Exit from computebody")

#__IDEMPOTENT__
def compute_contribution_force(bodyA, bodyB):
	m1 = bodyA[0]
	x1 = bodyA[1]
	y1 = bodyA[2]
	vx1 = bodyA[3]
	vy1 = bodyA[4]

	m2 = bodyB[0]
	x2 = bodyB[1]
	y2 = bodyB[2]
	vx2 = bodyB[3]
	vy2 = bodyB[4]

	dx = math.sqrt((x1-x2)**2)
	if dx != 0:
		fx = (m1*m2)/(dx**2)
	else:
		fx=0
	if x2<x1:
		fx = -fx

	dy = math.sqrt((y1-y2)**2)
	if dy!=0:
		fy = (m1*m2)/(dy**2)
	else:
		fy=0
	if y2<y1:
		fy = -fy

	return (fx,fy)

def main():
	global body_list
	global body_new
	MAX_ITERATIONS = 10
	X_MAX = 100
	Y_MAX = 100
	VX_MAX = 10
	VY_MAX = 10
	N = CONST_N
	print("Construyendo la lista...")
	for i in range(CONST_N):	
		m = 10 #mass
		x = randint(-X_MAX,X_MAX)
		y = randint(-Y_MAX,Y_MAX)
		vx = randint(-VX_MAX,VX_MAX)
		vy = randint(-VY_MAX,VY_MAX)

		body_list.append((m,x,y,vx,vy))		

	for j in range(MAX_ITERATIONS):
		print("starting iteration", j)
		for i in body_list:
			#__NONBLOCKING__
			f = compute_body(i,j)

		#aux = body_list
		body_list = body_new
		body_new = []
		print("iteration ", j, " executed")

main()