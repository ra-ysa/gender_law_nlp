import pandas as pd 
table = pd.read_excel("processos com status.xlsx")

'''
Extracts list of processes in .txt from the .xlxs file provided 

Extrai lista de processos em .txt a partir do arquivo .xlxs 
'''


codes = [] # keeps process code numbers / guarda codigos dos processos
for item in table["processo"]:
	codes.append(item)

with open("lista_processos.txt", "w") as f:
	for item in codes:
		f.write("%s\n" % item)