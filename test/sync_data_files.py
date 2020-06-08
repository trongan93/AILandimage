import pandas as pd

input1_path = "/mnt/d/Landsat/input_0_280.csv"
input2_path = "/mnt/d/Landsat/input_281_560.csv"

data1 = pd.read_csv(input1_path)
data2 = pd.read_csv(input2_path)
# merge_data = data1.append(data2)
merge_data = pd.concat([data1,data2],ignore_index=True)
merge_data.to_csv("/mnt/d/Landsat/input_0_560.csv",index=False)