import re 
import PyPDF2 # https://pythonhosted.org/PyPDF2/PageObject.html
import os 

def clean_text(text):
	'''
	Cleans text

	Limpa texto 
	'''

	# leaves letters, spaces and basic punctuation marks only 
	# basic punctuation marks = "legal" periods, hyphens, commas, semicolons, exclamation points and question marks
	# manages ellipsis
	# remove tudo o que nao eh letra, espaco e pontuacao basica
	# pontuacao basica = pontos finais "legais", hifens, virgulas, ponto-e-virgulas, exclamacoes e interrogacoes
	# trata reticencias
	text = re.sub(r'(\.\.\.)', '!ELLIPSIS! ', text)
	# standards that define legal periods:
	# padroes que definem um ponto final legal:
	# .AA
	text = re.sub(r'(\.)(?=[A-ZÁÀÃÄÂÉÈẼËÊÍÌĨÏÓÒÕÖÔÚÙŨÜÇŸ][A-ZÁÀÃÄÂÉÈẼËÊÍÌĨÏÓÒÕÖÔÚÙŨÜÇŸ])', '!PERIOD! ', text)
	# .Aa 
	text = re.sub(r'(\.)(?=[A-ZÁÀÃÄÂÉÈẼËÊÍÌĨÏÓÒÕÖÔÚÙŨÜÇŸ][a-záàãäâéèẽëêíìĩïóòõöôúùũüçÿ])', '!PERIOD! ', text)
	#. A
	text = re.sub(r'(\. )(?=[A-ZÁÀÃÄÂÉÈẼËÊÍÌĨÏÓÒÕÖÔÚÙŨÜÇŸ])', '!PERIOD! ', text)
	text = text.replace('!ELLIPSIS!', '...')
	
	text = re.sub(r'[^A-Za-z0-9 \?!,;\-ÁÀÃÄÂÉÈẼËÊÍÌĨÏÓÒÕÖÔÚÙŨÜÇŸáàãäâéèẽëêíìĩïóòõöôúùũüçÿ]+', '', text)
	text = text.replace('!PERIOD!', '.')
	
	# removes new lines
	# remove quebras de linha
	text = re.sub(r'\n', '', text)
	# replaces process code for the tag '[CODE]', then removes it
	# troca codigo de processo pela tag '[CODE]' e a remove
	text = re.sub(r'RI[A-Z0-9]{11}', '[CODE]', text)
	text = text.replace('[CODE]', '')
	# splits patterns (...)1A and (...)1a
	# separa palavras que sairam juntas no padrao (...)1A ou (...)1a
	text = re.sub(r'(?<=[0-9])(?=[A-ZÁÀÃÄÂÉÈẼËÊÍÌĨÏÓÒÕÖÔÚÙŨÜÇŸ])', ' ', text)
	text = re.sub(r'(?<=[0-9])(?=[a-záàãäâéèẽëêíìĩïóòõöôúùũüçÿ])', ' ', text)
	# replaces numbers for the tag '[NUMBER]'
	# troca numeros pela tag '[NUMBER]'
	text = re.sub(r'(\d+)', '[NUMBER]', text) 
	# splits patterns (...)ABb and (...)aB
	# separa palavras que sairam juntas no padrao (...)ABb ou (...)aB
	text = re.sub(r'(?<=[a-záàãäâéèẽëêíìĩïóòõöôúùũüçÿ])(?=[A-ZÁÀÃÄÂÉÈẼËÊÍÌĨÏÓÒÕÖÔÚÙŨÜÇŸ])', ' ', text)
	text = re.sub(r'(?<=[A-ZÁÀÃÄÂÉÈẼËÊÍÌĨÏÓÒÕÖÔÚÙŨÜÇŸ])(?=[A-ZÁÀÃÄÂÉÈẼËÊÍÌĨÏÓÒÕÖÔÚÙŨÜÇŸ][a-záàãäâéèẽëêíìĩïóòõöôúùũüçÿ])', ' ', text)
	# splits JUDICIARIOTRIBUNAL
	# separa a expressao JUDICIARIOTRIBUNAL
	text = re.sub(r'JUDICI(A|Á)RIOTRIBUNAL', 'JUDICIÁRIO TRIBUNAL', text)
	# splits JUSTICAPODER
	# separa a expressao JUSTICAPODER
	text = re.sub(r'JUSTI(Ç|C)APODER', 'JUSTIÇA PODER', text)
	# splits NOMERELATOR(A)
	# separa a expressao NOMERELATOR(A)
	text = re.sub(r'(?<=[A-ZÁÀÃÄÂÉÈẼËÊÍÌĨÏÓÒÕÖÔÚÙŨÜÇŸ])(?=(RELATORA|RELATOR))', ' ', text)
	# splits PALAVRAACORDAM
	# separa a expressao PALAVRAACORDAM
	text = re.sub(r'(?<=[A-ZÁÀÃÄÂÉÈẼËÊÍÌĨÏÓÒÕÖÔÚÙŨÜÇŸ])(?=ACORDAM)', ' ', text)
	# splits PALAVRANUMBER
	# separa a expressao PALAVRANUMBER
	text = re.sub(r'(?<=[A-ZÁÀÃÄÂÉÈẼËÊÍÌĨÏÓÒÕÖÔÚÙŨÜÇŸ])(?=\[NUMBER\])', ' ', text)
	# removes the tag '[NUMBER]'
	# remove a tag '[NUMBER]'
	text = text.replace('[NUMBER]', '')
	# removes some common headers 
	# remove cabecalhos comuns
	text = re.sub(r'Poder Judici(á|a)rio Tribunal de Justi(ç|c)a do Estado de S(ã|a)o Paulo', '', text)
	text = re.sub(r'PODER JUDICI(Á|A)RIO TRIBUNAL DE JUSTI(Ç|C)A DO ESTADO DE S(Ã|A)O PAULO', '', text)
	text = re.sub(r'Tribunal de Justi(ç|a)a Poder Judici(á|a)rio S((ã|a)o Paulo|(Ã|A)O PAULO)', '', text)
	text = re.sub(r'TRIBUNAL DE JUSTI(Ç|C)A PODER JUDICI(Á|A)RIO S((ã|a)o Paulo|(Ã|A)O PAULO)', '', text)
	# removes 'fl' and 'fls'
	# remove 'fl' e 'fls'
	text = re.sub(r'(\bfl(s*)\b)', '', text)
	# removes extra spaces
	# remove espacos extras
	text = re.sub(r' +', ' ', text)
	# removes signature
	# remove assinatura
	text = re.sub(r'(Assinatura( |)Eletr(ô|o)nica|ASSINATURA( |)ELETR(Ô|O)NICA)', '', text)
	text = re.sub(r'(\bEste documento é cópia do original, assinado digitalmente por.*?autos em (à|a)s\b)', '', text)
	text = re.sub(r'(\bPara conferir o original.*?informe o processo\b)', '', text)
	
	return text


def text_extractor(path):

	directory = os.fsencode(path)

	for file in os.listdir(directory):
		filename = os.fsdecode(file)
		text_full = '' 
		if filename.endswith(".pdf"):		
			pdf_file = open(filename, "rb")
			pdf_reader = PyPDF2.PdfFileReader(pdf_file, strict=False)

			for page in pdf_reader.pages:
				text_page = page.extractText() 
				text_full = text_full + text_page + ' '

			text = clean_text(text_full)
			text_filename = filename[:len(filename)-4] + ".txt" # replaces .pdf extension for .txt / substitui extensao .pdf por .txt
			textfile = open(path + text_filename, "a+")
			textfile.write(text)
			textfile.close()

path = os.path.abspath(os.getcwd()) + "/"
text_extractor(path)