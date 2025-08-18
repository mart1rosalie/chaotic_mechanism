import mixer as m

def elementary_of(mat):
    elementary = False
    candidat = mat.propose_elementary()
    if candidat == mat:
        elementary = True
    while elementary is False:
        new = candidat.propose_elementary()
        if candidat != new:
            candidat = new
        else:
            elementary = True
    return candidat

def left_elementary(mat):
    left = m.Mixer(mat.size-1, mat.matrix.getA()[0:mat.size-1, 0:mat.size-1])
    return elementary_of(left)

def right_elementary(mat):
    right = m.Mixer(mat.size-1, mat.matrix.getA()[1:mat.size, 1:mat.size])
    return elementary_of(right)

if __name__ == "__main__": 
    # Unique initial mixer of size 2
    print("Mixer of size 2")
    A = m.Mixer(2, '0 0; 0 1')
    print(A, " = A")
    # Concatenation of A+A
    print("Concatenation")
    res = A.concatenate_after(A)
    print(res, " = A + A")
    print("Mixers of size 3")
    B = elementary_of(list(res.sub(3))[1])
    C = elementary_of(list(res.sub(3))[0])
    print(B, "= B ")
    print(C, "= C ")

    list_of_set = list()
    a = m.Mixer(2, '0 0; 0 1')
    list_of_set.append({a})
    for index, size in enumerate(range(2, 6), 1):
        list_of_candidates = set()
        for elementary in list_of_set[index-1]:
            for other_elementary in list_of_set[index-1]:
                temp = other_elementary.concatenate_after(elementary).sub(size+1)
                for submixer in temp:
                    list_of_candidates.add(submixer)
        list_of_set.append(set())
        for candidate in list_of_candidates:
            list_of_set[index].add(elementary_of(candidate))
    for size, a_set in enumerate(list_of_set, 2):
        print(size, len(a_set))
