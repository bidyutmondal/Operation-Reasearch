#Bidyut Mondal
#18MA20010
#2 Phase Method Lab 5

epsilon = 0.00000000001

#Function to print the table in desired formal
def printTable(tab, count):
	print ('\n\n')
	print ('\t\ttable {}'.format(count))
	for i in range (m+1):
		for j in range (N):
			if (j != N-1):
				print (tab[i][j], end = '\t\t')
			else:
				print (tab[i][j])
	print ()
	return

#Returns the col with least value in the last row
def minCol(tab):
	t = tab[m][0]
	v = 0
	for i in range(N-1):
		if (tab[m][i] < t):
			t = tab[m][i]
			v = i
	return v

#Returns the column with the least value expect the artificial variables(the cv array contians the index of artificial variables)
def minCol(tab, cv):
	t = tab[m][0]
	v = 0
	for i in range(N-1):
		if ((tab[m][i] < t) and (i not in cv)):
			t = tab[m][i]
			v = i
	return v

#Function to find the row with min Ratio in the most neg col
def minRow(tab, v):
	t = 1e10
	u = -1
	for i in range(m):
		if (tab[i][v] != 0):
			q = tab[i][N-1] / tab[i][v]
			if ((q >= 0) and (q < t)):
				t = q
				u = i
	if (u == -1):
		print ('The problem is Unbounded.')
	return u

#Updating the values of the simplex table
def updateTable(tab, u, v):
	p = tab[u][v]
	for i in range(m+1):
		for j in range(N):
			if ((i != u) and (j != v)):
				s = tab[i][j]
				q = tab[i][v]
				r = tab[u][j]
				t = ((p*s) - (r*q)) / p
				if (abs(t) < epsilon):
					t = 0
				tab[i][j] = t
	for j in range(N):
		if (j != v):
			t = tab[u][j] / p
			if (abs(t) < epsilon):
				t = 0
			tab[u][j] = t
	for i in range(m+1):
		if (i != u):
			t = -tab[i][v] / p
			if (abs(t) < epsilon):
				t = 0
			tab[i][v] = t
	tab[u][v] = 1 / p
	vr = nonBasicVar[v]
	nonBasicVar[v] = B[u]
	B[u] = vr
	co = coeffNonBasic[v]
	coeffNonBasic[v] = coeffBasicVar[u]
	coeffBasicVar[u] = co
	return tab

#Printing the optimum value and all the variables associated
def printOptimum():
	print ('\n\nThe value of Basic variables are:')
	for i in range(m):
		print ('{} = {}'.format(B[i], tab[i][N-1]))
	print ('\n\nNon basic variables are:')
	for i in range(N-1):
		print ('{} = '.format(nonBasicVar[i]), end = '')
	print ('0\n\nwhere')
	if (len(slackVar) != 0):
		print ('\nSlack variables: ', end = '')
		for z in slackVar:
			print (z, end = '   ')
	if (len(surplusVar) != 0):
		print ('\nSurplus variables: ', end = '')
		for z in surplusVar:
			print (z, end = '   ')
	if (len(artificialVar) != 0):
		print ('\nArtificial variables: ', end = '')
		for z in artificialVar:
			print (z, end = '   ')
	if (minimize):
		print ('\n\nThe optimal solution is {}'.format(-tab[m][N-1]))
	else:
		print ('\n\nThe optimal solution is {}'.format(tab[m][N-1]))

#Returns an array which contains the index of all the artificial variables columns
def artificialVarCol():
	coeffNonBasic.clear()
	coeffBasicVar.clear()
	flag = 0
	for vr in artificialVar:
		if vr not in nonBasicVar:
			flag = 1
	if (flag == 1):
		exit()
	else:
		tvr = artificialVar.copy()
		cv = []
		k = len(tvr)
		for i in range(k):
			vr = tvr[0]
			tvr.pop(0)
			index = nonBasicVar.index(vr)
			cv.append(index)
			for j in range(m+1):
				tab[j][index] = 0
		for i in range(N):
			if (nonBasicVar[i] in Variables):
				index = Variables.index(nonBasicVar[i])
				if (minimize):
					coeffNonBasic.append(-float(obj_arr[index]))
				else:
					coeffNonBasic.append(float(obj_arr[index]))
			else:
				coeffNonBasic.append(0)
		for i in range(m):
			if (B[i] in Variables):
				index = Variables.index(B[i])
				if (minimize):
					coeffBasicVar.append(-float(obj_arr[index]))
				else:
					coeffBasicVar.append(float(obj_arr[index]))
			else:
				coeffBasicVar.append(0)
		for j in range(N):
			s = 0
			for k in range(m):
				s += (coeffBasicVar[k] * tab[k][j])
			tab[m][j] = s - coeffNonBasic[j]
		return (cv)

