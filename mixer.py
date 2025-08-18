import numpy as np
import pandas as pd
from numpy import linalg as LA

class Mixer(object):
    """Algrebraic description of a mixer with a matrix"""

    def __init__(self, size =1, content='0'):
        self.size = size
        self.matrix = np.matrix(content)

    def __repr__(self):
        return "\n"+self.matrix.__str__()+" "

    def __str__(self):
        return self.matrix.__str__()

    def __hash__(self):
        return hash(str(self.matrix.getA()))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def concatenate(self, A, B):
        a = A.size
        b = B.size
        a_s = np.zeros(a*b)
        for i in range(1, a*b+1):
            a_s[i-1] = i
        a_exp = np.zeros([a*b, a*b], dtype=int)
        for i in range(1, a+1):
            for j in range(1, a+1):
                for k in range(1, b+1):
                    for l in range(1, b+1):
                        a_exp[(i-1)*b+k-1, (j-1)*b+l-1] = A.get(i, j)
        a_e = np.zeros(a*b)
        for i in range(1, a*b+1):
            pos = 0
            neg = 0
            for j in range(i+1, a*b+1):
                if a_exp[i-1, j-1] % 2 == 1:
                    pos = pos+1
            for j in range(1, i):
                if a_exp[i-1, j-1] % 2 == 1:
                    neg = neg+1
            a_e[i+pos-neg-1] = i
        b_s = np.zeros(a*b)
        k = 1
        for j in range(1, b+1):
            for i in range(1, a+1):
                #  print(i, j)
                b_s[k-1] = a_e[(i-1)*b+j-1]
                k += 1
        a_tra = np.zeros([a*b, a*b], dtype=int)
        for k in range(1, a*b):
            l = self.find(b_s, a_e[k-1])
            for p in range(k+1, a*b+1):
                q = self.find(b_s, a_e[p-1])
                if q < l:
                    i = self.find(a_s, a_e[k-1])
                    j = self.find(a_s, a_e[p-1])
                    a_tra[i, j] = 1
                    a_tra[j, i] = 1
        b_exp = np.zeros([a*b, a*b], dtype=int)
        for i in range(1, a+1):
            for j in range(1, a+1):
                if A.get(i, i) % 2 == 0 and A.get(j, j) % 2 == 0:
                    for k in range(1, b+1):
                        for l in range(1, b+1):
                            b_exp[(i-1)*b+k-1, (j-1)*b+l-1] = B.get(k, l)
                elif A.get(i, i) % 2 == 0 and A.get(j, j) % 2 == 1:
                    for k in range(1, b+1):
                        for l in range(1, b+1):
                            b_exp[(i-1)*b+k-1, (j-1)*b+l-1] = B.get(k, b-l+1)
                elif A.get(i, i) % 2 == 1 and A.get(j, j) % 2 == 0:
                    for k in range(1, b+1):
                        for l in range(1, b+1):
                            b_exp[(i-1)*b+k-1, (j-1)*b+l-1] = B.get(b-k+1, l)
                else:
                    for k in range(1, b+1):
                        for l in range(1, b+1):
                            b_exp[(i-1)*b+k-1, (j-1)*b+l-1] = B.get(b-k+1, b-l+1)
        result = a_exp+a_tra+b_exp
        return Mixer(a*b, np.copy(result))

    def find(self, array, val):
        i=0
        while array[i]!=val:
            i+=1
        return i

    def concatenate_before(self, C):
        return self.concatenate(self, C)

    def concatenate_after(self, C):
        return self.concatenate(C, self)

    def get(self, i, j):
        return self.matrix.item(i-1, j-1)

    def sub(self, subsize):
        """Get a set of submatrix of size subsize from a mixer"""
        result = set()
        if subsize <= self.size:
            for i in range(0, self.size-subsize+1):
                result.add(Mixer(subsize, self.matrix.getA()[i:i+subsize, i:i+subsize]))
        return result

    def criteres(self):
        """ Computation of criteria used to select elementary matrix """
        count_decrease = 0
        for row in range(1, self.size):
            if self.get(row+1, row+1) - self.get(row, row) == -1:
                count_decrease += 1
        infinite_norm = int(LA.norm(self.matrix, np.inf))
        rows_values = np.sum(np.abs(self.matrix), axis = 0)
        trace = abs(int(self.matrix.trace()[0, 0]))
        index_max = self.size - int(np.max(np.flatnonzero(rows_values == np.max(rows_values))))
        index_min = 1 + int(np.min(np.flatnonzero(rows_values == np.min(rows_values))))
        return (infinite_norm, trace, index_max, index_min, count_decrease)

    def inverse(self):
        """ Algrebraic relation """
        inv = np.zeros([self.size, self.size], dtype=int)
        for i in range(1, self.size+1):
            for j in range(1, self.size+1):
                if i != j:
                    inv[i-1, j-1] = -self.get(i, j)-1
                else:
                    inv[i-1, j-1] = -self.get(i, j)
        return Mixer(self.size, inv)

    def transpose(self):
        """ Algrebraic relation """
        tra = np.zeros([self.size, self.size], dtype=int)
        for i in range(1, self.size+1):
            for j in range(1, self.size+1):
                tra[i-1, j-1] = self.get(self.size-i+1, self.size-j+1)
        return Mixer(self.size, tra)

    def concat_torsion(self, val):
        """ Algrebraic relation """
        tor = np.zeros([self.size, self.size], dtype=int)
        for i in range(1, self.size+1):
            for j in range(1, self.size+1):
                tor[i-1, j-1] = self.get(i, j)+val
        return Mixer(self.size, tor)

    def list_of_potential_matrix(self):
        """ Creation of a list of matrix using algrebraic relations """
        new_set = set()
        matrix_to_add = self
        new_set.add((matrix_to_add, matrix_to_add.criteres()))
        matrix_to_add = self.inverse()
        new_set.add((matrix_to_add, matrix_to_add.criteres()))
        matrix_to_add = self.transpose()
        new_set.add((matrix_to_add, matrix_to_add.criteres()))
        matrix_to_add = self.transpose().inverse()
        new_set.add((matrix_to_add, matrix_to_add.criteres()))
        matrix_to_add = self.concat_torsion(1)
        new_set.add((matrix_to_add, matrix_to_add.criteres()))
        matrix_to_add = self.concat_torsion(1).inverse()
        new_set.add((matrix_to_add, matrix_to_add.criteres()))
        matrix_to_add = self.concat_torsion(1).inverse().transpose()
        new_set.add((matrix_to_add, matrix_to_add.criteres()))
        matrix_to_add = self.concat_torsion(1).transpose()
        new_set.add((matrix_to_add, matrix_to_add.criteres()))
        matrix_to_add = self.concat_torsion(-1)
        new_set.add((matrix_to_add, matrix_to_add.criteres()))
        matrix_to_add = self.concat_torsion(-1).inverse()
        new_set.add((matrix_to_add, matrix_to_add.criteres()))
        matrix_to_add = self.concat_torsion(-1).inverse().transpose()
        new_set.add((matrix_to_add, matrix_to_add.criteres()))
        matrix_to_add = self.concat_torsion(-1).transpose()
        new_set.add((matrix_to_add, matrix_to_add.criteres()))
        the_list = [*new_set]
        return(the_list)

    def propose_elementary(self):
        """ Select the minimal linking matrix from equivalent matrices """
        the_list = self.list_of_potential_matrix()
        df = pd.DataFrame.from_records(the_list, columns=['matrix', 'metric'])
        df[['infinity', 'trace', 'index_max_rev','index_min', 'count_decrease']] = pd.DataFrame(df.metric.tolist(), index=df.index)
        df['c'] = range(len(df))
        df_sorted = df.sort_values(by=['infinity', 'trace', 'index_max_rev', 'index_min', 'count_decrease'])
        selected = list(df_sorted['c'])[0]
        return(the_list[selected][0])
