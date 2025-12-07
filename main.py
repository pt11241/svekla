from Alghoritm import Alghoritm
import numpy as np
from scipy.optimize import linear_sum_assignment
from MatrixOfStates import MatrixOfStates
 

def main():
    
    cost = np.array([[1, 2, 3], [3, 2, 1], [3, 3, 3]])
    row_ind, col_ind = linear_sum_assignment(cost, maximize=True)
    m = MatrixOfStates(3, 0.16, 0.2, 0.93, 0.98)  

    matrixC = m.matrix()
    a = Alghoritm.greedy_strategy(cost)
    print(cost[row_ind, a].sum())



        
if __name__ == '__main__':
    main()