from gerenciador import GerenciadorColecao
from search_engine import MotorBusca
import json

# Ana Alice Cordeiro - 12211BCC028;
# Bruno Castro - 12211BCC004;
# Ester Freitas - 12211BCC036;
# Fernanda Ferreira - 12211BCC043;
# João Vitor Feijó - 12311BCC061

class MenuPrincipal:
    def __init__(self):
        self.gerenciador = GerenciadorColecao()
        self.motor_busca = MotorBusca(self.gerenciador)
        self.documentos_json = []
        self.indice_atual = -1
    
    def carregar_colecao(self):
        self.documentos_json = self.gerenciador.carregar_json("colecao - trabalho 01.json")
        if not self.documentos_json:
            print("Nenhum documento foi carregado!")
            return False
        print(f"✓ {len(self.documentos_json)} documentos carregados do JSON")
        return True
    
    def exibir_menu_principal(self):
        while True:
            print("\n" + "="*60)
            print("         Sistema de Indexação e Recuperação de Documentos")
            print("="*60)
            print(f"Status: {len(self.gerenciador.documentos)} documentos na coleção")
            print("-"*60)
            print("1.  Adicionar um documento")
            print("2.  Adicionar todos os documentos")
            print("3.  Remover um documento")
            print("4.  Listar documentos da coleção")
            print("5.  Exibir vocabulário")
            print("6.  Exibir matriz TF-IDF")
            print("7.  Exibir índice invertido")
            print("8.  Realizar busca booleana")
            print("9.  Realizar busca por similaridade (cosseno)")
            print("10. Realizar busca por frases")
            print("11. Exibir estatísticas")
            print("0.  Sair")
            print("-"*60)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "1":
                self.adicionar_um_documento()
            elif opcao == "2":
                self.adicionar_todos_documentos()
            elif opcao == "3":
                self.remover_documento()
            elif opcao == "4":
                self.listar_documentos()
            elif opcao == "5":
                self.exibir_vocabulario()
            elif opcao == "6":
                self.exibir_matriz_tfidf()
            elif opcao == "7":
                self.exibir_indice_invertido()
            elif opcao == "8":
                self.busca_booleana()
            elif opcao == "9":
                self.busca_similaridade()
            elif opcao == "10":
                self.busca_frases()
            elif opcao == "11":
                self.exibir_estatisticas()
            elif opcao == "0":
                print("\nEncerrando o sistema...")
                break
            else:
                print("❌ Opção inválida!")
    
    def adicionar_um_documento(self):
        #adiciona o proximo documento
        if self.indice_atual + 1 >= len(self.documentos_json):
            print("❌ Todos os documentos já foram adicionados!")
            return
        
        self.indice_atual += 1
        doc = self.documentos_json[self.indice_atual]
        
        self.gerenciador.adicionar_documento(
            doc_id=self.indice_atual,
            nome=doc["name"],
            conteudo=doc["content"]
        )
        
        print(f"✓ Documento {doc['name']} adicionado com sucesso!")
        print(f"  Progresso: {self.indice_atual + 1}/{len(self.documentos_json)}")
    
    def adicionar_todos_documentos(self):
        confirmacao = input("Adicionar todos os documentos? (s/n): ").strip().lower()
        if confirmacao != 's':
            return
        
        quantidade_adicionada = 0
        while self.indice_atual + 1 < len(self.documentos_json):
            self.adicionar_um_documento()
            quantidade_adicionada += 1
        
        print(f"✓ {quantidade_adicionada} documentos adicionados com sucesso!")
    
    def remover_documento(self):
        docs = self.gerenciador.listar_documentos()
        if not docs:
            print("Nenhum documento na coleção!")
            return
        
        print("\nDocumentos disponíveis:")
        for doc in docs:
            print(f"  ID: {doc['id']:2d} | Nome: {doc['name']:5s} | Palavras: {doc['palavras']}")
        
        try:
            doc_id = int(input("\nDigite o ID do documento a remover: ").strip())
            self.gerenciador.remover_documento(doc_id)
            self.indice_atual -= 1 if doc_id <= self.indice_atual else 0
        except ValueError:
            print("ID inválido!")
    
    def listar_documentos(self):
        docs = self.gerenciador.listar_documentos()
        
        if not docs:
            print("Nenhum documento na coleção!")
            return
        
        print("\n" + "="*60)
        print("DOCUMENTOS NA COLEÇÃO")
        print("="*60)
        print(f"{'ID':>3} | {'Nome':>10} | {'Palavras':>12} | {'Documento'}")
        print("-"*60)
        
        for doc in docs:
            nome = doc['name']
            conteudo = self.gerenciador.documentos[doc['id']]['content'][:40]
            print(f"{doc['id']:>3} | {nome:>10} | {doc['palavras']:>12} | {conteudo}...")
    
    def exibir_vocabulario(self):
        vocab = self.gerenciador.obter_vocabulario_ordenado()
        
        if not vocab:
            print("Vocabulário vazio!")
            return
        
        print("\n" + "="*60)
        print("VOCABULÁRIO DA COLEÇÃO")
        print("="*60)
        print(f"Total de palavras únicas: {len(vocab)}\n")
        
        #pra exibir em colunas
        cols = 4
        for i in range(0, len(vocab), cols):
            linha = vocab[i:i+cols]
            print("  |  ".join(f"{p:20s}" for p in linha))
    
    def exibir_matriz_tfidf(self):
        #matrixz idf
        if not self.gerenciador.documentos:
            print("Nenhum documento na coleção!")
            return
        
        dados, vocab = self.gerenciador.obter_matriz_tfidf_tabular()
        
        print("\n" + "="*80)
        print("MATRIZ TF-IDF")
        print("="*80)
        print(f"Documentos: {len(dados)} | Palavras: {len(vocab)}\n")
        
        palavras_exibir = vocab[:10]
        
        print(f"{'Documento':<12}", end="")
        for palavra in palavras_exibir:
            print(f"{palavra:>12}", end="")
        if len(vocab) > 10:
            print(f"{'...':<12}", end="")
        print()
        print("-" * (12 + 12 * len(palavras_exibir) + (12 if len(vocab) > 10 else 0)))
        
        for doc_id in sorted(dados.keys()):
            print(f"D{doc_id:<10}", end="")
            for palavra in palavras_exibir:
                valor = dados[doc_id][palavra]
                print(f"{valor:>12.4f}", end="")
            if len(vocab) > 10:
                print(f"{'...':<12}", end="")
            print()
        
        if len(vocab) > 10:
            print(f"\n[Mostrando primeiras {len(palavras_exibir)} de {len(vocab)} palavras]")
    
    def exibir_indice_invertido(self):
        #indice invertido
        indice = self.gerenciador.obter_indice_invertido_formatado()
        
        if not indice:
            print("Índice invertido vazio!")
            return
        
        print("\n" + "="*60)
        print("ÍNDICE INVERTIDO")
        print("="*60)
        print(f"Total de palavras: {len(indice)}\n")
        
        limite = min(20, len(indice))
        palavras = list(indice.keys())[:limite]
        
        for palavra in palavras:
            docs = indice[palavra]
            docs_info = []
            for doc_id in sorted(docs.keys()):
                posicoes = docs[doc_id]
                docs_info.append(f"D{doc_id}:{posicoes}")
            
            print(f"{palavra:>15} → {', '.join(docs_info)}")
        
        if len(indice) > limite:
            print(f"\n[Mostrando {limite} de {len(indice)} palavras. Use uma palavra específica para detalhes]")
    
    def busca_booleana(self):
        print("\n" + "="*60)
        print("BUSCA BOOLEANA")
        print("="*60)
        print("Operadores: AND, OR, NOT")
        print("Exemplo: 'estrutura AND dados NOT linear'")
        
        consulta = input("\nDigite a consulta: ").strip()
        if not consulta:
            return
        
        resultados = self.motor_busca.busca_booleana(consulta)
        
        print(f"\n{'RESULTADOS':^60}")
        print("-"*60)
        
        if not resultados:
            print("Nenhum resultado encontrado!")
        else:
            print(f"✓ {len(resultados)} documento(s) encontrado(s):\n")
            for i, (doc_id, nome) in enumerate(resultados, 1):
                conteudo = self.gerenciador.documentos[doc_id]['content'][:60]
                print(f"{i}. [{nome}]")
                print(f"   {conteudo}...")
    
    def busca_similaridade(self):
        print("\n" + "="*60)
        print("BUSCA POR SIMILARIDADE (COSSENO)")
        print("="*60)
        print("Digite termos de busca. Os documentos mais similares serão retornados.")
        
        consulta = input("\nDigite a consulta: ").strip()
        if not consulta:
            return
        
        try:
            top_k = input("Quantos resultados? (Enter para todos): ").strip()
            top_k = int(top_k) if top_k else None
        except ValueError:
            top_k = None
        
        resultados = self.motor_busca.busca_similaridade_cosseno(consulta, top_k)
        
        print(f"\n{'RESULTADOS':^60}")
        print("-"*60)
        
        if not resultados:
            print("Nenhum resultado encontrado!")
        else:
            print(f"✓ {len(resultados)} documento(s) encontrado(s):\n")
            print(f"{'Rank':<5} {'Nome':<10} {'Similaridade':<15} {'Conteúdo'}")
            print("-"*60)
            
            for i, (doc_id, nome, score) in enumerate(resultados, 1):
                conteudo = self.gerenciador.documentos[doc_id]['content'][:30]
                print(f"{i:<5} {nome:<10} {score:<15.4f} {conteudo}...")
    
    def busca_frases(self):
        """Realiza uma busca por frases"""
        print("\n" + "="*60)
        print("BUSCA POR FRASES")
        print("="*60)
        print("Digite uma frase para buscar.")
        
        consulta = input("\nDigite a frase: ").strip()
        if not consulta:
            return
        
        try:
            top_k = input("Quantos resultados? (Enter para todos): ").strip()
            top_k = int(top_k) if top_k else None
        except ValueError:
            top_k = None
        
        resultados = self.motor_busca.busca_por_frases(consulta, top_k)
        
        print(f"\n{'RESULTADOS':^60}")
        print("-"*60)
        
        if not resultados:
            print("Nenhum resultado encontrado!")
        else:
            print(f"✓ {len(resultados)} documento(s) encontrado(s):\n")
            print(f"{'Rank':<5} {'Nome':<10} {'Ocorrências':<15} {'Conteúdo'}")
            print("-"*60)
            
            for i, (doc_id, nome, score) in enumerate(resultados, 1):
                conteudo = self.gerenciador.documentos[doc_id]['content'][:30]
                print(f"{i:<5} {nome:<10} {score:<15d} {conteudo}...")
    
    def exibir_estatisticas(self):
        stats = self.gerenciador.obter_estatisticas()
        
        print("\n" + "="*60)
        print("ESTATÍSTICAS DA COLEÇÃO")
        print("="*60)
        print(f"Total de documentos:      {stats['total_documentos']}")
        print(f"Total de palavras únicas: {stats['total_palavras_unicas']}")
        print(f"Total de palavras:        {stats['total_palavras']}")
        print(f"Média de palavras/doc:    {stats['media_palavras_por_doc']:.2f}")
    
    def executar(self):
        print("\n" + "="*60)
        print("    CARREGANDO SISTEMA DE INDEXAÇÃO...")
        print("="*60)
        
        if not self.carregar_colecao():
            return
        
        self.exibir_menu_principal()


if __name__ == "__main__":
    menu = MenuPrincipal()
    menu.executar()
