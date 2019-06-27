# TCC_News_Crawler


## Fatores que influenciam a cotação dólar

No geral, o que determina a cotação do dólar é a oferta e demanda da moeda dentro do Brasil. 
Logo, se há muita oferta o preço cai, já se há muita demanda o preço sobe.
Sabendo disso, é preciso entender quais são os fatores que afetam a oferta e a demanda. 
Esses são três fatores principais apontados pela matéria do G1:

- Exportação e Importação. Déficit faz com que o dólar suba, superávit com que desça.
- Gastos de turistas brasileiros no exterior faz com que o dólar suba, gastos de turistas estrangeiros no Brasil com que desça.
- Alta dos juros americanos faz com que o dólar suba, alta dos juros brasileiros com que desça.

Nessas matérias da BBC e do G1 é possível encontrar informações mais detalhadas e podemos nos guiar por elas:
https://www.bbc.com/portuguese/geral-48288923
https://g1.globo.com/economia/educacao-financeira/noticia/veja-o-que-faz-o-dolar-subir-ou-cair-em-relacao-ao-real.ghtml

## Descrição do crawler

O intuito da pesquisa é encontrar uma relação de causa entre as notícias sobre o governo e a variação do dólar. Logo,
com esse objetivo em vista e a partir dos fatores que influenciam a cotação do dólar em relação ao real,
determinamos os seguintes parâmetros de busca:

- Palavra para filtrar a busca: "governo bolsonaro"
- Intervalo de datas: do 01/07/2018(início do período eleitoral) até 27/07/2019
- Seção de Editoriais
- Categorias dos Editoriais: "Poder", "Mercado" e "Mundo"

Uma vez feita a busca das notícias é feito um processamento das mesmas, limpando e formatando.

- Substitui o espaço em branco ISO 8859-1 por um espaço UTF-8.
- Remove os pulos de linha("/r/n" e "/n")
- Removes os espaços em branco extras
- Converte para letra minúscula
- Substitui aspas simples por aspas duplas, evitando que o NLTK pense que citações são palavras em inglês.
- Se a notícia não possuir um autor estabelece o valor: "NO AUTHOR"
