import pandas as pd 

def strips(df):
	'''
	Strips every cell of a dataframe

	Limpa espacos extras de todas as celulas de um dataframe
	'''
	for column in df:
		if(df[column].dtypes == 'object' or 
			df[column].dtypes == 'str'):
			df[column] = df[column].str.strip()

def lower_case(df):
	'''
	Lower cases every character of a dataframe

	Converte todos os caracteres de um dataframe para caixa baixa
	'''
	for column in df:
		if(df[column].dtypes == 'object' or 
			df[column].dtypes == 'str'):
			df[column] = df[column].str.lower() 

def delatinize(df):
	'''
	Replaces latin diacritics and other special characters of a dataframe for plain ones

	Substitui diacriticos latinos e outros caracteres especiais de um dataframe por caracteres simples
	'''
	for column in df:
		if(df[column].dtypes == 'object' or 
			df[column].dtypes == 'str'):
			# probably more elegant with regex but i dont feel like doing it
			df[column] = df[column].str.replace("à", "a") 
			df[column] = df[column].str.replace("á", "a")
			df[column] = df[column].str.replace("ã", "a")
			df[column] = df[column].str.replace("â", "a")
			df[column] = df[column].str.replace("ä", "a")
			df[column] = df[column].str.replace("è", "e")
			df[column] = df[column].str.replace("é", "e")
			df[column] = df[column].str.replace("ẽ", "e")
			df[column] = df[column].str.replace("ê", "e")
			df[column] = df[column].str.replace("ë", "e")
			df[column] = df[column].str.replace("ì", "i")
			df[column] = df[column].str.replace("í", "i")
			df[column] = df[column].str.replace("ï", "i")
			df[column] = df[column].str.replace("ò", "o") 
			df[column] = df[column].str.replace("ó", "o")
			df[column] = df[column].str.replace("õ", "o")
			df[column] = df[column].str.replace("ô", "o")
			df[column] = df[column].str.replace("ö", "o")
			df[column] = df[column].str.replace("ù", "u")
			df[column] = df[column].str.replace("ú", "u")
			df[column] = df[column].str.replace("ũ", "u")
			df[column] = df[column].str.replace("ü", "u")
			df[column] = df[column].str.replace("ñ", "n")
			df[column] = df[column].str.replace("ç", "c")
			df[column] = df[column].str.replace("ª", "")
			df[column] = df[column].str.replace("º", "")
			df[column] = df[column].str.replace("(", "")
			df[column] = df[column].str.replace(")", "")

def no_spaces(df):
	'''
	Replaces dataframe string spaces for underscores 

	Substitui espacos em strings de um dataframe por underscores 
	'''
	for column in df:
		if(df[column].dtypes == 'object' or 
			df[column].dtypes == 'str'):
			df[column] = df[column].str.replace(" ", "_")  



def separate(df):
	'''
	Sets ; as standard intracell separation character in a dataframe

	Define ; como caracter de separacao intracelula em um dataframe
	'''
	for column in df:
		if(df[column].dtypes == 'object' or 
			df[column].dtypes == 'str'):
			df[column] = df[column].str.replace("/", "; ")


tjmg1 = pd.read_csv("tjmg1_viol.csv")
tjmg2 = pd.read_csv("tjmg2_viol.csv")
tjrj = pd.read_csv("tjrj_viol.csv")
tjsp1 = pd.read_csv("tjsp1_viol.csv")
tjsp2 = pd.read_csv("tjsp2_viol.csv")

df_list = [tjmg1, tjmg2, tjrj, tjsp1, tjsp2]

for item in df_list:
	# deletes column with original keys
	# deleta coluna com chaves originais
	item.drop(["Unnamed: 0"], axis=1, inplace=True)

	# stripping everything 
	# limpando espacos extras 
	strips(item)

	# lower casing everything
	# convertendo caracteres para caixa baixa
	lower_case(item)

	# replacing special characters
	# substituindo caracteres especiais
	delatinize(item)

	# replacing spaces for underscores
	# substituindo espacos por underscores 
	no_spaces(item)

	# sets ; as separation character for cells with more than one value
	# define ; como caracter de separacao em celulas com mais de um valor  
	separate(item)

	# adds new columns for bias annotation
	# adiciona novas colunas para anotacao de vies 
	item['vies'] = pd.Series(dtype='str')
	item['vies_alvo'] = pd.Series(dtype='str')

	# sorts by decision date
	# ordena por data do julgamento
	item.sort_values('data_julgamento', inplace=True, ignore_index=True)

tjmg1.to_csv("tjmg1_annotate.csv", escapechar=";")
tjmg2.to_csv("tjmg2_annotate.csv", escapechar=";")
tjrj.to_csv("tjrj_annotate.csv", escapechar=";")
tjsp1.to_csv("tjsp1_annotate.csv", escapechar=";")
tjsp2.to_csv("tjsp2_annotate.csv", escapechar=";")
