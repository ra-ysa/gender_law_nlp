library(tjsp)
library(jsonlite)
library(stringr)
library(qdapRegex)

# creates json file corresponding to a table 
# a partir de uma tabela, cria o arquivo json correspondente
create_json <- function(table, name){
  json_table <- toJSON(table, pretty=TRUE)
  filename = paste(getwd(), name, ".json", sep="")
  jsg_file <- file(filename)
  write(json_table,jsg_file)
  close(jsg_file)
}

# standardizes string for legal process number as used in tjsp
# padroniza string do numero de processo para o formato usado no tjsp 
# NNNNNNN-DD.AAAA.J.TR.OOOO (https://tjsp.jus.br/Download/GeraisIntranet/Implanta%C3%A7%C3%A3o_Res65.pdf)
tjspify_nproc <- function(n_proc){
  n_proc_char <- strsplit(n_proc, split = "")
  n <- paste(n_proc_char[[1]][1:7], collapse="")
  d <- paste(n_proc_char[[1]][8:9], collapse="")
  a <- paste(n_proc_char[[1]][10:13], collapse="")
  j <- paste(n_proc_char[[1]][14], collapse="")
  t <- paste(n_proc_char[[1]][15:16], collapse="")
  o <- paste(n_proc_char[[1]][17:20], collapse="")
  
  n_proc_final <- paste(n, "-", d, ".", a, ".", j, ".", t, ".", o, sep="")
  return(n_proc_final)
}

# opposite of function above, cleans legal process number getting rid of punctuation marks
# faz o oposto da funcao anterior, limpando o numero do processo de pontuacoes 
simplify_nproc <- function(n_proc){
  n_proc <- gsub(".", "", n_proc, fixed=TRUE)
  n_proc_final <- gsub("-", "", n_proc)
  return(n_proc_final)
}

# locally, pdf files are named as YYYY-MM-DD_NNNNNNNNNNNNNNNNNNN
# (in which YYYY-MM-DD is the decision date and N(...) = n_proc (process number))
# generates filename (no extension) from n_proc and date
# localmente, nome dos arquivos pdf segue formato AAAA-MM-DD_NNNNNNNNNNNNNNNNNNNN 
# (em que AAAA-MM-DD eh a data do julgamento e N(...) = n_proc)
# gera nome de arquivo (sem extensao) a partir do n_proc e da data
generate_filename <- function(n_proc, data){
  clean_n_proc <- simplify_nproc(n_proc)
  filename <- paste(data, "_", clean_n_proc, sep="")
  return(filename)
}

# extracts process cd (code) from the url of a decision
# (if there are duplicated numbers, duplicated cds are a possibility)
# a partir da url de um acordao, extrai o cd do processo correspondente
# (se ha duplicacao de numeros de processo, pode haver duplicacao dos cds)
extract_cd_proc <- function(url){
  cd_processo <- ex_between(url, "cdProcesso=", "&")[[1]]
  
  # if one wants to avoid using qdapRegex, use this instead
  # (assumes cd_processo has 13 characters)
  # caso se queira evitar usar o qdapRegex, usar o codigo abaixo
  # (assume que cd_processo tem 13 caracteres)
  #pos <- str_locate(url, "cdProcesso=")
  #start_cd <- pos[2] + 1
  #stop_cd <- start_cd + 12
  #cd_processo <- substr(url, start_cd, stop_cd)
  
  return(cd_processo)
}

# extracts decision/document cd (code) from its url
# (duplicates are not expected since each decision is unique)
# a partir da url de um acordao, extrai o cd dele
# (nao deve haver duplicidade pois cada acordao eh unico)
extract_cd_doc <- function(url){
  cd_documento <- ex_between(url, "cdDocumento=", "&")[[1]]
  
  # if one wants to avoid using qdapRegex, use this instead
  # (assumes cd_documento has 8 characters)
  # caso se queira evitar usar o qdapRegex, usar o codigo abaixo
  # (assume que cd_documento tem 8 caracteres)
  # pos <- str_locate(url, "cdDocumento=")
  # start_cd <- pos[2] + 1
  # stop_cd <- start_cd + 7
  # cd_documento <- substr(url, start_cd, stop_cd)
  
  return(cd_documento)
}

# extracts decision/document id from its url
# (duplicates are not expected since each decision is unique)
# a partir da url de um acordao, extrai o id dele
# (id = cd-XXX-X)
# (nao deve haver duplicidade pois cada acordao eh unico)
extract_id_doc <- function(url){
  id_documento <- ex_between(url, "idDocumento=", "&")[[1]]
    
  # if one wants to avoid using qdapRegex, use this instead
  # (assumes id_documento has 14 characters)
  # caso se queira evitar usar o qdapRegex, usar o codigo abaixo
  # (assume que id_documento tem 14 caracteres)
  # pos <- str_locate(url, "idDocumento=")
  # start_id <- pos[2] + 1
  # stop_id <- start_id + 13
  # id_documento <- substr(url, start_id, stop_id)
    
  return(id_documento)
}

lista_processos <- read.delim2(paste(getwd(), "/lista_processos.txt", sep=""), header=FALSE, sep="\n")
lista_processos <- unlist(lista_processos)
length(lista_processos)

start_time <- Sys.time()
# downloads htmls
# baixa htmls
baixar_cposg(processos=lista_processos, diretorio=getwd())
end_time <- Sys.time()
print(paste("Running time for htmls download / Tempo total de execucao (download arquivos html): ", end_time - start_time, " min"))
# reads data from htmls
# le dados dos htmls
arquivos_html <- list.files(path = getwd(), pattern = ".html")
dados_cposg <- tjsp_ler_dados_cposg(arquivos=arquivos_html)
# creates json
# cria json
create_json(dados_cposg, "dados_cposg")
# deletes html files
# deleta arquivos html
junk <- dir(path=getwd(),  pattern=".html") 
file.remove(junk) 

