import mysql.connector
import pandas as pd

def gerar_relatorio_excel():
    conexao = None  
    cursor = None

    try:
        # Conexão com o MySQL
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="20873594",
            database="estoque_pecas"
        )

        cursor = conexao.cursor()

        # Consulta correta — SEM GROUP BY no SELECT principal
        query = """
            SELECT 
                p.id_peca,
                g.nome_grupo AS grupo,
                p.codigo,
                p.descricao,
                p.local,
                p.estoque_atual,
                f.nome_fornecedor AS ultimo_fornecedor
            FROM pecas p
            LEFT JOIN grupos g 
                ON p.id_grupo = g.id_grupo
            LEFT JOIN (
                SELECT 
                    mov.id_peca,
                    mov.id_fornecedor
                FROM movimentacoes mov
                INNER JOIN (
                    SELECT id_peca, MAX(data_movimentacao) AS ultima_data
                    FROM movimentacoes
                    GROUP BY id_peca
                ) ult
                    ON mov.id_peca = ult.id_peca
                    AND mov.data_movimentacao = ult.ultima_data
            ) ult_mov 
                ON p.id_peca = ult_mov.id_peca
            LEFT JOIN fornecedores f 
                ON ult_mov.id_fornecedor = f.id_fornecedor;
        """

        cursor.execute(query)
        dados = cursor.fetchall()

        colunas = [
            "ID Peça", "Grupo", "Código", "Descrição",
            "Local", "Estoque Atual", "Último Fornecedor"
        ]

        df = pd.DataFrame(dados, columns=colunas)

        df.to_excel("relatorio_estoque.xlsx", index=False)

        print("Relatório gerado com sucesso! (relatorio_estoque.xlsx)")

    except mysql.connector.Error as erro:
        print("Erro ao gerar relatório:", erro)

    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()

# Executar função
gerar_relatorio_excel()