#First phase of the 2 Phase method
def phase1():
	count = 1
	while (1):
		printTable(tab, count)
		v = minCol(tab, [])
		t = tab[m][v]
		if (t >= 0) and (tab[m][N-1] == 0):
			print ('\n\nPHASE 2')
			return tab
			break
		elif (t >= 0) and (tab[m][N-1] != 0):
			print ('\n\nNo solution exists')
			return False
			break
		elif (t < 0):
			u = minRow(tab, v)
			if (u == -1):
				return False
				break
			else:
				q = tab[u][N-1] / tab[u][v]
				if (q >= 0):
					print ('u, v = {}, {}'.format(u, v))
					updateTable(tab, u, v)
		count += 1
		continue

#Second phase of 2 Phase method
def phase2():
	cv = artificialVarCol()
	count = 1
	while(1):
		printTable(tab, count)
		v = minCol(tab, cv)
		t = tab[m][v]
		if (t == 0):
			print('\n\nSolution is optimal.\nAlternate optimal solution also exist')
			printOptimum()
			break
		elif(t > 0):
			print ('\n\nSolution is optimal.\nUnique optimal solution only (no alternate optimal solution).')
			printOptimum()
			break
		else:
			u = minRow(tab, v)
			if (u == -1):
				break
			else:
				q = tab[u][N-1] / tab[u][v]
				if (q >= 0):
					print ('u, v = {}, {}'.format(u, v))
					updateTable(tab, u, v)
		count += 1
		continue

#Taking all the input from the user
def readInput():
	n = int(input('\nEnter the number of variables: '))
	m = int(input('\nEnter the number of equations: '))
	print ('\nEnter the coefficients of variables in respective equations with sign and the constant value (separated by space):\n\n')
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

#Initializing all the variables in the standard form
def initialize():
	ex = sign.count('>=')
	N = n + ex + 1
	nonBasicVar = []
	B = []
	coeffBasicVar = []
	coeffNonBasic = []
	tab = []
	Variables = []
	slackVar = []
	surplusVar = []
	artificialVar = []
	for i in range(n):
		nonBasicVar.append('x' + str(i+1))
		Variables.append('x' + str(i+1))
		coeffNonBasic.append(0)
	t = n+1
	for i in range(m):
		if (sign[i] == '='):
			B.append('x' + str(t))
			artificialVar.append('x' + str(t))
			t += 1
			coeffBasicVar.append (-1)
		elif(sign[i] == '<='):
			B.append('x' + str(t))
			slackVar.append('x' + str(t))
			t += 1
			coeffBasicVar.append(0)
		elif (sign[i] == '>='):
			nonBasicVar.append('x' + str(t))
			surplusVar.append('x' + str(t))
			t += 1
			coeffNonBasic.append(0)
			B.append('x' + str(t))
			artificialVar.append('x' + str(t))
			t += 1
			coeffBasicVar.append(-1)
	nonBasicVar.append('xb')
	coeffNonBasic.append(0)
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
			s += (tab[j][i] * coeffBasicVar[j])
		row.append(s - coeffNonBasic[i])
	tab.append(row)
	return (N, nonBasicVar, B, coeffBasicVar, coeffNonBasic, tab, Variables, slackVar, surplusVar, artificialVar)

#main function
if __name__ == "__main__":
    (n, m, arr, sign, obj_arr, minimize) = readInput()
    (N, nonBasicVar, B, coeffBasicVar, coeffNonBasic, tab, Variables, slackVar, surplusVar, artificialVar) = initialize()
    count = 1
    print("\nPHASE 1\n")
    tab = phase1()
    if (tab != False):
        phase2()