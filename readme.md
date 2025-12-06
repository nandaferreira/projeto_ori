# Sistema de Indexação e Organização da Informação

## Objetivo
O objetivo deste trabalho era implementar, em linguagem Python, um sistema completo de 
indexação e recuperação de informação que seria capaz de manipular dinamicamente uma 
coleção de documentos. O sistema teria que possibilitar a construção e atualização do vocabulário, assim como a construção da matriz TF-IDF e do índice invertido, sempre que documentos fossem inseridos ou removidos. As buscas contemplam consultas booleanas, consultas por 
similaridade e consultas por frases.
***

## Orientações sobre o sistema

- [Código fonte](./main.py)
- [Manual de uso do sistema](./GUIA_SISTEMA.txt)
- [Implementação explicada](./LEIA-ME.txt)

***

## Funcionalidades obrigatórias
 
1) Leitura dos documentos pelo arquivo ‘colecao - trabalho 01.json’. 
2) Remoção de stopwords e radicalização (bibliotecas podem ser utilizadas). 
3) Construção e atualização do vocabulário da coleção. 
4) Construção e atualização da matriz TF-IDF. 
5) Construção e atualização do índice invertido. 
6) Execução de consultas booleanas usando a matriz TF-IDF e exibição dos 
documentos que satisfazem a consulta. 
7) Consultas por similaridade de cosseno utilizando o índice invertido, com 
exibição do ranqueamento dos documentos. 
8) Buscas por frases utilizando o índice invertido, com exibição do 
ranqueamento dos documentos retornados. 
9) Apresentação dos resultados de forma organizada (vocabulário, TF-IDF, 
índice invertido e resultados das consultas). 
***

## Interações do menu
1) Adicionar um documento por vez à coleção (seguindo a ordem do JSON). 
2) Adicionar todos os documentos da lista. 
3) Remover um documento da coleção pelo seu identificador. 
4) Exibir o vocabulário atualizado. 
5) Exibir a matriz TF-IDF atual. 
6) Exibir o índice invertido completo por posição de palavras. 
7) Realizar consultas booleanas. 
8) Realizar consultas por similaridade. 
9) Realizar consultas por frase. 
10) Executar quaisquer outras operações que o grupo considerar necessárias 
para o funcionamento do sistema.
***

## Fluxo do projeto

### 1 - Pré-processamento do texto

***

### 2 - Estruturas de dados dinâmicas

***

### 3 - Menu

***

### 4 - Consultas

***

### 5 - Interface


***

## Referências

- [Como converter json e dicionários em python](https://www.index.dev/blog/convert-json-to-dictionary-python)