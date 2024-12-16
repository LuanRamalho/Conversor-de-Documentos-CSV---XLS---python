import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os

def selecionar_arquivo():
    caminho_arquivo = filedialog.askopenfilename(title="Selecione um arquivo")
    if caminho_arquivo:
        arquivo_selecionado.set(caminho_arquivo)  # Atualiza a variável StringVar
        # Atualiza o label para mostrar o nome do arquivo (opcional, para melhor UX)
        nome_arquivo = os.path.basename(caminho_arquivo)
        label_nome_arquivo.config(text=f"Arquivo: {nome_arquivo}")

def converter_arquivo():
    caminho_entrada = arquivo_selecionado.get()
    tipo_entrada_selecionado = tipo_entrada.get()
    tipo_saida_selecionado = tipo_saida.get()

    if not caminho_entrada:
        messagebox.showerror("Erro", "Selecione um arquivo primeiro.")
        return

    if tipo_entrada_selecionado == tipo_saida_selecionado:
        messagebox.showerror("Erro", "Os tipos de entrada e saída devem ser diferentes.")
        return

    try:
        if tipo_entrada_selecionado == "CSV" and tipo_saida_selecionado == "XLS":
            df = pd.read_csv(caminho_entrada)
            novo_caminho = os.path.splitext(caminho_entrada)[0] + ".xlsx"
            df.to_excel(novo_caminho, index=False)
        elif (tipo_entrada_selecionado == "XLS" or tipo_entrada_selecionado == "XLSX") and tipo_saida_selecionado == "CSV":
            df = pd.read_excel(caminho_entrada)
            novo_caminho = os.path.splitext(caminho_entrada)[0] + ".csv"
            df.to_csv(novo_caminho, index=False)
        else:
            messagebox.showerror("Erro", "Conversão não suportada.")
            return
        messagebox.showinfo("Sucesso", "Conversão concluída com sucesso!")

    except FileNotFoundError:
        messagebox.showerror("Erro", "Arquivo não encontrado.")
    except pd.errors.ParserError: # tratamento de erro para arquivo CSV mal formatado
        messagebox.showerror("Erro", "Erro ao ler o arquivo. Verifique o formato.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

janela = tk.Tk()
janela.title("Conversor de arquivos")
janela.config(bg="#6EFFEC")

# Variável para armazenar o caminho do arquivo
arquivo_selecionado = tk.StringVar()

# Labels
tipo_entrada_label = tk.Label(janela, text="Tipo de Entrada:", font=("Arial",12), bg="#6EFFEC")
tipo_entrada_label.grid(row=0, column=0, padx=5, pady=5) # adicionando espaçamento
tipo_saida_label = tk.Label(janela, text="Tipo de Saída:", font=("Arial",12), bg="#6EFFEC")
tipo_saida_label.grid(row=1, column=0, padx=5, pady=5)
label_nome_arquivo = tk.Label(janela, text="Arquivo: Nenhum selecionado", font=("Arial",12), bg="#6EFFEC") # label para mostrar o nome do arquivo
label_nome_arquivo.grid(row=3, column=0, columnspan=2, padx=5, pady=5) #span nas duas colunas


# Comboboxes
tipo_entrada = ttk.Combobox(janela, values=["CSV", "XLS"], state="readonly", font=("Arial",12)) #state readonly para o usuário não digitar
tipo_entrada.current(0) #define CSV como default
tipo_entrada.grid(row=0, column=1, padx=5, pady=5)
tipo_saida = ttk.Combobox(janela, values=["XLS", "CSV"], state="readonly", font=("Arial",12))
tipo_saida.current(0) #define XLS como default
tipo_saida.grid(row=1, column=1, padx=5, pady=5)


# Botões
botao_selecionar = tk.Button(janela, text="Selecionar Arquivo", command=selecionar_arquivo, font=("Arial",12,"bold"), bg="#002859", fg="#FFFFFF")
botao_selecionar.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
botao_converter = tk.Button(janela, text="Converter", command=converter_arquivo, font=("Arial",12,"bold"), bg="#145400", fg="#FFFFFF")
botao_converter.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Espaçamento entre os elementos
for widget in janela.winfo_children(): #adiciona padding em todos os widgets
    widget.grid_configure(padx=5, pady=5)

janela.mainloop()