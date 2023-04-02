import wn
import numpy as np
import random
import nltk

# To avoid an issue with the server, change the default download path
wn.config.data_directory = "wn-data/"
wn.download('own-pt')

nltk.data.path = ['nltk_data/']
nltk.download('stopwords', download_dir='nltk_data/')
PT_STOPWORDS = nltk.corpus.stopwords.words('portuguese')

# dict of synonyms for bias-related words
BIAS_SYN_DICT = {"agressão": ["ofensa"],
			"agressiva": ["belicosa"],
			"agressividade": ["brutalidade"],
			"agressivo": ["belicoso"],
			"agressões": ["ofensas"],
			"algoz": ["carrasco"],
			"ardilosa": ["maliciosa"],
			"ardiloso": ["malicioso"],
			"beligerância": ["combatividade"],
			"bom juízo": ["apreciação"],
			"caráter": ["índole"],
			"comportamento": ["temperamento"],
			"condição": ["circunstância"],
			"conduta": ["ação"],
			"confusa": ["obscura"],
			"confuso": ["obscuro"],
			"conturbada": ["caótica"],
			"conturbado": ["caótico"],
			"convencer": ["persuadir"],
			"convincente": ["persuasivo"],
			"convincentes": ["persuasivos"],
			"deformação": ["deformidade"],
			"desajustada": ["deslocada"],
			"desajustado": ["deslocado"],
			"desentendimento": ["briga"],
			"desentendimentos": ["brigas"],
			"desfavorecida": ["indefesa"],
			"desfavorecido": ["indefeso"],
			"desvio": ["falha"],
			"deturpada": ["viciada"],
			"deturpado": ["viciado"],
			"deveria": ["precisaria"],
			"deveriam": ["precisariam"],
			"egoísmo": ["egocentrismo"],
			"egoísta": ["egotista"],
			"estabilidade": ["firmeza"],
			"estranha": ["esquisita"],
			"estranhas": ["esquisitas"],
			"estranho": ["esquisito"],
			"estranhos": ["esquisitos"],
			"evidentemente": ["claramente"],
			"explosão": ["estouro"],
			"explosões": ["estouros"],
			"falsa": ["fingida"],
			"falsas": ["fingidas"],
			"falso": ["fingido"],
			"falsos": ["fingidos"],
			"família": ["comunidade"],
			"familiar": ["parente"],
			"familiares": ["parentes"],
			"feminina": ["feminil"],
			"figura materna": ["cuidadora"],
			"figura paterna": ["cuidador"],
			"frágil": ["delicado"],
			"fragilidade": ["debilidade"],
			"hipossuficiência": ["vulnerabilidade"],
			"hipossuficiente": ["vulnerável"],
			"idônea": ["íntegra"],
			"idoneidade": ["integridade"],
			"idôneo": ["íntegro"],
			"inconvincente": ["suspeito"],
			"inconvincentes": ["suspeitos"],
			"individualismo": ["egoísmo"],
			"individualista": ["egoísta"],
			"inferior": ["menor"],
			"inferioridade": ["desvantagem"],
			"insuspeita": ["honesta"],
			"insuspeito": ["honesto"],
			"isolada": ["sozinha"],
			"isolado": ["sozinho"],
			"ladainha": ["papo"],
			"maldade": ["crueldade"],
			"medo": ["pavor"],
			"mútua": ["recíproca"],
			"mútuas": ["recíprocas"],
			"mútuo": ["recíproco"],
			"mútuos": ["recíprocos"],
			"normalidade": ["equilíbrio"],
			"obviamente": ["incontestavelmente"],
			"padrão": ["norma"],
			"padrões": ["normas"],
			"perfil": ["tipo"],
			"personalidade": ["individualidade"],
			"prestígio": ["importância"],
			"proteção": ["defesa"],
			"psicológico": ["emocional"],
			"recíproca": ["mútua"],
			"recíprocas": ["mútuas"],
			"reciprocidade": ["mutualidade"],
			"recíproco": ["mútuo"],
			"recíprocos": ["mútuos"],
			"reconciliação": ["harmonização"],
			"referência materna": ["provedora"],
			"referência paterna": ["provedor"],
			"reputação": ["imagem"],
			"teria": ["possuiria"],
			"teriam": ["possuiriam"],
			"tratamento": ["terapia"],
			"valor": ["princípio"],
			"valores": ["princípios"],
			"violência": ["ataque"],
			"violenta": ["descontrolada"],
			"violento": ["descontrolado"],
			"vulnerabilidade": ["hipossuficiência"],
			"vulnerável": ["hipossuficiente"]
}

def bias_synonyms(word):
    '''
    Returns a random bias-related synonym for a given word 
    '''
    
    if BIAS_SYN_DICT.get(word.lower()):
        bias_syn = random.choice(BIAS_SYN_DICT[word.lower()])
        return bias_syn
    else:
        return synonyms(word)

def synonyms(word):
	'''
    Returns a random synonym for a given word 
    '''
	syn = [] 
	word = word.lower()
	try:
		for related_words in np.random.choice(list(wn.synsets(word)), size=3):
			syn += related_words.lemmas()
			#for w in related_words.lemmas():
			#	syn.add(w)
		syn = set(syn)
		syn.remove(word) # removes the word itself
	except:
		pass

	if syn:
		return random.choice(list(syn))
	else:
		return word


def text_augmentation(texts, bias_labels):
    '''
    Performs data augmentation by changing a word for a synonym
    '''
    
    augmented_texts = []
    
    for text, bias in zip(texts, bias_labels):
        aug_text = []

        # skips stopwords
        for word in text.split():
            if word.lower() in PT_STOPWORDS:
                aug_text.append(word)
                continue

			# we flip a weighted coin to decide if the word will be changed
			# if this function takes too long, we can change the probability
            if np.random.choice([True, False], p=[0.7, 0.3]):
                if bias:
                    aug_text.append(bias_synonyms(word))
                else:
                    aug_text.append(synonyms(word))
            else:
                aug_text.append(word)

        augmented_texts.append(" ".join(aug_text))

    return augmented_texts

def main():
    '''
    Test data augmentation function
    '''
    import json
    with open('dataset/test_data_aug.json') as f:
        data = json.load(f)
	
    texts = []
    bias = []
    for item in data.values():
        for text in item['vies_contexto']:
            texts.append(text)
            bias.append(1 if item["vies"] != '' else 0)

    orig_texts = texts.copy()
	
    aug_texts = text_augmentation(texts, bias)

    for idx, text in enumerate(texts):
        if orig_texts[idx] != aug_texts[idx]:
            print(f"Original {idx}:: {text}")
            print(f"Augmented{idx}:: {aug_texts[idx]}")
            print()

if __name__ == "__main__":
    main()
