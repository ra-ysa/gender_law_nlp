import pandas as pd 
import random 
import os 
random.seed(10)

def annotate_select(df):
	'''
	Random selection of 0.1 from the dataframe to be annotated

	Sorteio de 0.1 do dataframe para anotacao
	'''

	# print(df.info())
	# checks which column has only unique values (therefore being suitable as a key attribute)
	# checa quais colunas tem apenas valores unicos (sendo portanto adequadas como atributo-chave)
	for column in list(df):
		if (df[column].nunique() == df.shape[0]):
			key = column 

	annotate_subset = random.sample(df[key].tolist(), k=int(0.1*df.shape[0]))
	annotate_subset.sort()
	return key, annotate_subset 

path = os.path.abspath(os.getcwd()) + "/"
df = pd.read_json(path + 'dados_processos_full.json')
key, annotate_subset = annotate_select(df)
#print(annotate_subset)

# Now we create a .csv file and a dataframe with annotations for annotate_subset
# Agora criamos um arquivo .csv e um dataframe com as anotacoes para annotate_subset
attributes = [key,
			'apelante',
			'apelante_genero',
			'apelado',
			'crime',
			'vitima',
			'vitima_genero',
			'pena_original',
			'requer',
			'requer_subsid',
			'requer_motivo',
			'mp_pj',
			'resultado',
			'resultado_razoes',
			'pena_atual',
			'vies',
			'vies_alvo']
annotated_df = pd.DataFrame(columns=attributes)
annotated_df[key] = annotate_subset 
annotated_df.to_csv('annotate.csv')
# After manually filling and renaming the .csv file, we complete the dataframe
# Apos preencher manualmente e renomear o arquivo .csv, completamos o dataframe
annotated_df = pd.read_csv('annotate_filled.csv')
#print(annotated_df.head(20))




