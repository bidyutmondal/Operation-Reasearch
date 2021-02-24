from sympy import var
import sympy as sym

def read ():
	n = int(input('\nEnter the number of variables: '))
	m = int(input('Enter the number of equations: '))
	print ('\nEnter the coefficients of variables inequation sign and the constant value (separated by space):\n\n')
	arr = []
	sign = []
	for i in range (m):
		print ('Constraint number {}:'.format(i+1))
		raw = input()
		raw_arr = raw.split()
		sign.append(raw_arr.pop(n))
		arr.append(raw_arr)
	print ('\n\nEnter the coefficient of variables in objective function with constant value (separated by space):')
	obj = input()
	obj_arr = obj.split()
	mi = int(input('\n\n1. Maximize\n2. Minimize\nEnter the choice for objective function: '))
	if (mi == 2):
		minimize = True
	else:
		minimize = False
	return (n, m, arr, sign, obj_arr, minimize)

def initialize():
	ex = sign.count('>=')
	N = n + ex + 1
	NB = []
	B = []
	CB = []
	CN = []
	tab = []
	NV = []
	SlV = []
	SuV = []
	ArV = []
	for i in range(n):
		NB.append('x' + str(i+1))
		NV.append('x' + str(i+1))
		if (minimize == True):
			CN.append(-int(obj_arr[i]))
		else:
			CN.append(int(obj_arr[i]))
	t = n+1
	for i in range(m):
		if (sign[i] == '='):
			B.append('x' + str(t))
			ArV.append('x' + str(t))
			t += 1
			CB.append (-M)
		elif(sign[i] == '<='):
			B.append('x' + str(t))
			SlV.append('x' + str(t))
			t += 1
			CB.append(0)
		elif (sign[i] == '>='):
			NB.append('x' + str(t))
			SuV.append('x' + str(t))
			t += 1
			CN.append(0)
			B.append('x' + str(t))
			ArV.append('x' + str(t))
			t += 1
			CB.append(-M)
	NB.append('xb')
	if (minimize == True):
		CN.append(int(obj_arr[n]))
	else:
		CN.append(-int(obj_arr[n]))

	t = n
	for i in range (m):
		row = []
		for j in range(n):
			row.append(int(arr[i][j]))
		for j in range(ex):
			row.append(0)
		row.append(int(arr[i][n]))
		if (sign[i] == '>='):
			row[t] = -1
			t += 1
		tab.append(row)
	row = []
	for i in range(N):
		s = 0
		for j in range(m):
			s += (tab[j][i] * CB[j])
		row.append(s - CN[i])
	tab.append(row)
	#print (tab)
	return (N, NB, B, CB, CN, tab, NV, SlV, SuV, ArV)

def min_col ():
	t = tab[m][0] + (M*0)
	v = 0
	for i in range(N-1):
		if ((tab[m][i] + (M*0)).coeff(M) < (t + (M*0)).coeff(M)):
			t = tab[m][i]
			v = i
		elif ((tab[m][i] + (M*0)).coeff(M) == (t + (M*0)).coeff(M)):
			if (t - tab[m][i] > 0):
				t = tab[m][i]
				v = i
	return v

def min_row():
  t = 9999999999
  u = -1
  for i in range(m):
    if (tab[i][v] != 0):
      q = tab[i][N-1] / tab[i][v]
      if ((q >= 0) and (q < t)):
        t = q
        u = i
  if (u == -1):
    print ('The problem is unbounded.')
  return u


def print_table():
	print ('\n\n')
	print ('\t\t Table {}'.format(count))
	for i in range (m+1):
		for j in range (N):
			if (j != N-1):
				print (tab[i][j], end = '\t ')
			else:
				print (tab[i][j])
	print ()
	return

def update_table():
	p = tab[u][v]
	for i in range(m+1):
		for j in range(N):
			if ((i != u) and (j != v)):
				s = tab[i][j]
				q = tab[i][v]
				r = tab[u][j]
				t = ((p*s) - (q*r)) / p
				tab[i][j] = t
	for j in range (N):
		if (j != v):
			t = tab[u][j] / p
			tab[u][j] = t
	for i in range (m+1):
		if (i != u):
			t = -tab[i][v] / p
			tab[i][v] = t
	tab[u][v] = 1 / p
	vr = NB[v]
	NB[v] = B[u]
	B[u] = vr
	co = CN[v]
	CN[v] = CB[u]
	CB[u] = co
	return


def show_optimal():
	print ('\n\nThe value of Basic variables are:')
	for i in range(m):
		print ('{} = {}'.format(B[i], tab[i][N-1]))
	print ('\n\nNon basic variables are:')
	for i in range(N-1):
		print ('{} = '.format(NB[i]), end = '')
	if (len(SlV) != 0):
		print ('\nSlack variables: ', end = '')
		for z in SlV:
			print (z, end = '   ')
	if (len(SuV) != 0):
		print ('\nSurplus variables: ', end = '')
		for z in SuV:
			print (z, end = '   ')
	if (len(ArV) != 0):
		print ('\nArtificial variables: ', end = '')
		for z in ArV:
			print (z, end = '   ')
	if (minimize):
		print ('\n\nThe optimal solution is {}'.format(-tab[m][N-1]))
	else:
		print ('\n\nThe optimal solution is {}'.format(tab[m][N-1]))

(n, m, arr, sign, obj_arr, minimize) = read()
M = var('M')
(N, NB, B, CB, CN, tab, NV, SlV, SuV, ArV) = initialize()
count = 1
while (1):
	print_table()
	v = min_col()
	t = tab[m][v]
	if (t == 0):
		print ('\n\nThe solution is optimal.\nAlternate optimal solution also exist.')
		show_optimal()
		break
	elif (((t+(M*0)).coeff(M) > 0) or (((t+(M*0)).coeff(M) == 0) and (t > 0))):
		print ('\n\nThe solution is optimal.\nUnique optimal solution only (no alternate optimal solution).')
		show_optimal()
		break
	else:
		u = min_row()
		if (u == -1):
			break
		q = tab[u][N-1] / tab[u][v]
		if (q >= 0):
			print ('u, v = {}, {}'.format(u, v))
			update_table()
	count += 1
	continue