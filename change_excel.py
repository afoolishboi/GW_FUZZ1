import pandas as pd

sheet = '温度系数-πT'
df = pd.read_excel(r'C:\Users\UNIS\Desktop\晶体管\大功率高频双极晶体管.xls', sheet_name=sheet)

# 假设频率在第一列，列名为 '频率(GHz)'，后面是不同输出功率
df_long = df.melt(id_vars=['T(℃)'], var_name='Vs(Vce/BVcEs)', value_name='温度系数πT')

# 保存为 CSV
df_long.to_csv(sheet + '_long.csv', index=False)