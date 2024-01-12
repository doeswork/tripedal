import pandas as pd

df = pd.read_csv('/home/jeffyx/robots/tripedal/robot_walk_data.csv')
df_best = df.loc[df['Performance'] == 10]

df = df.drop(columns=['Performance', 'TimeElapsed'])

for index, row in df_best.iterrows():
    # print(row)
    
    list_of_values = row.values.tolist()
    steps = [list_of_values[i:i+7] for i in range(0, len(list_of_values), 7)]

    print("Steps:")
    print(steps)