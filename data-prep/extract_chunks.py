import pandas as pd 
import re 
import json
import random


N_SENTENCES_INTRO = 5 # number of sentences to use for building intro chunks 
N_SENTENCES_END = 10 # number of sentences to use for building end chunks 
N_SENTENCES_RANDOM = 3 # number of sentences to use for building random chunks when not bias-related 
# domain: [1, len(sentences)]
BATCH_SIZE = 32 # number of chunks to use in test mode 

def bias_extractor(text, bias, n):
	'''
	Extracts sentences containing bias-related expressions as annotated
	Extrai sentencas que contenham expressoes relacionadas a vieses, conforme anotado

	input:  
	text (str): whole text content 
	bias (list): list of bias-related expressions / lista de expressoes relacionadas a vieses
	n: amount of sentences to include as bias context / quantidade de sentencas a incluir como contexto do vies
	
	output:
	bias_sentences (list): list of sentences containing bias-related expressions / 
						   lista de sentencas contendo expressoes relacionadas a vieses

	example:
	bias = ["quedou-se contrariada", "as lesoẽs que suportou são leves", "moderação por parte do réu", "forma isolada"]
	sentence = [<sent1>, <sent2>, ... <sentn>]
	bias_sentences = [<sent1>, <sent2>, ... <senti>], where <sent1> contains bias[0], <sent2> contains bias[1], ..., <senti> contains bias[i]
	a given bias can appear more than once in text; in that case, it will generate more than one sentence
	'''
	
	# converts text to a list of sentences / converte texto para uma lista de sentencas
	bias  = [b.replace('“',"").replace('”', "") for b in bias]  
	sentences = re.split("[?!;.\s]+\s", text)
	sentences = [s.strip() for s in sentences] 
	bias_sentences = []
	for sent_idx, sentence in enumerate(sentences):
		for b in bias:
			if b in sentence:
				idx_start = max(0, sent_idx-n)
				idx_end = min(sent_idx+n, len(sentences))
				bias_sentences.append(" ".join([sent for sent in sentences[idx_start:idx_end]]))
	return bias_sentences


def intro_extractor(text, n):
	'''
	Extracts the first n sentences from the text

	Extrai as primeiras n sentencas do texto
	'''
	sentences = re.split("[;.\s]+\s", text)
	sentences = [s.strip() for s in sentences] 
	sent_idx = 0
	intro_sentences = []
	idx_start = sent_idx
	idx_end = min(sent_idx+n, len(sentences))
	intro_sentences.append(" ".join([sent for sent in sentences[idx_start:idx_end]]))
	return intro_sentences   


def end_extractor(text, n):
	'''
	Extracts the last n sentences from the text

	Extrai as ultimas n sentencas do texto 
	'''
	sentences = re.split("[;.\s]+\s", text)
	sentences = [s.strip() for s in sentences] 
	sent_idx = len(sentences)
	end_sentences = []
	idx_start = max(0, sent_idx-n)
	idx_end = sent_idx
	end_sentences.append(" ".join([sent for sent in sentences[idx_start:idx_end]]))
	return end_sentences 


def random_extractor(text, n):
	'''
	Extracts a random sentence and its n-sized context from the text 

	Extrai uma sentenca aleatoria do texto, mais seu contexto de tamanho n 
	'''
	sentences = re.split("[;.\s]+\s", text)
	sentences = [s.strip() for s in sentences] 
	sent_idx = random.randint(0, len(sentences)) 
	random_sentences = []
	idx_start = max(0, sent_idx-n)
	idx_end = min(sent_idx+n, len(sentences))
	random_sentences.append(" ".join([sent for sent in sentences[idx_start:idx_end]]))
	return random_sentences


def full_extractor(text):
	'''
	Extracts the whole content from the text, in BATCH_SIZE chunks

	Extrai todo o conteudo do texto, em BATCH_SIZE chunks 
	'''
	sentences = re.split("[;.\s]+\s", text)
	sentences = [s.strip() for s in sentences] 

	while(len(sentences) < BATCH_SIZE):
		sentences.append(random.choice(sentences)) # we pad the sentences list by repeating random sentences 

	if(len(sentences) == BATCH_SIZE):
		return sentences
	else:
		chunk_size = len(sentences) // BATCH_SIZE 

		chunks = []
		start = 0

		for i in range(BATCH_SIZE):
			stop = start + chunk_size
			if(i==BATCH_SIZE-1): 
				stop = len(sentences)
				chunks.append(' '.join(sentences[start:stop]))
			else:
				chunks.append(' '.join(sentences[start:stop]))

			start+=chunk_size

		return chunks 


df_annotation = pd.read_csv('annotate_filled.csv')
json_annotation = {}
n_bias = 0
n_unbias = 0

for idx, row in df_annotation.iterrows():

	# Creates json item
	json_annotation[row["nome_arquivo"]] = {
				 k:v for k,v in row.items() if k!='Unnamed: 0'}

	# if cell is empty (nan), we replace it for an empty string 			 
	json_annotation[row["nome_arquivo"]].update({
				 k:"" for k,v in json_annotation[row["nome_arquivo"]].items()
				  if type(v) is float })

	filename = row["nome_arquivo"] + ".txt"
	with open(filename) as f:
		text = f.read()

	if type(row["vies"]) is float:
		# cell is empty, therefore no bias detected
		bias_chunks = []
		for n in [2, 3]:
			bias_chunks += random_extractor(text, n) 
		n_unbias += len(bias_chunks)
	else:
		bias_chunks = []
		for n in [1, 2, 3]:
			bias = row["vies"].split(";")
			bias_chunks += bias_extractor(text, bias, n)
			#print(bias_chunks)
		n_bias += len(bias_chunks)

	intro_chunks = intro_extractor(text, N_SENTENCES_INTRO)
	end_chunks = end_extractor(text, N_SENTENCES_END)
	random_chunks = []
	for i in range(10):
		# extracts 10 random chunks of size N_SENTENCES_RANDOM, for validation purposes
		random_chunks +=random_extractor(text, N_SENTENCES_RANDOM)
	all_chunks = full_extractor(text)

	# strips strings
	json_annotation[row["nome_arquivo"]].update({
		k:v.replace(" ", "") for k,v in json_annotation[row["nome_arquivo"]].items() if type(v) is str and k!='vies'}) 

	json_annotation[row["nome_arquivo"]].update({"vies_contexto":bias_chunks})
	json_annotation[row["nome_arquivo"]].update({"intro":intro_chunks})
	json_annotation[row["nome_arquivo"]].update({"end":end_chunks})
	json_annotation[row["nome_arquivo"]].update({"random":random_chunks})
	json_annotation[row["nome_arquivo"]].update({"full":all_chunks})

	json_annotation[row["nome_arquivo"]].update({
		k:v.replace('“',"").replace('”', "") for k,v in json_annotation[row["nome_arquivo"]].items() if k=='vies'})

	# stores items as a list, so that attributes can have more than one value that are presented separately
	json_annotation[row["nome_arquivo"]].update({
		k:v.split(";") for k,v in json_annotation[row["nome_arquivo"]].items() if type(v) is str and k!='nome_arquivo'})
	
	# checks amount of words in chunks
	#chunks = [bias_chunks, intro_chunks, end_chunks, random_chunks]
	#for chunk_type in chunks:  
	#	for i in chunk_type:  
	#		print(len(i.split()))

print("# of biased chunks", n_bias)
print("# of unbiased chunks", n_unbias)

with open("annotate_filled.json", "w") as f:
	json.dump(json_annotation, f)