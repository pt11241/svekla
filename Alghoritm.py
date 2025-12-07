import numpy as np

class Alghoritm:
    
    @staticmethod
    def greedy_strategy(S):
        n = S.shape[0]
        available = set(range(n))
        order = []
        for j in range(n):
            i = max(available, key=lambda x: S[x, j])
            order.append(i)
            available.remove(i)
        return order

    @staticmethod
    def thrifty_strategy(S):
        n = S.shape[0]
        available = set(range(n))
        order = []
        for j in range(n):
            i = min(available, key=lambda x: S[x, j])
            order.append(i)
            available.remove(i)
        return order

    @staticmethod
    def thrifty_greedy_strategy(S, nu):
        n = S.shape[0]
        available = set(range(n))
        order = []
        for j in range(n):
            if j < nu-1:
                i = min(available, key=lambda x: S[x, j])
            else:
                i = max(available, key=lambda x: S[x, j])
            order.append(i)
            available.remove(i)
        return order

    @staticmethod
    def greedy_thrifty_strategy(S, nu):
        n = S.shape[0]
        available = set(range(n))
        order = []
        for j in range(n):
            if j < nu-1:
                i = max(available, key=lambda x: S[x, j])
            else:
                i = min(available, key=lambda x: S[x, j])
            order.append(i)
            available.remove(i)
        return order

    @staticmethod
    def TkG_strategy(S, nu, k):
       
        n = S.shape[0]
        available = set(range(n))
        order = []
        for j in range(n):
            if j < nu-1:
                # сортируем оставшиеся партии по значению S[:, j]
                sorted_parties = sorted(available, key=lambda x: S[x, j])
                i = sorted_parties[k-1]  # k-я позиция
            else:
                i = max(available, key=lambda x: S[x, j])
            order.append(i)
            available.remove(i)
        return order

    @staticmethod
    def CTG_strategy(S, b):
        n = S.shape[0]
        
        order = sorted(range(n), key=lambda i: b[i], reverse=True)
        
        return order
