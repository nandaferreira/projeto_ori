import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer

# Ana Alice Cordeiro - 12211BCC028;
# Bruno Castro - 12211BCC004;
# Ester Freitas - 12211BCC036;
# Fernanda Ferreira - 12211BCC043;
# João Vitor Feijó - 12311BCC061

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('tokenizers/rslp')
except LookupError:
    nltk.download('rslp')


class Preprocessor:
    
    def __init__(self):
        self.stemmer = RSLPStemmer()
        self.stop_words = set(stopwords.words('portuguese'))
    
    def limpar_texto(self, texto):
        texto = texto.lower()
        texto = re.sub(r'\n+', ' ', texto)
        texto = re.sub(r'\s+', ' ', texto)
        texto = texto.strip()
        
        return texto
    
    def remover_pontuacao(self, texto):
        texto = re.sub(r'[^a-zà-úÀ-Ú\s]', '', texto)
        return texto
    
    def tokenizar(self, texto):
        texto = self.remover_pontuacao(texto)
        palavras = texto.split()
        return palavras
    
    def remover_stopwords(self, palavras):
        return [p for p in palavras if p and p not in self.stop_words]
    
    def radicalizar(self, palavras):
        return [self.stemmer.stem(p) for p in palavras]
    
    def processar_documento(self, texto):
        texto_limpo = self.limpar_texto(texto)
        palavras = self.tokenizar(texto_limpo)
        palavras = self.remover_stopwords(palavras)
        palavras = self.radicalizar(palavras)
        palavras = [p for p in palavras if p]
        
        return palavras
    
    def obter_posicoes_palavras(self, texto):
       
        texto_limpo = self.limpar_texto(texto)
        palavras = self.tokenizar(texto_limpo)
        
        posicoes = {}
        for i, palavra in enumerate(palavras):
            if palavra in self.stop_words:
                continue
          
            palavra_radical = self.stemmer.stem(palavra)
            
            if palavra_radical not in posicoes:
                posicoes[palavra_radical] = []
            posicoes[palavra_radical].append(i)
        
        return posicoes
