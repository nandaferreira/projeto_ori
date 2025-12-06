import json
import math
from collections import defaultdict
from preprocessor import Preprocessor

# Ana Alice Cordeiro - 12211BCC028;
# Bruno Castro - 12211BCC004;
# Ester Freitas - 12211BCC036;
# Fernanda Ferreira - 12211BCC043;
# João Vitor Feijó - 12311BCC061


class GerenciadorColecao:
    """Gerencia a coleção de documentos e suas estruturas de indexação"""
    
    def __init__(self):
        self.preprocessor = Preprocessor()
        self.documentos = {}  # {doc_id: {"name": "", "content": "", "palavras": []}}
        self.vocabulario = set()  # Conjunto de todas as palavras únicas
        self.matriz_tfidf = {}  # {doc_id: {palavra: valor_tfidf}}
        self.indice_invertido = {}  # {palavra: {doc_id: [posições]}}
        self.frequencias_doc = {}  # {doc_id: {palavra: frequência}}
        self.doc_frequencias = {}  # {palavra: número de docs com a palavra}
    
    def carregar_json(self, caminho_arquivo):
        """Carrega documentos do arquivo JSON"""
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                docs = json.load(f)
            return docs
        except Exception as e:
            print(f"Erro ao carregar JSON: {e}")
            return []
    
    def adicionar_documento(self, doc_id, nome, conteudo):
        """
        Adiciona um documento à coleção e atualiza todas as estruturas
        
        Args:
            doc_id: identificador único do documento
            nome: nome/id do documento
            conteudo: texto do documento
        """
        # Processa o documento
        palavras_processadas = self.preprocessor.processar_documento(conteudo)
        
        # Armazena informações do documento
        self.documentos[doc_id] = {
            "name": nome,
            "content": conteudo,
            "palavras": palavras_processadas
        }
        
        # Atualiza estruturas de indexação
        self._atualizar_vocabulario(doc_id, palavras_processadas)
        self._atualizar_frequencias(doc_id, palavras_processadas)
        self._atualizar_indice_invertido(doc_id, palavras_processadas)
        self._recalcular_tfidf_completo()
    
    def remover_documento(self, doc_id):
        """Remove um documento da coleção e atualiza todas as estruturas"""
        if doc_id not in self.documentos:
            print(f"Documento {doc_id} não encontrado")
            return False
        
        # Remove das estruturas
        palavras = self.documentos[doc_id]["palavras"]
        
        # Limpar índice invertido
        for palavra in set(palavras):
            if palavra in self.indice_invertido:
                if doc_id in self.indice_invertido[palavra]:
                    del self.indice_invertido[palavra][doc_id]
                
                # Se nenhum documento tem essa palavra, remove ela
                if not self.indice_invertido[palavra]:
                    del self.indice_invertido[palavra]
                    self.vocabulario.discard(palavra)
        
        # Remove do armazenamento
        del self.documentos[doc_id]
        if doc_id in self.matriz_tfidf:
            del self.matriz_tfidf[doc_id]
        if doc_id in self.frequencias_doc:
            del self.frequencias_doc[doc_id]
        
        # Recalcula TF-IDF para todos os documentos (pois IDF mudou)
        self._recalcular_tfidf_completo()
        
        print(f"Documento {doc_id} removido com sucesso")
        return True
    
    def _atualizar_vocabulario(self, doc_id, palavras_processadas):
        """Atualiza o vocabulário com as palavras do novo documento"""
        self.vocabulario.update(palavras_processadas)
    
    def _atualizar_frequencias(self, doc_id, palavras_processadas):
        """Atualiza a frequência de palavras no documento"""
        freq = defaultdict(int)
        for palavra in palavras_processadas:
            freq[palavra] += 1
        
        self.frequencias_doc[doc_id] = dict(freq)
        
        # Atualizar frequência de documentos para cada palavra (apenas palavras únicas)
        for palavra in set(palavras_processadas):
            if palavra not in self.doc_frequencias:
                self.doc_frequencias[palavra] = 0
            self.doc_frequencias[palavra] += 1
    
    def _atualizar_indice_invertido(self, doc_id, palavras_processadas):
        """Atualiza o índice invertido com as posições das palavras"""
        posicoes_por_palavra = defaultdict(list)
        
        for posicao, palavra in enumerate(palavras_processadas):
            posicoes_por_palavra[palavra].append(posicao)
        
        for palavra, posicoes in posicoes_por_palavra.items():
            if palavra not in self.indice_invertido:
                self.indice_invertido[palavra] = {}
            self.indice_invertido[palavra][doc_id] = posicoes
    
    def _atualizar_tfidf(self, doc_id):
        """Calcula e atualiza o TF-IDF para um documento"""
        self.matriz_tfidf[doc_id] = {}
        
        total_palavras = len(self.documentos[doc_id]["palavras"])
        if total_palavras == 0:
            return
        
        for palavra, freq in self.frequencias_doc[doc_id].items():
            # Calcula TF (Term Frequency)
            tf = freq / total_palavras
            
            # Calcula IDF (Inverse Document Frequency)
            num_docs_com_palavra = self.doc_frequencias.get(palavra, 1)
            total_docs = len(self.documentos)
            idf = math.log(total_docs / num_docs_com_palavra) if num_docs_com_palavra > 0 else 0
            
            # TF-IDF = TF * IDF
            tfidf = tf * idf
            self.matriz_tfidf[doc_id][palavra] = tfidf
    
    def _recalcular_tfidf_completo(self):
        """Recalcula TF-IDF para todos os documentos"""
        for doc_id in self.documentos:
            self._atualizar_tfidf(doc_id)
    
    def obter_vocabulario_ordenado(self):
        """Retorna o vocabulário ordenado alfabeticamente"""
        return sorted(list(self.vocabulario))
    
    def obter_matriz_tfidf_tabular(self):
        """Retorna a matriz TF-IDF em formato tabular para exibição"""
        vocab = self.obter_vocabulario_ordenado()
        
        dados = {}
        for doc_id in sorted(self.documentos.keys()):
            dados[doc_id] = {}
            for palavra in vocab:
                valor = self.matriz_tfidf.get(doc_id, {}).get(palavra, 0)
                dados[doc_id][palavra] = valor
        
        return dados, vocab
    
    def obter_indice_invertido_formatado(self):
        """Retorna o índice invertido formatado para exibição"""
        resultado = {}
        
        # Ordena palavras alfabeticamente
        for palavra in sorted(self.indice_invertido.keys()):
            docs = self.indice_invertido[palavra]
            resultado[palavra] = {}
            
            for doc_id in sorted(docs.keys()):
                posicoes = docs[doc_id]
                resultado[palavra][doc_id] = posicoes
        
        return resultado
    
    def obter_estatisticas(self):
        """Retorna estatísticas da coleção"""
        total_docs = len(self.documentos)
        total_palavras_unicas = len(self.vocabulario)
        total_palavras = sum(len(self.documentos[doc_id]["palavras"]) for doc_id in self.documentos)
        
        return {
            "total_documentos": total_docs,
            "total_palavras_unicas": total_palavras_unicas,
            "total_palavras": total_palavras,
            "media_palavras_por_doc": total_palavras / total_docs if total_docs > 0 else 0
        }
    
    def listar_documentos(self):
        """Lista todos os documentos na coleção"""
        docs_info = []
        for doc_id in sorted(self.documentos.keys()):
            doc = self.documentos[doc_id]
            docs_info.append({
                "id": doc_id,
                "name": doc["name"],
                "palavras": len(doc["palavras"])
            })
        return docs_info
