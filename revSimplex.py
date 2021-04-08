#Bidyut Mondal
#18MA20010
#OR LAB 7 Revised Simplex

import numpy as np
M = 1e5
def read():
    global var, n, mat, count, obj
    var = int(input("Enter the number of variables: "))
    n = int(input("Enter the number of equations: "))
    mat = [[]for i in range(n)]     # coefficient matrix
    nmat = [[]for i in range(n)]        #coefficient matrix without artificial and surplus variable
    cnst = []       # constant term in constraint
    arr = []        # to store artificial variable
    
    for i in range(var):
        arr.append(0)
        
    count = var
    
    inq = []
    for i in range(n):
        for j in range(var):
            nmat[i].append(float(input(F'{"X["}{i}{","}{j}{ "] : "}')))
        
        inq.append((input(F'{"Enter the inquality(<=, >=, ==) in cnsttraint" } {i+1} {" : "}')))
        
        cnst.append(float(input(F'{"B["}{i}{ "] : "}')))
    
    print("\n")
    for i in range(n):
        for j in nmat[i]:
            mat[i].append(j)
    
    count = var-1
    obj = []
    for j in range(var):
        obj.append(0)
        
    for i in range(n):
        if(inq[i] == "<="):
            count += 1
            obj.append(0)
            arr.append(0)
            for j in range(n):
                if(i != j):
                    mat[j].append(0)
            mat[i].append(1)
        elif(inq[i] == ">="):
            count += 2
            obj.append(0)
            arr.append(0)
            obj.append(-1*M)
            arr.append(1)
            for j in range(n):
                if(i!=j):
                    mat[j].append(0)
                    mat[j].append(0)
            mat[i].append(-1)
            mat[i].append(1)
        elif(inq[i] == "=="):
            count += 1
            obj.append(-1*M)
            arr.append(1)
            for j in range(n):
                if(i != j):
                    mat[j].append(0)
            mat[i].append(1)
    
    count += 1
    for i in range(n):
        mat[i].append(cnst[i])
    
    print("Coefficient Matrix : ")
    for i in range(n): print(mat[i])
    
    s = int(input("Choose - 1.Minimize  2.Maximize : "))
    print("\n")
    print("Enter the coefficient of objective function:")
    for j in range(var):
        coe = float(input(F'{"X"}{j+1}{ " : "}'))
        if(s == 1):
            obj[j] = -1*coe
        else:
            obj[j] = coe
    
    print("\n Objective function : ", end ='')
    print(obj)


def revSimplex():
    global basis, basic, b, n_b
    basis = []          #to store basic variables during each iteration
    b = [[]for i in range(n)]       # n*n basis matrix to store coefficients of basic variables in each constraints 
    for i in range(n):
        for j in range(var,count):
            if(mat[i][j] == 1):
                basis.append(j)
                for k in range(n):
                    b[i].append(mat[k][j])
    
    n_b = [[]for i in range(n)]
    for j in range(n):
        for k in range(n):
            if(j == k):
                n_b[j].append(1)
            elif(j!=k):
                n_b[j].append(0)
    
    basic = []
    for j in range(count):
        basic.append(0)
    for j in range(n):
        basic[basis[j]] = 1


if __name__ == '__main__':
    read()
    revSimplex()
    itr = 0
    print("\n------------------------------------------------------------------")
    while(1):
        print("------------------------------------------------------------------\n")
        print("Iteration : " , itr+1, "\n")
        cb = [obj[basis[i]]for i in range(n)]       #coefficients of basic variables in objective function    
        print("Basic variables : ", end='')
        for j in range(n):
            print(f"x{basis[j]+1}, ", end='')
        b = np.dot(b, n_b)                      #multiplying new basis matrix to old basis matrix
        print("\nTransform basis matrix")
        print(b, "\n")
        det = np.linalg.det(b)
        if(det == 0):   #checking determinant is  zero or not
            print("NO SOLUTION ")
            break 
        elif(det != 0):
            inv_b = np.linalg.inv(b)

        # y = cb*inverse(b)
        y = np.dot(cb, inv_b)
        col = -1
        mx = 0
        for i in range(count):
            if(basic[i]==0):
                coeff = [[]for k in range(n)]
                for j in range(n):
                    coeff[j].append(mat[j][i])
                z = np.dot(y,coeff)
                if(mx < obj[i]-z):
                    mx = obj[i]-z
                    col = i
        if(col == -1):
            ans = 0
            f = 0
            for j in range(n):
                if(obj[basis[j]] == -1*M):  # if an artificial variable present in basis matrix but cj-zj<0 so no sloution
                    f = 1
                    break
    
            if(f == 1):
                print("NO SOLUTION ")
                break
            elif(f == 0):
                for j in range(n):
                    print(f"x{basis[j]+1} = {mat[j][count]}")
                    if(basis[j] < var):
                        ans+=(obj[basis[j]]*mat[j][count])
                print("OPTIMAL VALUE = ", end = '')
                if(f == 1):
                    print(-1*ans)
                else:
                    print(ans)
                break
    
    
        n_cff = [[mat[j][col]]for j in range(n)]
    
        tmp = np.dot(inv_b, n_cff)
        rep = [[tmp[j][0]]for j in range(n)]
    
        row = -1
        zm=1e5
        # we have to find smallest ratio
        for j in range(n):
            if(rep[j][0]>0):
                if(zm>mat[j][count]/rep[j][0]):
                    zm = mat[j][count]/rep[j][0]
                    row = j
    
        if(row != -1):
            for j in range(n):
                if(j != row):
                    mat[j][count] -= rep[j][0]*zm
            mat[row][count] = zm
        elif(row == -1):    #if there is no entering variable but cj-zj>0 so unbounded solution
            print("UNBOUNDED SOLUTION")
            break
    
        basis[row] = col
    
        for j in range(count):
            basic[j] = 0
        for j in range(n):
            basic[basis[j]] = 1
    
        for j in range(n):
            for k in range(n):
                if(j == k):
                    n_b[j][k] = 1
                elif(j!=k):
                    n_b[j][k] = 0
    
        for j in range(n):
            n_b[j][row] = rep[j][0]     # entering modified variables of entering variables
        print("\n------------------------------------------------------------------")
        itr+=1
    print("\n------------------------------------------------------------------")