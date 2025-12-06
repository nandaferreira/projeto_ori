import math
from preprocessor import Preprocessor


class MotorBusca:
    """Implementa os diferentes tipos de busca"""
    
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador
        self.preprocessor = Preprocessor()
    
    # ==================== BUSCA BOOLEANA ====================
    
    def busca_booleana(self, consulta):
        """
        Executa busca booleana usando operadores AND, OR, NOT
        Utiliza a matriz TF-IDF
        
        Exemplo: "estrutura AND dados NOT linear"
        
        Retorna: lista de (doc_id, nome_doc)
        """
        # Processa a consulta
        tokens = consulta.split()
        
        if not tokens:
            return []
        
        # Processa primeiro token
        resultado = self._processar_token_booleano(tokens[0])
        
        # Processa tokens subsequentes
        i = 1
        while i < len(tokens):
            operador = tokens[i].upper()
            
            if operador not in ['AND', 'OR', 'NOT']:
                i += 1
                continue
            
            if i + 1 >= len(tokens):
                break
            
            proximo_termo = tokens[i + 1]
            proximo_resultado = self._processar_token_booleano(proximo_termo)
            
            if operador == 'AND':
                resultado = resultado.intersection(proximo_resultado)
            elif operador == 'OR':
                resultado = resultado.union(proximo_resultado)
            elif operador == 'NOT':
                resultado = resultado - proximo_resultado
            
            i += 2
        
        # Retorna documentos encontrados
        docs_encontrados = []
        for doc_id in sorted(resultado):
            if doc_id in self.gerenciador.documentos:
                docs_encontrados.append((doc_id, self.gerenciador.documentos[doc_id]["name"]))
        
        return docs_encontrados
    
    def _processar_token_booleano(self, termo):
        """Processa um termo e retorna o conjunto de documentos que o contêm"""
        # Processa o termo
        termo_processado = self.preprocessor.processar_documento(termo)
        
        if not termo_processado:
            return set()
        
        termo = termo_processado[0]
        
        # Busca no índice invertido
        if termo in self.gerenciador.indice_invertido:
            return set(self.gerenciador.indice_invertido[termo].keys())
        
        return set()
    
    # ==================== BUSCA POR SIMILARIDADE (COSSENO) ====================
    
    def busca_similaridade_cosseno(self, consulta, top_k=None):
        """
        Executa busca por similaridade de cosseno
        Calcula a similaridade entre o vetor de consulta e os documentos
        
        Args:
            consulta: string da consulta
            top_k: número de resultados a retornar (None = todos)
        
        Retorna: lista de (doc_id, nome_doc, similaridade) ordenada por score
        """
        # Processa a consulta
        palavras_consulta = self.preprocessor.processar_documento(consulta)
        
        if not palavras_consulta:
            return []
        
        # Calcula vetor TF-IDF da consulta
        vetor_consulta = self._calcular_vetor_consulta(palavras_consulta)
        
        # Se vetor_consulta está vazio, usa busca por ocorrência simples
        if not vetor_consulta:
            return self._busca_por_ocorrencia_palavras(palavras_consulta, top_k)
        
        # Calcula similaridade com cada documento
        similaridades = []
        
        for doc_id in self.gerenciador.documentos:
            vetor_doc = self.gerenciador.matriz_tfidf.get(doc_id, {})
            
            # Calcula similaridade de cosseno
            similaridade = self._similaridade_cosseno(vetor_consulta, vetor_doc)
            
            # Se similaridade é 0, usa contagem de termos comuns como alternativa
            if similaridade == 0:
                similaridade = self._calcular_relevancia_termos(palavras_consulta, doc_id)
            
            nome_doc = self.gerenciador.documentos[doc_id]["name"]
            similaridades.append((doc_id, nome_doc, similaridade))
        
        # Ordena por similaridade decrescente
        similaridades.sort(key=lambda x: x[2], reverse=True)
        
        # Limita aos top_k se especificado
        if top_k:
            similaridades = similaridades[:top_k]
        
        return similaridades
    
    def _calcular_vetor_consulta(self, palavras_consulta):
        """Calcula o vetor TF-IDF para a consulta"""
        vetor = {}
        
        # Calcula frequência das palavras na consulta
        freq_consulta = {}
        for palavra in palavras_consulta:
            freq_consulta[palavra] = freq_consulta.get(palavra, 0) + 1
        
        total_palavras = len(palavras_consulta)
        
        # Calcula TF-IDF para cada palavra
        for palavra, freq in freq_consulta.items():
            # TF
            tf = freq / total_palavras
            
            # IDF
            num_docs = self.gerenciador.doc_frequencias.get(palavra, 1)
            total_docs = len(self.gerenciador.documentos) if self.gerenciador.documentos else 1
            idf = math.log(total_docs / num_docs) if num_docs > 0 else 0
            
            # TF-IDF
            vetor[palavra] = tf * idf
        
        return vetor
    
    def _similaridade_cosseno(self, vetor1, vetor2):
        """Calcula a similaridade de cosseno entre dois vetores"""
        # Produto escalar
        produto = 0
        for palavra in vetor1:
            if palavra in vetor2:
                produto += vetor1[palavra] * vetor2[palavra]
        
        if produto == 0:
            return 0
        
        # Normas dos vetores
        norma1 = math.sqrt(sum(v**2 for v in vetor1.values()))
        norma2 = math.sqrt(sum(v**2 for v in vetor2.values()))
        
        if norma1 == 0 or norma2 == 0:
            return 0
        
        # Similaridade de cosseno
        return produto / (norma1 * norma2)
    
    def _calcular_relevancia_termos(self, palavras_consulta, doc_id):
        """Calcula relevância baseada em termos comuns quando TF-IDF retorna 0"""
        doc_palavras = self.gerenciador.documentos[doc_id]["palavras"]
        
        # Conta quantas palavras da consulta aparecem no documento
        termos_comuns = len([p for p in palavras_consulta if p in doc_palavras])
        
        # Normaliza por total de termos na consulta
        if len(palavras_consulta) > 0:
            return termos_comuns / len(palavras_consulta)
        return 0
    
    def _busca_por_ocorrencia_palavras(self, palavras_consulta, top_k=None):
        """Busca simples baseada em ocorrência de palavras"""
        resultados = []
        
        for doc_id in self.gerenciador.documentos:
            doc_palavras = self.gerenciador.documentos[doc_id]["palavras"]
            ocorrencias = sum(1 for p in palavras_consulta if p in doc_palavras)
            
            if ocorrencias > 0:
                nome_doc = self.gerenciador.documentos[doc_id]["name"]
                relevancia = ocorrencias / len(palavras_consulta) if palavras_consulta else 0
                resultados.append((doc_id, nome_doc, relevancia))
        
        resultados.sort(key=lambda x: x[2], reverse=True)
        
        if top_k:
            resultados = resultados[:top_k]
        
        return resultados
    
    # ==================== BUSCA POR FRASES ====================
    
    def busca_por_frases(self, frase, top_k=None):
        """
        Busca por uma frase completa usando o índice invertido
        Encontra documentos onde as palavras aparecem consecutivamente
        
        Args:
            frase: string da frase a buscar
            top_k: número de resultados a retornar
        
        Retorna: lista de (doc_id, nome_doc, score) ordenada por relevância
        """
        # Processa a frase
        palavras_frase = self.preprocessor.processar_documento(frase)
        
        if not palavras_frase:
            return []
        
        if len(palavras_frase) == 1:
            # Se é uma única palavra, busca como termo simples
            return self._busca_palavra_simples(palavras_frase[0], top_k)
        
        # Busca por múltiplas palavras consecutivas
        resultados = []
        
        # Encontra documentos que contêm todas as palavras
        docs_candidatos = self._encontrar_docs_com_todas_palavras(palavras_frase)
        
        # Para cada documento candidato, verifica se a frase aparece
        for doc_id in docs_candidatos:
            ocorrencias = self._encontrar_frases_no_doc(doc_id, palavras_frase)
            
            if ocorrencias:
                nome_doc = self.gerenciador.documentos[doc_id]["name"]
                score = len(ocorrencias)  # Score = número de ocorrências
                resultados.append((doc_id, nome_doc, score))
        
        # Ordena por score decrescente
        resultados.sort(key=lambda x: x[2], reverse=True)
        
        # Limita aos top_k
        if top_k:
            resultados = resultados[:top_k]
        
        return resultados
    
    def _busca_palavra_simples(self, palavra, top_k=None):
        """Busca por uma única palavra"""
        resultados = []
        
        if palavra in self.gerenciador.indice_invertido:
            docs = self.gerenciador.indice_invertido[palavra]
            
            for doc_id in docs:
                nome_doc = self.gerenciador.documentos[doc_id]["name"]
                score = len(docs[doc_id])  # Frequência da palavra
                resultados.append((doc_id, nome_doc, score))
        
        resultados.sort(key=lambda x: x[2], reverse=True)
        
        if top_k:
            resultados = resultados[:top_k]
        
        return resultados
    
    def _encontrar_docs_com_todas_palavras(self, palavras):
        """Encontra documentos que contêm todas as palavras"""
        # Começa com documentos da primeira palavra
        if palavras[0] not in self.gerenciador.indice_invertido:
            return set()
        
        docs = set(self.gerenciador.indice_invertido[palavras[0]].keys())
        
        # Intersecciona com documentos das demais palavras
        for palavra in palavras[1:]:
            if palavra not in self.gerenciador.indice_invertido:
                return set()
            docs = docs.intersection(self.gerenciador.indice_invertido[palavra].keys())
        
        return docs
    
    def _encontrar_frases_no_doc(self, doc_id, palavras_frase):
        """
        Encontra ocorrências de uma frase em um documento
        Retorna a lista de posições onde a frase começa
        """
        # Obtém as posições de cada palavra no documento
        posicoes_por_palavra = []
        
        for palavra in palavras_frase:
            if palavra not in self.gerenciador.indice_invertido:
                return []
            
            posicoes = self.gerenciador.indice_invertido[palavra].get(doc_id, [])
            if not posicoes:
                return []
            
            posicoes_por_palavra.append(posicoes)
        
        # Encontra posições onde as palavras aparecem consecutivamente
        ocorrencias = []
        
        for pos_primeira in posicoes_por_palavra[0]:
            # Verifica se as demais palavras aparecem consecutivamente
            encontrada = True
            
            for i, palavra_pos in enumerate(posicoes_por_palavra[1:], 1):
                posicao_esperada = pos_primeira + i
                
                if posicao_esperada not in palavra_pos:
                    encontrada = False
                    break
            
            if encontrada:
                ocorrencias.append(pos_primeira)
        
        return ocorrencias