start_time <- Sys.time()
# downloads decisions
# baixa acordaos
table <- tjsp_baixar_acordaos_cposg(processos=lista_processos, diretorio=getwd())
end_time <- Sys.time()
print(paste("Running time for decisions downloads / Tempo total de execucao (download acordaos): ", end_time - start_time, " min"))
# creates json
# cria json 
create_json(table, "dados_acordaos")

# dealing with json files
# lidando com os json
cposg <- fromJSON(txt="dados_cposg.json", simplifyDataFrame=TRUE)
acordaos <- fromJSON(txt="dados_acordaos.json", simplifyDataFrame=TRUE)

# adds fields cd_processo, cd_documento and id_documento in the decisions dataframe
# acrescenta os campos cd_processo, cd_documento e id_documento no dataframe acordaos
cd_processo_acordaos <- sapply(acordaos$url, extract_cd_proc)
acordaos$cd_processo <- cd_processo_acordaos 
cd_documento_acordaos <- sapply(acordaos$url, extract_cd_doc)
acordaos$cd_documento <- cd_documento_acordaos 
id_documento_acordaos <- sapply(acordaos$url, extract_id_doc)
acordaos$id_documento <- id_documento_acordaos 

# standardizes numbers
# padroniza numeraçao
cposg["processo"] <- sapply(cposg$processo, tjspify_nproc)

### Concatenate ###
### Concatenacao ###

# checking for duplicates
# verificacao de duplicacoes
acordaos$cd_processo[duplicated(acordaos$cd_processo)]
cposg$cd_processo[duplicated(cposg$cd_processo)]

acordaos$processo[duplicated(acordaos$processo)]
cposg$processo[duplicated(cposg$processo)]

# cd_processo has fewer duplicates
# therefore we use it as a common identifier
# cd_processo tem menos duplicacoes
# logo, usamos como identificador em comum 

length(unique(acordaos$cd_processo)) 
nrow(acordaos)
n_occur_acordaos <- data.frame(table(acordaos$cd_processo))
View(n_occur_acordaos[n_occur_acordaos$Freq != 1, ])

length(unique(cposg$cd_processo)) 
nrow(cposg)
n_occur_cposg <- data.frame(table(cposg$cd_processo))
View(n_occur_cposg[n_occur_cposg$Freq != 1, ])

# the only duplicate in cposg does not exist in the decisions
# therefore we join decisions and cposg
# a unica duplicacao em cposg nao existe em acordaos
# entao, fazemos o join entre acordaos e cposg com acordaos
full <- merge(x = cposg, y = acordaos, by = "cd_processo", all.acordaos = TRUE, all.cposg = FALSE)
View(full)
length(unique(full$cd_processo)) 
nrow(full)
n_occur_full <- data.frame(table(full$cd_processo))
View(n_occur_full[n_occur_full$Freq != 1, ])

# if n_occur_acordaos == n_occur_full, then join works
# se n_occur_acordaos == n_occur_full, join deu certo 
all.equal(n_occur_acordaos, n_occur_full)

# if processo.x == processo.y, we can delete one of the columns
# se processo.x == processo.y, podemos excluir uma das colunas 
all.equal(full$processo.x, full$processo.y)
full$processo.y <- NULL 
colnames(full)[which(names(full) == "processo.x")] <- "processo"

# checks if all cd_processo duplicates refer to the same process
# checa se todos os cd_processo duplicados se referem a um mesmo processo 
cd_mult <- as.character(n_occur_acordaos[n_occur_acordaos$Freq != 1, ]$Var1)
full_mult_cd <- full[is.element(full$cd_processo, cd_mult), c("processo", "cd_processo")]
full_mult_cd_unique <- unique(full_mult_cd)
# if there are duplicates in cd_processo, there are processes with different numbers for the same cd
# otherwise we can say that equal cd -> equal process
# (the opposite is not true, since cd is more restrictive than process)
# se houver duplicacoes em cd_processo, ha processos com numeros diferentes para um mesmo cd
# caso contrario, podemos afirmar que cd igual -> processo igual 
# (o contrario nao eh verdadeiro, pois cd eh mais restritivo que processo)
nrow(full_mult_cd_unique$cd_processo[duplicated(full_mult_cd_unique$cd_processo)])

# checks for equal processes with different cd_processo
# checa se ha processos iguais com cd_processo diferente
n_occur_proc <- data.frame(table(full$processo))
proc_mult <- as.character(n_occur_proc[n_occur_proc$Freq != 1, ]$Var1)
full_mult_proc <- full[is.element(full$processo, proc_mult), c("processo", "cd_processo")]
full_mult_proc_unique <- unique(full_mult_proc)
nrow(full_mult_proc_unique$processo[duplicated(full_mult_proc_unique$processo)])

# corrects column name for grammar
# corrige nome da coluna
# data_jugalmento -> data_julgamento 
colnames(full)[which(names(full) == "data_jugalmento")] <- "data_julgamento"

# checks if there are processes with same number and date
# verifica se ha processos com numero e data iguais
full_mult_datas <- full[is.element(full$processo, proc_mult), c("processo", "data_julgamento")]
all.equal(full_mult_datas, unique(full_mult_datas)) # if true, they are all unique / se true, todos sao unicos
# adds column with local filename
# acrescenta coluna com nome do arquivo local
filenames <- mapply(generate_filename, full$processo, full$data_julgamento)
full["nome_arquivo"] <- filenames

create_json(full, "dados_processos_full")
