import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ------------------------------------------------------
#   CONEXÃO COM O BANCO DE DADOS
# ------------------------------------------------------
def conectar():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",       # coloque sua senha aqui
            database="estoque_pecas"
        )
        return conexao
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco:\n{e}")
        return None


# ------------------------------------------------------
#   FUNÇÃO PARA SALVAR NO BANCO
# ------------------------------------------------------
def salvar_dados():
    data = data_entry.get()
    grupo = grupo_entry.get()
    codigo = codigo_entry.get()
    descricao = descricao_entry.get()
    movimentacao = mov_entry.get()
    local = local_entry.get()
    quantidade = qtde_entry.get()
    fornecedor = fornecedor_entry.get()

    if not data or not codigo or not quantidade:
        messagebox.showwarning("Atenção", "Os campos Data, Código e Quantidade são obrigatórios!")
        return

    conexao = conectar()
    if not conexao:
        return

    cursor = conexao.cursor()

    try:
        sql = """
        INSERT INTO pecas 
        (data_movimentacao, grupo, codigo, descricao, movimentacao, local, quantidade, fornecedor)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        valores = (data, grupo, codigo, descricao, movimentacao, local, quantidade, fornecedor)
        cursor.execute(sql, valores)
        conexao.commit()

        messagebox.showinfo("Sucesso", "Registro inserido com sucesso!")

        # limpar inputs
        data_entry.delete(0, tk.END)
        grupo_entry.delete(0, tk.END)
        codigo_entry.delete(0, tk.END)
        descricao_entry.delete(0, tk.END)
        mov_entry.delete(0, tk.END)
        local_entry.delete(0, tk.END)
        qtde_entry.delete(0, tk.END)
        fornecedor_entry.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao inserir dados:\n{e}")

    finally:
        cursor.close()
        conexao.close()


# ------------------------------------------------------
#   INTERFACE (TKINTER)
# ------------------------------------------------------
root = tk.Tk()
root.title("Estoque de Peças")
root.geometry("900x500")
root.configure(bg="#8c8c8c")

font_label = ("Arial", 12, "bold")
font_entry = ("Arial", 12)

titulo = tk.Label(root, text="ESTOQUE DE PEÇAS", font=("Arial", 20, "bold"), bg="#8c8c8c")
titulo.pack(pady=20)

frame = tk.Frame(root, bg="#8c8c8c")
frame.pack()

# COLUNA ESQUERDA
tk.Label(frame, text="Data da movimentação", bg="#8c8c8c", font=font_label).grid(row=0, column=0, sticky="w", padx=20)
data_entry = ttk.Entry(frame, width=30)
data_entry.grid(row=1, column=0, padx=20, pady=5)

tk.Label(frame, text="Grupo", bg="#8c8c8c", font=font_label).grid(row=2, column=0, sticky="w", padx=20)
grupo_entry = ttk.Entry(frame, width=30)
grupo_entry.grid(row=3, column=0, padx=20, pady=5)

tk.Label(frame, text="Código", bg="#8c8c8c", font=font_label).grid(row=4, column=0, sticky="w", padx=20)
codigo_entry = ttk.Entry(frame, width=30)
codigo_entry.grid(row=5, column=0, padx=20, pady=5)

tk.Label(frame, text="Descrição", bg="#8c8c8c", font=font_label).grid(row=6, column=0, sticky="w", padx=20)
descricao_entry = ttk.Entry(frame, width=30)
descricao_entry.grid(row=7, column=0, padx=20, pady=5)

# COLUNA DIREITA
tk.Label(frame, text="Movimentação", bg="#8c8c8c", font=font_label).grid(row=0, column=1, sticky="w", padx=20)
mov_entry = ttk.Entry(frame, width=30)
mov_entry.grid(row=1, column=1, padx=20, pady=5)

tk.Label(frame, text="Local", bg="#8c8c8c", font=font_label).grid(row=2, column=1, sticky="w", padx=20)
local_entry = ttk.Entry(frame, width=30)
local_entry.grid(row=3, column=1, padx=20, pady=5)

tk.Label(frame, text="Quantidade", bg="#8c8c8c", font=font_label).grid(row=4, column=1, sticky="w", padx=20)
qtde_entry = ttk.Entry(frame, width=30)
qtde_entry.grid(row=5, column=1, padx=20, pady=5)

tk.Label(frame, text="Fornecedor", bg="#8c8c8c", font=font_label).grid(row=6, column=1, sticky="w", padx=20)
fornecedor_entry = ttk.Entry(frame, width=30)
fornecedor_entry.grid(row=7, column=1, padx=20, pady=5)

# BOTÃO SALVAR
btn = tk.Button(root, text="Salvar", font=("Arial", 14, "bold"), command=salvar_dados)
btn.pack(pady=20)

root.mainloop()
