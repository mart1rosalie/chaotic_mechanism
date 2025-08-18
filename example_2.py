import mixer as m
import pandas as pd

if __name__ == "__main__": 
    print("Linking matrix of the template of the Burke-Shaw attractor")
    B = m.Mixer(4, '3 2 2 3; 2 2 2 3; 2 2 3 3; 3 3 3 4')
    print(B)

    the_list = B.list_of_potential_matrix()
    df = pd.DataFrame.from_records(the_list, columns=['matrix', 'metric'])
    df[['infinity', 'trace', 'index_max_rev','index_min', 'count_decrease']] = pd.DataFrame(df.metric.tolist(), index=df.index)
    df_sorted = df.sort_values(by=['infinity', 'trace', 'index_max_rev', 'index_min', 'count_decrease'])
    print(df_sorted)
    first = df_sorted
    candidate_minimal_1 = list(df_sorted['matrix'])[0] # mixer of first row 

    the_list = candidate_minimal_1.list_of_potential_matrix()
    df = pd.DataFrame.from_records(the_list, columns=['matrix', 'metric'])
    df[['infinity', 'trace', 'index_max_rev','index_min', 'count_decrease']] = pd.DataFrame(df.metric.tolist(), index=df.index)
    df_sorted = df.sort_values(by=['infinity', 'trace', 'index_max_rev', 'index_min', 'count_decrease'])
    print(df_sorted)
    candidate_minimal_2 = list(df_sorted['matrix'])[0] # mixer of first row 

    the_list = candidate_minimal_2.list_of_potential_matrix()
    df = pd.DataFrame.from_records(the_list, columns=['matrix', 'metric'])
    df[['infinity', 'trace', 'index_max_rev','index_min', 'count_decrease']] = pd.DataFrame(df.metric.tolist(), index=df.index)
    df_sorted = df.sort_values(by=['infinity', 'trace', 'index_max_rev', 'index_min', 'count_decrease'])
    print(df_sorted)
    candidate_minimal_3 = list(df_sorted['matrix'])[0] # mixer of first row 

    the_list = candidate_minimal_3.list_of_potential_matrix()
    df = pd.DataFrame.from_records(the_list, columns=['matrix', 'metric'])
    df[['infinity', 'trace', 'index_max_rev','index_min', 'count_decrease']] = pd.DataFrame(df.metric.tolist(), index=df.index)
    df_sorted = df.sort_values(by=['infinity', 'trace', 'index_max_rev', 'index_min', 'count_decrease'])
    print(df_sorted)
    candidate_minimal_4 = list(df_sorted['matrix'])[0] # mixer of first row 

    print("Linking matrix of the template of the Burke-Shaw attractor")
    print(B)
    print("Step 1")
    print(candidate_minimal_1)
    print("Step 2")
    print(candidate_minimal_2)
    print("Step 3")
    print(candidate_minimal_3)
    print("Step 4 : the minimal linking matrix is obtained")
    print(candidate_minimal_4)

