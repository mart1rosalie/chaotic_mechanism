import mixer as m

if __name__ == "__main__": 
    A = m.Mixer(2, '1 1; 1 2')
    B = A.concatenate_before(A)
    print("Linking matrix of the template of the Burke-Shaw attractor")
    print(B)
