'''
Extracts list of processes in .txt from the .xlxs file provided 

Extrai lista de processos em .txt a partir do arquivo .xlxs 
'''

def gen_txt_list(table, court):
	'''
	From a table that has a column with process code numbers, generates a .txt file with its content

	A partir de uma tabela que tenha uma coluna com numeros de processo, gera um arquivo .txt com o conteudo 
	'''
	codes = [] # keeps process code numbers / guarda codigos dos processos
	for item in table["processo"]:
		codes.append(item.strip())

	filename = "lista_" + court + ".txt"
	with open(filename, "w") as f:
		for item in codes:
			f.write("%s\n" % item)


import pandas as pd 
table = pd.ExcelFile("ap_dados_sudeste.xlsx")

# parses sheets
# le abas 
sheet_tjmg1 = table.parse(0)
sheet_tjmg2 = table.parse(1)
sheet_tjrj = table.parse(2)
sheet_tjsp1 = table.parse(3)
sheet_tjsp2 = table.parse(4)

# ------------------------------------------------------- #

# rename columns
# renomeia colunas

cn_tjmg1 = list(sheet_tjmg1.columns)
cn_tjmg2 = list(sheet_tjmg2.columns)
cn_tjrj = list(sheet_tjrj.columns)
cn_tjsp1 = list(sheet_tjsp1.columns)
cn_tjsp2 = list(sheet_tjsp2.columns)

cn_tjmg1_new = ["processo", "mag", "data_julgamento", "inteiro_teor", "assunto", 
		       "alegou_ap", "acusado_ap", "viol_mulher", "viol_menor",
			   "acusado_viol", "resultado_viol", "prova_viol",
			   "resultado_ap", "prova_ap"]
cn_tjsp1_new = ["processo", "mag", "vara", "data_julgamento", "inteiro_teor", "assunto", 
		       "alegou_ap", "acusado_ap", "viol_mulher", "viol_menor",
			   "acusado_viol", "resultado_viol", "prova_viol",
			   "resultado_ap", "prova_ap"]
cn_si_new = ["processo", "relator", "orgao_julgador", "data_julgamento", "tipo_recurso", 
			"colegialidade", "inteiro_teor", "assunto", "alegou_ap", "acusado_ap", 
			"viol_mulher", "viol_menor", "acusado_viol", "resultado_viol", "prova_viol",
			"resultado_ap", "prova_ap"] # second instance / segunda instancia 

dict_tjmg1 = {cn_tjmg1[0]: cn_tjmg1_new[0], cn_tjmg1[1]: cn_tjmg1_new[1], cn_tjmg1[2]: cn_tjmg1_new[2],
				  cn_tjmg1[3]: cn_tjmg1_new[3], cn_tjmg1[4]: cn_tjmg1_new[4], cn_tjmg1[5]: cn_tjmg1_new[5],
				  cn_tjmg1[6]: cn_tjmg1_new[6], cn_tjmg1[7]: cn_tjmg1_new[7], cn_tjmg1[8]: cn_tjmg1_new[8],
				  cn_tjmg1[9]: cn_tjmg1_new[9], cn_tjmg1[10]: cn_tjmg1_new[10], cn_tjmg1[11]: cn_tjmg1_new[11],
				  cn_tjmg1[12]: cn_tjmg1_new[12], cn_tjmg1[13]: cn_tjmg1_new[13]}
dict_tjmg2 = {cn_tjmg2[0]: cn_si_new[0], cn_tjmg2[1]: cn_si_new[1], cn_tjmg2[2]: cn_si_new[2],
				  cn_tjmg2[3]: cn_si_new[3], cn_tjmg2[4]: cn_si_new[4], cn_tjmg2[5]: cn_si_new[5],
				  cn_tjmg2[6]: cn_si_new[6], cn_tjmg2[7]: cn_si_new[7], cn_tjmg2[8]: cn_si_new[8],
				  cn_tjmg2[9]: cn_si_new[9], cn_tjmg2[10]: cn_si_new[10], cn_tjmg2[11]: cn_si_new[11],
				  cn_tjmg2[12]: cn_si_new[12], cn_tjmg2[13]: cn_si_new[13], cn_tjmg2[14]: cn_si_new[14], 
				  cn_tjmg2[15]: cn_si_new[15], cn_tjmg2[16]: cn_si_new[16]}
