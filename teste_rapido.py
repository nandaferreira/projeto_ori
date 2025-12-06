#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script de teste do sistema de indexação"""

# Ana Alice Cordeiro - 12211BCC028;
# Bruno Castro - 12211BCC004;
# Ester Freitas - 12211BCC036;
# Fernanda Ferreira - 12211BCC043;
# João Vitor Feijó - 12311BCC061

from gerenciador import GerenciadorColecao
from search_engine import MotorBusca

def teste_completo():
    """Executa um teste completo do sistema"""
    
    print("="*60)
    print("TESTE COMPLETO DO SISTEMA DE INDEXAÇÃO")
    print("="*60)
    
    # Inicializa
    gerenciador = GerenciadorColecao()
    docs = gerenciador.carregar_json("colecao - trabalho 01.json")
    
    # Adiciona 5 documentos
    print("\n1. Adicionando 5 documentos...")
    for i in range(min(5, len(docs))):
        doc = docs[i]
        gerenciador.adicionar_documento(i, doc["name"], doc["content"])
        print(f"   ✓ {doc['name']} adicionado")
    
    print(f"\n   Total docs: {len(gerenciador.documentos)}")
    print(f"   Total palavras: {len(gerenciador.vocabulario)}")
    
    # Testa índice
    print("\n2. Testando índice invertido...")
    indice = gerenciador.obter_indice_invertido_formatado()
    print(f"   Palavras no índice: {len(indice)}")
    print(f"   Primeiras 5: {list(indice.keys())[:5]}")
    
    # Testa TF-IDF
    print("\n3. Testando matriz TF-IDF...")
    dados, vocab = gerenciador.obter_matriz_tfidf_tabular()
    print(f"   Dimensões: {len(dados)}x{len(vocab)}")
    print(f"   Exemplo de valores: {list(dados[0].items())[:3]}")
    
    # Testa busca booleana
    motor = MotorBusca(gerenciador)
    print("\n4. Testando busca booleana...")
    resultado = motor.busca_booleana("estrutura AND dados")
    print(f"   Consulta: 'estrutura AND dados'")
    print(f"   Resultados: {len(resultado)} documentos")
    for doc_id, nome in resultado:
        print(f"   - {nome}")
    
    # Testa busca por similaridade
    print("\n5. Testando busca por similaridade...")
    resultado_sim = motor.busca_similaridade_cosseno("estrutura de dados", top_k=3)
    print(f"   Consulta: 'estrutura de dados'")
    print(f"   Top 3 resultados:")
    for doc_id, nome, score in resultado_sim:
        print(f"   - {nome}: {score:.4f}")
    
    # Testa busca por frases
    print("\n6. Testando busca por frases...")
    resultado_frase = motor.busca_por_frases("lista encadeada simples", top_k=3)
    print(f"   Consulta: 'lista encadeada simples'")
    print(f"   Resultados:")
    for doc_id, nome, ocorrencias in resultado_frase:
        print(f"   - {nome}: {ocorrencias} ocorrência(s)")
    
    # Estatísticas
    print("\n7. Estatísticas finais...")
    stats = gerenciador.obter_estatisticas()
    print(f"   Total de documentos: {stats['total_documentos']}")
    print(f"   Total de palavras únicas: {stats['total_palavras_unicas']}")
    print(f"   Total de palavras: {stats['total_palavras']}")
    print(f"   Média por documento: {stats['media_palavras_por_doc']:.2f}")
    
    print("\n✓ Teste concluído com sucesso!")

if __name__ == "__main__":
    teste_completo()
