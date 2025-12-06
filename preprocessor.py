import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer

# Download de dados necessários
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('tokenizers/rslp')
except LookupError:
    nltk.download('rslp')


class Preprocessor:
    """Responsável pelo pré-processamento de textos"""
    
    def __init__(self):
        self.stemmer = RSLPStemmer()
        self.stop_words = set(stopwords.words('portuguese'))
    
    def limpar_texto(self, texto):
        """
        Realiza limpeza básica do texto:
        - Converte para minúsculas
        - Remove quebras de linha
        - Remove espaços múltiplos
        """
        # Converter para minúsculas
        texto = texto.lower()
        
        # Remover quebras de linha e espaços múltiplos
        texto = re.sub(r'\n+', ' ', texto)
        texto = re.sub(r'\s+', ' ', texto)
        
        # Remover espaços nas bordas
        texto = texto.strip()
        
        return texto
    
    def remover_pontuacao(self, texto):
        """Remove pontuação mantendo apenas palavras e números"""
        # Remove pontuação mas mantém hífens e apóstrofos para palavras compostas
        texto = re.sub(r'[^\w\s\-\']', ' ', texto)
        return texto
    
    def tokenizar(self, texto):
        """Divide o texto em palavras"""
        # Remove pontuação
        texto = self.remover_pontuacao(texto)
        # Divide em palavras
        palavras = texto.split()
        return palavras
    
    def remover_stopwords(self, palavras):
        """Remove palavras vazias (stopwords) da lista"""
        return [p for p in palavras if p and p not in self.stop_words]
    
    def radicalizar(self, palavras):
        """Aplica stemming (radicalização) às palavras"""
        return [self.stemmer.stem(p) for p in palavras]
    
    def processar_documento(self, texto):
        """
        Processa um documento completo:
        1. Limpeza
        2. Tokenização
        3. Remoção de stopwords
        4. Radicalização
        
        Retorna: lista de palavras processadas
        """
        # Passo 1: Limpeza
        texto_limpo = self.limpar_texto(texto)
        
        # Passo 2: Tokenização
        palavras = self.tokenizar(texto_limpo)
        
        # Passo 3: Remoção de stopwords
        palavras = self.remover_stopwords(palavras)
        
        # Passo 4: Radicalização
        palavras = self.radicalizar(palavras)
        
        # Filtrar palavras vazias
        palavras = [p for p in palavras if p]
        
        return palavras
    
    def obter_posicoes_palavras(self, texto):
        """
        Retorna as posições de cada palavra no texto original
        Útil para busca de frases
        
        Retorna: dicionário {palavra: [posições]}
        """
        # Processa mantendo posições
        texto_limpo = self.limpar_texto(texto)
        palavras = self.tokenizar(texto_limpo)
        
        posicoes = {}
        for i, palavra in enumerate(palavras):
            # Remover stopwords
            if palavra in self.stop_words:
                continue
            
            # Radicalizar
            palavra_radical = self.stemmer.stem(palavra)
            
            if palavra_radical not in posicoes:
                posicoes[palavra_radical] = []
            posicoes[palavra_radical].append(i)
        
        return posicoes
