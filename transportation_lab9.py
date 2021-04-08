#Bidyut Mondal
#18MA20010
#OR LAB 9

#taking input from the user
def read():
    totSupply = 0
    totDemand = 0
    costMat = [[0 for l1 in range(15)] for l2 in range(15)]
    src = int(input("Enter no of Source: "))
    dest = int(input("Enter the no of Destination: "))
    print("Enter the cost matrix row wise: ")
    for i in range(src):
        s = input()
        l = s.split()
        for j in range(dest):
            costMat[i][j] = int(l[j])

    supply = [None]*15
    demand = [None]*15
    s = input("Enter the Supply: ")
    l = s.split()
    for i in range(src):
        supply[i] = int(l[i])
        totSupply += supply[i]

    s = input("Enter the Demand: ")
    l = s.split()
    for i in range(dest):
        demand[i] = int(l[i])
        totDemand += demand[i]

    if (totSupply > totDemand):
        demand[dest] = totSupply - totDemand
        dest += 1
    if (totDemand > totSupply):
        supply[src] = totDemand - totSupply
        src += 1

    return ([[costMat[i][j] for j in range(dest)] for i in range(src)], [supply[i] for i in range(src)], [demand[i] for i in range(dest)])


#function used to print the path of the transportation problem
def displayPath(basic_variables, n, m):
    #print('----------------------------------------------------------------')
    path = [[0 for l1 in range(m)] for l2 in range(n)]
    for (i, j), v in basic_variables:
        path[i][j] = v
    print("\n  Allocated Cells:")
    print('\n'.join([''.join(['{:6}'.format(path[r][c]) for c in range(m)]) for r in range(n)]))
    return path


#Using North west corner method to get the initial basic feasible solution
def NWCM(supply, demand):
    i = 0
    j = 0
    pathMat = []
    while len(pathMat) < len(supply) + len(demand) - 1:
        v = min(supply[i], demand[j])
        supply[i] -= v
        demand[j] -= v
        pathMat.append(((i, j), v))
        if supply[i] == 0 and i < len(supply) - 1:
            i += 1
        elif demand[j] == 0 and j < len(demand) - 1:
            j += 1
    return pathMat


#function used to find the next cell to be added in the closed_path
def nextCells(closed_path, unallocated):
    l_cell = closed_path[-1]
    cell_r = [n for n in unallocated if n[0] == l_cell[0]]
    cell_c = [n for n in unallocated if n[1] == l_cell[1]]
    if len(closed_path) < 2:
        return cell_r + cell_c
    else:
        p_cell = closed_path[-2]
        r_move = p_cell[0] == l_cell[0]
        if r_move: return cell_c
        return cell_r


#function to calculate the total cost of transportation
def totalCost(costMat, path):
    tot = 0
    for i, row in enumerate(costMat):
        for j, cost in enumerate(row):
            tot += cost * path[i][j]
    return tot


#Applying modi method to get the minimum cost possible
def modi(pathMat):

    #At first we are calculating the ui and vj 
    U = [None] * len(costMat)
    V = [None] * len(costMat[0])
    U[0] = 0
    pathMat_copy = pathMat.copy()
    while len(pathMat_copy) > 0:
        for index, bv in enumerate(pathMat_copy):
            i, j = bv[0]
            if U[i] is None and V[j] is None: continue
                
            cost = costMat[i][j]
            if U[i] is None:
                U[i] = cost - V[j]
            else: 
                V[j] = cost - U[i]
            pathMat_copy.pop(index)
            break

    print('  U:', U)
    print('  V:', V)
    #Creating list containing ui+vj-cij and their position for the unallocated cells
    P = []
    for i, row in enumerate(costMat):
        for j, cost in enumerate(row):
            non_basic = all([p[0] != i or p[1] != j for p, v in pathMat])
            if non_basic:
                P.append(((i, j), U[i] + V[j] - cost))

    #Checking if the pathMat is minimum or not
    pathMat_is_minimum = True
    for p, v in P:
        if v > 0: pathMat_is_minimum = False

    #If the pathMat is not minimum we find closed_path in the solution and update the solution
    if pathMat_is_minimum == False:
        P_copy = P.copy()
        P_copy.sort(key=lambda w: w[1])
        enter_var_pos = P_copy[-1][0]
        basic_var_pos = [p for p, v in pathMat]

        #function to create a required closed_path to allow entering of new cell
        def formClosedPath(closed_path):
            if len(closed_path) > 3:
                can_be_closed = len(nextCells(closed_path, [enter_var_pos])) == 1
                if can_be_closed: return closed_path
            
            unallocated = list(set(basic_var_pos) - set(closed_path))
            possible_next_cells = nextCells(closed_path, unallocated)
            for next_cell in possible_next_cells:
                new_closed_path = formClosedPath(closed_path + [next_cell])
                if new_closed_path: return new_closed_path

        closed_path = formClosedPath([enter_var_pos])
        pos_path = closed_path[0::2]           #values will get added to these cells
        neg_path = closed_path[1::2]           #values will get subtracted from these cells
        get_bv = lambda pos: next(v for p, v in pathMat if p == pos)
        out_pos = sorted(neg_path, key=get_bv)[0]       #position of the outgoing cell
        out_val = get_bv(out_pos)
        
        new_pathMat = []
        #updating the path matrix
        for p, v in [bv for bv in pathMat if bv[0] != out_pos] + [(closed_path[0], 0)]:
            if p in pos_path:
                v += out_val
            elif p in neg_path:
                v -= out_val
            new_pathMat.append((p, v))

        path = displayPath(pathMat, len(costMat), len(costMat[0]))
        print('\n  Cost with the above path: ', totalCost(costMat, path))
        print('\n----------------------------------------------------------------')
        print('----------------------------------------------------------------\n')
        return modi(new_pathMat)

    return pathMat


if __name__=="__main__":

    costMat, supply, demand = read()
    pathMat = NWCM(supply.copy(), demand.copy())
    print('----------------------------------------------------------------')
    print('----------------------------------------------------------------')
    print('\n  Cost Matrix:\n')
    print('\n'.join([''.join(['{:6}'.format(costMat[r][c]) for c in range(len(costMat[0]))]) for r in range(len(costMat))]))
    print('\n  Supply:', supply)
    print('\n  Demand:', demand)
    print('----------------------------------------------------------------')
    print('----------------------------------------------------------------')
    path = displayPath(modi(pathMat), len(costMat), len(costMat[0]))
    print('\n  Minimum cost: ', totalCost(costMat, path))
    print('----------------------------------------------------------------')
    print('----------------------------------------------------------------')
