#simple apoximation to nbody problem
from random import randint
import time
import math
import json
import threading


#__CRITICAL__
def _CONST_N():
	return 100 #number of bodies

#__CRITICAL__
def _VAR_body_list(op, old_ver):
	if not hasattr(_VAR_body_list, "body_list"):
		_VAR_body_list.body_list=[]
	if not hasattr(_VAR_body_list, "ver_body_list"):
		_VAR_body_list.ver_body_list=0
	if not hasattr(_VAR_body_list, "lock_body_list"):
		_VAR_body_list.lock_body_list = threading.Lock()
	if op == None:
		if old_ver == _VAR_body_list.ver_body_list:
			return (None, old_ver)
		else:
			return (json.dumps(_VAR_body_list.body_list),_VAR_body_list.ver_body_list)
	else:
		try:
			_VAR_body_list.ver_body_list+=1
			return (eval(op),_VAR_body_list.ver_body_list)
		except:
			with lock_body_list:
				exec(op)
				_VAR_body_list.ver_body_list+=1
				return ("done",_VAR_body_list.ver_body_list)

#__CRITICAL__
cosa = threading.Lock()
def _VAR_body_new(op,old_ver):
	if not hasattr(_VAR_body_new, "body_new"):
		_VAR_body_new.body_new=[]
	if not hasattr(_VAR_body_new, "ver_body_new"):
		_VAR_body_new.ver_body_new=0
	if not hasattr(_VAR_body_new, "lock_body_new"):
		_VAR_body_new.lock_body_new = threading.Lock()
	if op == None:
		if old_ver == _VAR_body_new.ver_body_new:
			return (None, old_ver)
		else:
			return (json.dumps(_VAR_body_new.body_new),_VAR_body_new.ver_body_new)
	else:
		try:
			_VAR_body_new.ver_body_new+=1
			return (eval(op),_VAR_body_new.ver_body_new)
		except:
			with _VAR_body_new.lock_body_new:
				exec(op)
				_VAR_body_new.ver_body_new+=1
				return ("done",_VAR_body_new.ver_body_new)

#Nonblocking invocation synchronizer
def _SYNC_compute_body(op, old_ver = None):
	if not hasattr(_SYNC_compute_body, "termination_list"):
		_SYNC_compute_body.termination_list=0
	if op == None:
		return json.dumps(_SYNC_compute_body.termination_list)
	if op == "increase":
		_SYNC_compute_body.termination_list+=1
	if op == "decrease":
		_SYNC_compute_body.termination_list-=1


#__IDEMPOTENT__
def compute_body(single_body, iteration):
	# ---------------- AUTOMATED  CODE --------------------
	if not hasattr(compute_body, "body_list"):
		compute_body.body_list = []
	if not hasattr(compute_body, "ver_body_list"):
		compute_body.ver_body_list = 0
	aux = _VAR_body_list(None,compute_body.ver_body_list)[0]
	if aux != None:
		compute_body.body_list = json.loads(aux)

	if not hasattr(compute_body, "body_new"):
		compute_body.body_new = []
	if not hasattr(compute_body, "ver_body_new"):
		compute_body.ver_body_new = 0        
	aux_body_new = _VAR_body_new(None,compute_body.ver_body_new)[0]
	if aux_body_new != None:
		compute_body.body_new = json.loads(aux_body_new)

	single_body = json.loads(single_body)

	_SYNC_compute_body("increase")
	# ------------------------------------------------------
	fx=0.0
	fy=0.0
	for i in compute_body.body_list:
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
	_VAR_body_new("_VAR_body_new.body_new.append("+str(new_single_body)+")",compute_body.ver_body_new)
	compute_body.body_new.append(new_single_body)
	_SYNC_compute_body("decrease")

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
	#============================global vars automatic code=========================
	#body_list
	if not hasattr(main, "body_list"):
		main.body_list = []

	if not hasattr(main, "ver_body_list"):
		main.ver_body_list = 0
        
	aux_body_list = _VAR_body_list(None,main.ver_body_list)[0]
	if aux_body_list != None:
		main.body_list = json.loads(aux_body_list)
	#body_new
	if not hasattr(main, "body_new"):
		main.body_new = []

	if not hasattr(main, "ver_body_new"):
		main.ver_body_new = 0
        
	aux_body_new = _VAR_body_new(None,main.ver_body_new)[0]
	if aux_body_new != None:
		main.body_new = json.loads(aux_body_new)

	#============================global vars automatic code=========================
	MAX_ITERATIONS = 10
	X_MAX = 100
	Y_MAX = 100
	VX_MAX = 10
	VY_MAX = 10
	N = _CONST_N()
	print("Construyendo la lista...")
	for i in range(_CONST_N()):	
		m = 10 #mass
		x = randint(-X_MAX,X_MAX)
		y = randint(-Y_MAX,Y_MAX)
		vx = randint(-VX_MAX,VX_MAX)
		vy = randint(-VY_MAX,VY_MAX)
		_VAR_body_list("_VAR_body_list.body_list.append(("+str(m)+","+str(x)+","+str(y)+","+str(vx)+","+str(vy)+"))",main.ver_body_list)
		main.body_list.append((m,x,y,vx,vy))	

	for j in range(MAX_ITERATIONS):
		print("starting iteration", j)
		for i in main.body_list:
			#__NONBLOCKING__
			compute_body(json.dumps(i),j)#this will be f = invoke("compute_body(json.dumps(i),j)",[du_3,_du4,..,du_n],) or similar

		while _SYNC_compute_body(None) != '0':
			time.sleep(.1)

		##main.body_list = json.loads(_VAR_body_new(None,main.ver_body_new)[0])
		##main.ver_body_new = _VAR_body_new(None,main.ver_body_new)[1]
		main.body_list, main.ver_body_new = _VAR_body_new(None,main.ver_body_new)
		main.body_list = json.loads(main.body_list)		
		_VAR_body_new("_VAR_body_new.body_new = []",main.ver_body_new)
		main.body_new = []
		print("iteration ", j, " executed")

main()

