import mysql.connector
import pandas as pd

def gerar_relatorio_excel():
    try:
        # Conexão com o MySQL
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sua_senha",
            database="estoque_pecas"
        )

        cursor = conexao.cursor()

        # Consulta do estoque completo
        query = """
            SELECT 
                pecas.id_peca,
                grupos.nome_grupo AS grupo,
                pecas.codigo,
                pecas.descricao,
                pecas.local,
                pecas.estoque_atual,
                fornecedores.nome_fornecedor
            FROM pecas
            LEFT JOIN grupos ON pecas.id_grupo = grupos.id_grupo
            LEFT JOIN movimentacoes ON pecas.id_peca = movimentacoes.id_peca
            LEFT JOIN fornecedores ON movimentacoes.id_fornecedor = fornecedores.id_fornecedor
            GROUP BY pecas.id_peca;
        """

        cursor.execute(query)
        dados = cursor.fetchall()

        colunas = [
            "ID Peça", "Grupo", "Código", "Descrição", 
            "Local", "Estoque Atual", "Último Fornecedor"
        ]

        # Convertendo para DataFrame
        df = pd.DataFrame(dados, columns=colunas)

        # Salvando em Excel
        df.to_excel("relatorio_estoque.xlsx", index=False)

        print("Relatório gerado com sucesso! (relatorio_estoque.xlsx)")

    except mysql.connector.Error as erro:
        print("Erro ao gerar relatório:", erro)

    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()

# Executar função
gerar_relatorio_excel()
