#simple apoximation to nbody problem
from random import randint
import time
import math
import json

#the programmer wrote body_list = [] (as a global var)
#__CRITICAL__
def _VAR_body_list(op, old_hash):
	if not hasattr(_VAR_body_list, "body_list"):
		_VAR_body_list.body_list=[]
	if not hasattr(_VAR_body_list, "hash_body_list"):
		_VAR_body_list.hash_body_list=hash(str(_VAR_body_list.body_list))
	if op == None:
		if old_hash == _VAR_body_list.hash_body_list:
			#print("GET BODY_LIST: No hay cambios",old_hash,_VAR_body_list.hash_body_list)
			return None
		else:
			#return eval("_VAR_body_list.body_list")
			return json.dumps(_VAR_body_list.body_list)
	else:
		try:
			eval(op)
			_VAR_body_list.hash_body_list=hash(str(_VAR_body_list.body_list))
			return _VAR_body_list.hash_body_list
		except:
			#print(op, "No se puede evaluar")
			exec(op)
			_VAR_body_list.hash_body_list=hash(str(_VAR_body_list.body_list))
			return _VAR_body_list.hash_body_list

#the programmer wrote body_new = [] (as a global var)
#__CRITICAL__
def _VAR_body_new(op):
	#Tenemos pendiente dejar esta vble global como body_list (hacer lo del hash)
	if not hasattr(_VAR_body_new, "body_new"):
		_VAR_body_new.body_new=[]
	if op == None:	
		return eval("_VAR_body_new.body_new")
	else:
		try:
			return eval(op)
		except:
			exec(op)

#Computebody access to global var body_list.
#global vars are cached and before read its changes are checked 
#__IDEMPOTENT__
def compute_body(single_body, iteration):
	#print("Enter in computebody")
	# ---------------- AUTOMATED  CODE --------------------
	# el acceso a variables globales se cachea y solo se lee 
	# como mucho una vez al comienzo de la funcion ( si ha cambiado)
	if not hasattr(compute_body, "body_list"):
		compute_body.body_list = []#_VAR_body_list(None,hash(str(None)))
        
	aux = _VAR_body_list(None,hash(str(compute_body.body_list)))
	#print("AUX: ", aux)
	if aux != None:
		compute_body.body_list = json.loads(aux)
        #print("LA lista es distinta y hemos hecho load")
    #-------------------------------------------------
	single_body = json.loads(single_body)
	#print("LLega: ", single_body)
    # ------------------------------------------------------
	#calculation
	#print("CB_BODY_LIST: ",compute_body.body_list)
	fx=0.0
	fy=0.0
	for i in compute_body.body_list:
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
	#print("@Computation body done", x)
	#insert_body(new_single_body)
	_VAR_body_new("_VAR_body_new.body_new.append("+str(new_single_body)+")")
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

'''def insert_body(single_body):
	if not hasattr(insert_body, "body_new"):
		insert_body.body_new=[]
	if not hasattr(insert_body, "done"):
		insert_body.done = False
	if not hasattr(insert_body,"const_N"):
		insert_body.const_N = _CONST_N()
	if single_body == None:
		return 
	insert_body.body_new.append(single_body)
	if len(insert_body.body_new) == insert_body.const_N:
		insert_body.done = True'''


#The programmer wrote const_N = 1000	
def _CONST_N():
	return 1000 #number of bodies

def main():
#tenemos que manejar las variables globales y constantes globales en main como hacemos en el resto de funciones
# de momento el main esta en modo chapu



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
		_VAR_body_list("_VAR_body_list.body_list.append(("+str(m)+","+str(x)+","+str(y)+","+str(vx)+","+str(vy)+"))",hash("0"))

	for j in range(MAX_ITERATIONS):
		print("starting iteration", j)
		for i in json.loads(_VAR_body_list(None,hash(str("0")))):
			#__NONBLOCKING__
			f = compute_body(json.dumps(i),j)
			
			#body_new.append((i[0],x,y,vx,vy))
		#pointer commutation
		#while(insert_body.done == False):
		while _VAR_body_new("len(_VAR_body_new.body_new)") < _CONST_N():
			time.sleep(.1)
		aux = _VAR_body_list(None,hash(0))
		'''if (aux ==None ) :
			print "aux=none"
		else:
			print "aux= algo"'''

		body = _VAR_body_new(None)
		_VAR_body_new("_VAR_body_new.body_new = []")
		print("iteration ", j, " executed")

main()

