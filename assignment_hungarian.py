import random
import numpy as np

class Assignment:
	
	#constructor
    def __init__(self):
        self.costMat = self.read()
        self.Col = self.costMat.shape[1]
        self.Row = self.costMat.shape[0]        
        self.sz_ = len(self.costMat)
        self.shp_ = self.costMat.shape
        self.res_ = []
        self.tot_cost = 0

    #function to calculate the result list
    def calculate(self):
        res_mat = self.costMat.copy()
        for idx, row in enumerate(res_mat): res_mat[idx] -= row.min()  #subtract row min from each row
        for idx, column in enumerate(res_mat.T): res_mat[:, idx] -= column.min()  #subtract column min from each col
        tot_cov = 0
        #we use min no of row/column to cover all zeroes in the cost matrix
        #if total covered rows+columns is not equal to size of matrix the we adjust the matrix and continue the process
        while tot_cov < self.sz_:
            cov_z = self.zero__(res_mat)
            cov_r = self._z_cov_r
            cov_c = self._z_cov_c
            tot_cov = len(cov_r) + len(cov_c)
            #calculate minimum uncovered number and adjust the matrix  
            if tot_cov < self.sz_:
                elts = []
                for row_idx, row in enumerate(res_mat):
                    if row_idx not in cov_r:
                        for idx, ele in enumerate(row):
                            if idx not in cov_c:
                                elts.append(ele)

                min_uncovered_num = min(elts)
                print("Min uncovered elements : ", min_uncovered_num)
                adjusted_matrix = res_mat
                print("Adjusted Matrix : ")
                print(adjusted_matrix)
                #add min uncovered number to required elts
                for row in cov_r: adjusted_matrix[row] += min_uncovered_num
                for column in cov_c: adjusted_matrix[:, column] += min_uncovered_num
                m_matrix = np.ones(self.shp_, dtype=int) * min_uncovered_num
                #subtract min un uncovered number from required elts
                adjusted_matrix -= m_matrix
                res_mat = adjusted_matrix
        #Searching one zero row and columns
        exp_res = min(self.Col, self.Row)
        zero_loc = (res_mat == 0)
        #adding to result and deleting the row/columns
        while len(self.res_) != exp_res:
            marked_r = np.array([], dtype=int)
            marked_c = np.array([], dtype=int)
            for idx, row in enumerate(zero_loc):
                row_idx = np.array([idx])
                if np.sum(row) == 1:
                    column_idx, = np.where(row)
                    marked_r, marked_c = self.mark_rnc(marked_r, marked_c, row_idx, column_idx)

            for idx, column in enumerate(zero_loc.T):
                column_idx = np.array([idx])
                if np.sum(column) == 1:
                    row_idx, = np.where(column)
                    marked_r, marked_c = self.mark_rnc(marked_r, marked_c, row_idx, column_idx)

            matched_r, matched_c = marked_r, marked_c
            tot_matched = len(matched_r) + len(matched_c)
            if tot_matched == 0:
            	#Selecting row & column combination with min no. of zeros
                rows, columns = np.where(zero_loc)
                z_cnt = []
                for idx, row in enumerate(rows):
                    tot_z = np.sum(zero_loc[row]) + np.sum(zero_loc[:, columns[idx]])
                    z_cnt.append(tot_z)
                indices = z_cnt.index(min(z_cnt))
                row = np.array([rows[indices]])
                column = np.array([columns[indices]])
                matched_r, matched_c = row, column
            #deleting the rows & columns
            for row in matched_r: zero_loc[row] = False
            for column in matched_c: zero_loc[:, column] = False
            result_lists = zip(matched_r, matched_c)
            for result in result_lists:
                row, column = result
                if row < self.Row and column < self.Col:
                    new_result = (int(row), int(column))
                    self.res_.append(new_result)    #adding results to the list
        #calculating the total min cost
        value = 0
        for row, column in self.res_:
            value += self.costMat[row, column]
        self.tot_cost = value

    #to mark row/col if it is nt marked
    def mark_rnc(self, marked_r, marked_c, row_idx, column_idx):
        new_marked_r = marked_r
        new_marked_c = marked_c
        if not (marked_r == row_idx).any() and not (marked_c == column_idx).any():
            new_marked_r = np.insert(marked_r, len(marked_r), row_idx)
            new_marked_c = np.insert(marked_c, len(marked_c), column_idx)

        return new_marked_r, new_marked_c

    #helper function to find zeros in matrix and storing other variables as class variables
    def zero__(self, z_matrix):
        self._zero_loc = (z_matrix == 0)
        self._zeroshp_ = z_matrix.shape
        self._choices = np.zeros(self._zeroshp_, dtype=bool)
        self._z_marked_r = []
        self._z_marked_c = []
        self.cover_zero()
        self._z_cov_r = list(set(range(self._zeroshp_[0])) - set(self._z_marked_r))
        self._z_cov_c = self._z_marked_c

	#helper function to cover all single zeros in the cost matrix
    def cover_zero(self):
        while True:
            # inittially clear all, then mark all rows, cols that are unmarked, if no marked rows, cols then stop
            self._z_marked_r = []
            self._z_marked_c = []
            for idx, row in enumerate(self._choices):
                if not row.any(): self._z_marked_r.append(idx)
            if not self._z_marked_r: return True
            num_z_marked_c = self.mark_new_c()
            if num_z_marked_c == 0: return True
            while self.choice_in_zmc():
                num_z_marked_r = self.mark_new_r()
                if num_z_marked_r == 0: return True
                num_z_marked_c = self.mark_new_c()
                if num_z_marked_c == 0: return True
            choice_column_idx = self.find_mrk_c()
            #search zero in the col indxed that does not have a row with a choice, accomodate it, delete old choice, and set 0 to choice
            while choice_column_idx is not None:
                choice_row_idx = self.find_mrk_r(choice_column_idx)
                new_choice_column_idx = None
                if choice_row_idx is None:
                    choice_row_idx, new_choice_column_idx = self.find_opt_idx(choice_column_idx)
                    self._choices[choice_row_idx, new_choice_column_idx] = False
                self._choices[choice_row_idx, choice_column_idx] = True
                choice_column_idx = new_choice_column_idx

    #function to mark rows unmarked with zeros in marked rows
    def mark_new_c(self):
        num_z_marked_c = 0
        for idx, column in enumerate(self._zero_loc.T):
            if idx not in self._z_marked_c:
                if column.any():
                    row_indices, = np.where(column)
                    zeros_in_z_marked_r = (set(self._z_marked_r) & set(row_indices)) != set([])
                    if zeros_in_z_marked_r:
                        self._z_marked_c.append(idx)
                        num_z_marked_c += 1

        return num_z_marked_c

    #function to mark cols unmarked with choices in marked cols
    def mark_new_r(self):
        num_z_marked_r = 0
        for idx, row in enumerate(self._choices):
            if idx not in self._z_marked_r:
                if row.any():
                    column_idx, = np.where(row)
                    if column_idx in self._z_marked_c:
                        self._z_marked_r.append(idx)
                        num_z_marked_r += 1

        return num_z_marked_r

    #returns true if there is a choice
    def choice_in_zmc(self):
        for column_idx in self._z_marked_c:
            if not self._choices[:, column_idx].any(): return False
        return True

    #returns marked cols with choices
    def find_mrk_c(self):
        for column_idx in self._z_marked_c:
            if not self._choices[:, column_idx].any(): return column_idx

    #returns row without choices
    def find_mrk_r(self, choice_column_idx):
        row_indices, = np.where(self._zero_loc[:, choice_column_idx])
        for row_idx in row_indices:
            if not self._choices[row_idx].any(): return row_idx
        return None

    #returns a optimal row idx for choices
    def find_opt_idx(self, choice_column_idx):
        row_indices, = np.where(self._zero_loc[:, choice_column_idx])
        for row_idx in row_indices:
            column_indices, = np.where(self._choices[row_idx])
            column_idx = column_indices[0]
            if self.find_mrk_r(column_idx) is not None:
                return row_idx, column_idx

        random.shuffle(row_indices)
        column_idx, = np.where(self._choices[row_indices[0]])
        return row_indices[0], column_idx[0]
    
    #taking input from the user
    def read(self):
        rows = int(input('Enter the no of rows: '))
        cols = int(input('Enter the no of columns: '))
        costs = [[0 for c in range(cols)] for r in range(rows)]
        print("Enter the cost matrix row wise: ")
        for i in range(rows):
            s = input()
            l = s.split()
            for j in range(cols):
                costs[i][j] = int(l[j])

        
        costs = np.array(costs)
        if (rows  > cols) :
          costs = np.c_[costs, np.zeros((rows, rows-cols))]
        if ( rows < cols ) :
          costs = np.r_[costs, np.zeros((cols-rows, cols))]
        print("Cost Matrix :")
        print(costs)

          


        return np.array(costs)

    #returns list containing the job done by each worker
    def get_costs(self): return self.res_.sort()

    #function to display the cost of each job to be completed
    def display_costs(self):
        self.res_.sort()
        for row, column in self.res_:
            print('Job',row+1,' completed by Worker',column+1, ', Cost: ',self.costMat[row, column], sep='')

    #return the total minimum cost for all jobs to be completed
    def get_total_cost(self): return self.tot_cost


if __name__ == '__main__':
    assignment = Assignment()   #creating assignmnet object
    assignment.calculate()
    print()
    assignment.display_costs()
    print("\nTotal Minimum Cost: ", assignment.get_total_cost())