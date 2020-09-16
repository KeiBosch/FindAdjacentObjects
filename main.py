import numpy as np
import pandas as pd

df = pd.read_csv(r"./feature_small.csv")

print(df)

yoko_ls = pd.DataFrame(
    columns=["fid_from", "fid_to", "distance", "common_height", "angle"])

for i in range(len(df)):
    for j in range(len(df)):
        mesh_diff_lat = abs(df.iloc[j, 2] - df.iloc[i, 2])
        mesh_diff_lon = abs(df.iloc[j, 3] - df.iloc[i, 3])

        # Limit the adjacent mesh for performance
        if mesh_diff_lat > 1 or mesh_diff_lon > 1:
            continue
        dist_hr = np.round(np.sqrt(
            (df.iloc[j, 7] - df.iloc[i, 4]) ** 2 + (df.iloc[j, 8] - df.iloc[i, 5]) ** 2), decimals=3)
        # print(dist_hr)
        # If self.start and other.end exists horizontally within 0.6m -> go
        if df.iloc[i, 1] != df.iloc[j, 1] and dist_hr < 0.6:
            # If they overlap vertically -> go
            if df.iloc[i, 11] <= df.iloc[j, 11]:
                c_h = np.round(
                    df.iloc[i, 11] + df.iloc[i, 10] - df.iloc[j, 11], decimals=3)
            elif df.iloc[i, 11] > df.iloc[j, 11]:
                c_h = np.round(
                    df.iloc[j, 11] + df.iloc[j, 10] - df.iloc[i, 11], decimals=3)
            # But if overlap is within 0.1m, remove due to manual blur
            if c_h > 0.1:
                # caluculate angle between two objects
                vector_from = np.array(
                    [df.iloc[i, 7] - df.iloc[i, 4], df.iloc[i, 8] - df.iloc[i, 5]])
                vector_to = np.array(
                    [df.iloc[j, 7] - df.iloc[j, 4], df.iloc[j, 8] - df.iloc[j, 5]])
                norm_from = np.linalg.norm(vector_from)
                norm_to = np.linalg.norm(vector_to)
                inner = np.inner(vector_from, vector_to)
                cos_theta = inner/(norm_from * norm_to)
                angle = np.round(np.rad2deg(
                    np.arccos(cos_theta)), decimals=1)
                # the angle is within 30 degrees -> adjacent
                if angle < 30:
                    row = pd.Series([df.iloc[i, 1], df.iloc[j, 1], dist_hr, c_h, angle],
                                    index=["fid_from", "fid_to", "distance", "common_height", "angle"], name=0)
                    yoko_ls = yoko_ls.append(row)
print(yoko_ls)

yoko_ls.to_csv(r"./test1.csv", index=False)


tate_ls = pd.DataFrame(
    columns=["fid_from", "fid_to", "distance", "common_width", "angle"])

for i in range(len(df)):
    for j in range(len(df)):

        # If distance between self and other is within 0.3m,
        # they are judged as vertically adjacent.

        dist_hr2 = np.round(np.sqrt(
            (df.iloc[j, 4] - df.iloc[i, 4]) ** 2 + (df.iloc[j, 5] - df.iloc[i, 5]) ** 2), decimals=3)

        if df.iloc[i, 1] != df.iloc[j, 1] and dist_hr2 < 0.3:
            # If self is below, self.Y + Height - other.Y < XXm
            if df.iloc[i, 11] <= df.iloc[j, 11]:
                c_v = df.iloc[j, 11] - df.iloc[i, 11]
            # If self is over, other.Y + Height - self.Y < XXm
            elif df.iloc[i, 11] > df.iloc[j, 11]:
                c_v = df.iloc[i, 11] - df.iloc[j, 11]

        print(c_v)
print(tate_ls)

tate_ls.to_csv(r"./tate.csv", index=False)
