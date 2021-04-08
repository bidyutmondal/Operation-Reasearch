import numpy as np

#taking input from the user
def read():
	global r, c, payMat;
	r = int(input("Enter the number of rows: "))
	c = int(input("Enter the number of columns: "))
	payMat = np.zeros([r,c], float)
	print("Enter the payoff matrix row wise: ")
	for i in range(r):
		s = input()
		l = s.split()
		for j in range(c):
			payMat[i][j] = int(l[j])

#function to find out the saddle point
def saddle():
	global rowMin, colMax
	rowMin = np.zeros(r)
	colMax = np.zeros(c)

	for i in range(r):
		rowMin[i] = min(payMat[i])

	tempMat = np.transpose(payMat)
	for i in range(c):
		colMax[i] = max(tempMat[i])

	if(min(colMax)==max(rowMin)):
		for i in range(r):
			for j in range(c):
				if(rowMin[i]==colMax[j]):
					return (i, j)

	return (-1, -1)

#function to apply simplex method in case the game is unstable
def Simplex():
	global newMat, basic
	col = minColIndex()
	while(col):
		idx=0
		for i in range(r):
			if(newMat[idx][col-1]<=0): idx+=1
			if(newMat[i][col-1] and newMat[idx][col-1] and (newMat[i][r+c]/newMat[i][col-1] < newMat[idx][r+c]/newMat[idx][col-1]) and (newMat[i][col-1]>0)): idx=i
		row = idx+1
		div = newMat[row-1][col-1]*1.0
		if(div==0): return
		for i in range(r+c+1):
			newMat[row-1][i] /= div

		for i in range(r):
			mult = newMat[i][col-1]
			if(i!=row-1):
				for j in range(r+c+1): newMat[i][j] -= mult*newMat[row-1][j]

		basic[row-1] = col-1
		helper()
		col = minColIndex()

#helper function calculating the Zj values and Zj-Cj values
def helper():
	global newMat
	for i in range(r+c+1):
		newMat[r+1][i] = 0
		for j in range(r):
			newMat[r+1][i] += (newMat[r][basic[j]]*newMat[j][i])

	for i in range(r+c):
		newMat[r+2][i] = (newMat[r+1][i]-newMat[r][i])

#function to return the min col index
def minColIndex():
	idx = 0
	for i in range(r+c):
		if((newMat[r+2][i]<newMat[r+2][idx]) and (newMat[r+2][i]<0)): idx = i
	if(idx == 0 and newMat[r+2][0]<0): return 1
	elif(idx>0): return idx+1
	else: return 0	

if __name__=='__main__':
	read()
	print("\nPayoff Matrix: ")
	print('\n'.join([''.join(['{:6}'.format(payMat[i][j]) for j in range(c)]) for i in range(r)]))
	(rowidx, colidx) = saddle()
	strategyA = np.zeros(r)
	strategyB = np.zeros(c)
	if(rowidx != -1):
		print("\nThe game is STABLE")
		strategyA[rowidx] = 1
		strategyB[colidx] = 1
		print("\nStragies of both players:")
		print("Strategy of player A: ", strategyA)
		print("Strategy of player B: ", strategyB)
		print("The value of the game is: ", min(colMax))
		exit()

	print("\nThe game is UNSTABLE")
	k = max(-min(rowMin),0) #finding the min element of the payoff matrix
	if(k>0): payMat = payMat+k #adding -ve of min val to all elements off the pay off matrix
	global newMat, basic
	basic = []
	newMat = np.zeros([15, 15], float)

	for i in range(r):
		for j in range(c):
			newMat[i][j] = payMat[i][j]
		for j in range(c):
			newMat[i][c+i] = 1
			basic.append(c+i)
			newMat[i][c+r] = 1

	for i in range(c):
		newMat[r][i] = 1

	helper()
	Simplex()

	strategyA = [] #strategy probability for player A
	strategyB = [] #strategy probability for player B	
	val = 1/newMat[r+1][r+c]
	for i in range(c):
		flag = 0
		for j in range(r):
			if(basic[j]==i):
				flag=1
				break
		if(flag): strategyB.append(newMat[j][r+c]*val)
		else: strategyB.append(0)

	for i in range(r): strategyA.append(newMat[r+1][c+i]*val)

	print("\nStragies of both players:")
	print("Strategy of player A: ", strategyA)
	print("Strategy of player B: ", strategyB)
	print("\nThe value of the game is: ", val-k)