dict_tjrj = {cn_tjrj[0]: cn_si_new[0], cn_tjrj[1]: cn_si_new[1], cn_tjrj[2]: cn_si_new[2],
				  cn_tjrj[3]: cn_si_new[3], cn_tjrj[4]: cn_si_new[4], cn_tjrj[5]: cn_si_new[5],
				  cn_tjrj[6]: cn_si_new[6], cn_tjrj[7]: cn_si_new[7], cn_tjrj[8]: cn_si_new[8],
				  cn_tjrj[9]: cn_si_new[9], cn_tjrj[10]: cn_si_new[10], cn_tjrj[11]: cn_si_new[11],
				  cn_tjrj[12]: cn_si_new[12], cn_tjrj[13]: cn_si_new[13], cn_tjrj[14]: cn_si_new[14], 
				  cn_tjrj[15]: cn_si_new[15], cn_tjrj[16]: cn_si_new[16]}
dict_tjsp1 = {cn_tjsp1[0]: cn_tjsp1_new[0], cn_tjsp1[1]: cn_tjsp1_new[1], cn_tjsp1[2]: cn_tjsp1_new[2],
				  cn_tjsp1[3]: cn_tjsp1_new[3], cn_tjsp1[4]: cn_tjsp1_new[4], cn_tjsp1[5]: cn_tjsp1_new[5], 
				  cn_tjsp1[6]: cn_tjsp1_new[6], cn_tjsp1[7]: cn_tjsp1_new[7], cn_tjsp1[8]: cn_tjsp1_new[8], 
				  cn_tjsp1[9]: cn_tjsp1_new[9], cn_tjsp1[10]: cn_tjsp1_new[10], cn_tjsp1[11]: cn_tjsp1_new[11], 
				  cn_tjsp1[12]: cn_tjsp1_new[12], cn_tjsp1[13]: cn_tjsp1_new[13], cn_tjsp1[14]: cn_tjsp1_new[14]}
dict_tjsp2 = {cn_tjsp2[0]: cn_si_new[0], cn_tjsp2[1]: cn_si_new[1], cn_tjsp2[2]: cn_si_new[2],
				  cn_tjsp2[3]: cn_si_new[3], cn_tjsp2[4]: cn_si_new[4], cn_tjsp2[5]: cn_si_new[5],
				  cn_tjsp2[6]: cn_si_new[6], cn_tjsp2[7]: cn_si_new[7], cn_tjsp2[8]: cn_si_new[8],
				  cn_tjsp2[9]: cn_si_new[9], cn_tjsp2[10]: cn_si_new[10], cn_tjsp2[11]: cn_si_new[11],
				  cn_tjsp2[12]: cn_si_new[12], cn_tjsp2[13]: cn_si_new[13], cn_tjsp2[14]: cn_si_new[14], 
				  cn_tjsp2[15]: cn_si_new[15], cn_tjsp2[16]: cn_si_new[16]}

sheet_tjmg1.rename(mapper=dict_tjmg1, axis=1, inplace=True)
sheet_tjmg2.rename(mapper=dict_tjmg2, axis=1, inplace=True)
sheet_tjrj.rename(mapper=dict_tjrj, axis=1, inplace=True)
sheet_tjsp1.rename(mapper=dict_tjsp1, axis=1, inplace=True)
sheet_tjsp2.rename(mapper=dict_tjsp2, axis=1, inplace=True)

# ------------------------------------------------------- #

# selects cases with claims of sexual violence against minor
# seleciona casos em que consta acusacao de abuso sexual contra menor

tjmg1_viol = sheet_tjmg1.loc[sheet_tjmg1['viol_menor'].str.contains('sexual', na=False)]
tjmg2_viol = sheet_tjmg2.loc[sheet_tjmg2['viol_menor'].str.contains('sexual', na=False)]
tjrj_viol = sheet_tjrj.loc[sheet_tjrj['viol_menor'].str.contains('sexual', na=False)]
tjsp1_viol = sheet_tjsp1.loc[sheet_tjsp1['viol_menor'].str.contains('sexual', na=False)]
tjsp2_viol = sheet_tjsp2.loc[sheet_tjsp2['viol_menor'].str.contains('sexual', na=False)]

gen_txt_list(tjmg1_viol, "tjmg1")
gen_txt_list(tjmg2_viol, "tjmg2")
gen_txt_list(tjrj_viol, "tjrj")
gen_txt_list(tjsp1_viol, "tjsp1")
gen_txt_list(tjsp2_viol, "tjsp2")

tjmg1_viol.to_csv("tjmg1_viol.csv")
tjmg2_viol.to_csv("tjmg2_viol.csv")
tjrj_viol.to_csv("tjrj_viol.csv")
tjsp1_viol.to_csv("tjsp1_viol.csv")
tjsp2_viol.to_csv("tjsp2_viol.csv")
