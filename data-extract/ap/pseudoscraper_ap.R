library(tjsp)
library(jsonlite)
library(stringr)
library(data.table)

# creates json file corresponding to a table 
# a partir de uma tabela, cria o arquivo json correspondente
create_json <- function(table, name){
  json_table <- toJSON(table, pretty=TRUE)
  filename = paste("/home/ray/mestrado/projeto/final/ap/", name, ".json", sep="")
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

# cleans filename by stripping date and extension, leaving process number only
# limpa nome do arquivo eliminando data e extensao, deixando so o numero do processo
clean_filename <- function(filename){
  clean_fn <- substr(filename, 12, 31)
  return(clean_fn)
}

lista_processos <- read.delim2("/home/ray/mestrado/projeto/final/ap/lista_tjsp2.txt", header=FALSE, sep="\n")
lista_processos <- unlist(lista_processos)
length(lista_processos)
u_processos <- unique(lista_processos)
length(u_processos)
n_occur_processos <- table(lista_processos)
View(n_occur_processos)

start_time <- Sys.time()
# downloads decisions
# baixa acordaos
table <- tjsp_baixar_acordaos_cposg(processos=lista_processos, diretorio="/home/ray/mestrado/projeto/final/ap")
end_time <- Sys.time()
print(paste("Running time for decisions downloads / Tempo total de execucao (download acordaos): ", end_time - start_time, " min"))
# creates json
# cria json 
create_json(table, "dados_acordaos")

# dealing with json file
# lidando com o json
acordaos <- fromJSON(txt="dados_acordaos.json", simplifyDataFrame=TRUE)
n_occur_acordaos <- data.frame(table(acordaos$processo))
View(n_occur_acordaos)
lista_acordaos <- unlist(as.vector(acordaos["processo"]))
lista_acordaos
length(lista_acordaos)
u_acordaos <- unique(lista_acordaos)
length(u_acordaos)

# list of decision files
# lista dos arquivos com acordaos
lista_arquivos <- list.files(pattern = "[0-9]+\\.pdf$")
lista_arquivos <- unlist(lapply(lista_arquivos, clean_filename))
n_occur_arquivos <- table(lista_arquivos)
View(n_occur_arquivos)
lista_arquivos
length(lista_arquivos)
u_arquivos <- unique(lista_arquivos)
length(u_arquivos)

# checks if unique process numbers in dados_acordaos.json match pdf files 
# checa se numeros de processo unicos em dados_acordaos.json correspondem aos arquivos pdf 
u_acordaos
u_arquivos
u_arquivos <- lapply(u_arquivos, tjspify_nproc)
unlist(u_arquivos)
# if true, they match
# se true, ha correspondencia
setequal(u_acordaos, u_arquivos)
# checks if every item in dados_acordaos.json is in the original lista_processos
# checa se todos os itens em dados_acordaos.json estao na lista_processos original
setequal(intersect(u_processos, u_acordaos), u_acordaos)

manual <- setdiff(u_processos, u_acordaos)
length(manual)
fwrite(list(manual), file = "lista_manual.txt")


















