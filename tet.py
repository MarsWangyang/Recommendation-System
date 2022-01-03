import pandas as pd
import ast

path = 'Bot_Info.xlsx'
table = pd.read_excel(path, engine='openpyxl')
with open('./text.txt', 'w') as file:
    for i in table['label']:
        if str(i) != 'nan':
            label_list = eval(i)
            for content in label_list:
                file.write(content)
                file.write('\n')
