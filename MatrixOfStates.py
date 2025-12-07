import numpy as np


class MatrixOfStates:
    def __init__(self, size, stA, endA, stB, endB):
        self._size = size
        self._stA = stA
        self._endA = endA
        self._stB = stB
        self._endB = endB

    def __createBcoefs(self, dist='evenly'):
        if(dist == 'evenly'):
            coefsB = np.random.uniform(self._stB, self._endB, self._size * (self._size - 1))
            coefsB = coefsB.reshape(self._size, self._size - 1)
            return coefsB
        
        elif (dist == 'concentrated'):
            lenghtB = self._endB - self._stB
            dots = np.random.uniform(self._stB + lenghtB / 4, 
                                     self._endB - lenghtB / 4, 
                                     self._size)
            
            lenghts = np.random.uniform(0, lenghtB / 4, self._size)

            coefsB = np.empty((0, self._size))

            for i in range(len(dots)):
                vec = np.random.uniform(dots[i] - lenghts[i], 
                                           dots[i] + lenghts[i], 
                                           self._size)
                
                coefsB = np.vstack((coefsB, vec.reshape(1, -1)))
            return coefsB
        



    def matrix(self) -> np.array:
        coefsA = np.random.uniform(self._stA, self._endA, self._size)

        coefsB =  self.__createBcoefs(dist='evenly')
        
        coefsC = np.array(coefsA.reshape(-1, 1))
                
        for i in range(self._size - 1):
            vec = coefsC[:, i] * coefsB[:, i]
            coefsC = np.hstack((coefsC, vec.reshape(-1, 1)))
        
        return coefsC


