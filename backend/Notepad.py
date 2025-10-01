import tkinter as tki
from tkinter import filedialog, messagebox, simpledialog
import os
from datetime import datetime

# Variável global para armazenar o nome do arquivo atual
arquivo_atual = None


def novo_arquivo():
    global arquivo_atual

    # Pop-up para solicitar o nome do arquivo
    nome_arquivo = simpledialog.askstring(
        "Novo Arquivo", "Digite o nome do novo arquivo:", initialvalue=""
    )

    # Verifica se o usuário forneceu um nome
    if not nome_arquivo or nome_arquivo.strip() == "":
        messagebox.showwarning(
            "Nome Obrigatório",
            "É obrigatório fornecer um nome para o arquivo!\n"
            "O novo arquivo não foi criado.",
        )
        return  # Não cria o arquivo se nome não foi fornecido

    # Remove caracteres inválidos do nome
    nome_arquivo = nome_arquivo.strip()
    caracteres_invalidos = '<>:"/\\|?*'
    for char in caracteres_invalidos:
        nome_arquivo = nome_arquivo.replace(char, "_")

    # Garante que tenha extensão .md
    if not nome_arquivo.endswith(".md"):
        nome_arquivo += ".md"

    # Limpa o texto atual
    escrever_texto.delete(1.0, "end")

    # Atualiza o arquivo atual
    arquivo_atual = nome_arquivo

    # Atualiza o título da janela
    tela.title(f"Bloco de Notas - {nome_arquivo}")

    # Mostra confirmação
    messagebox.showinfo(
        "Novo Arquivo Criado",
        f"Novo arquivo '{nome_arquivo}' criado com sucesso!\n\n"
        f"Comece a escrever e depois clique em 'Salvar'.",
    )


def mostrar_notificacao_diretorio_padrao(caminho_salvo):
    messagebox.showinfo(
        "Diretório não escolhido",
        f"Nenhum diretório foi selecionado.\n"
        f"Arquivo salvo no diretório padrão:\n\n"
        f"{caminho_salvo}",
    )


def salvar_arquivo():
    global arquivo_atual
    container = escrever_texto.get(1.0, "end")

    # Verifica se há conteúdo para salvar
    if not container.strip():
        messagebox.showwarning(
            "Conteúdo Vazio",
            "Não há conteúdo para salvar!\n" "Digite algum texto antes de salvar.",
        )
        return

    # Define o diretório padrão (pasta 'documentos' dentro do projeto)
    diretorio_documentos = os.path.join(os.path.dirname(__file__), "documentos")

    # Cria o diretório se não existir
    if not os.path.exists(diretorio_documentos):
        os.makedirs(diretorio_documentos)

    # Define o nome do arquivo
    if arquivo_atual:
        nome_arquivo = arquivo_atual
    else:
        # Se não há arquivo atual, gera nome com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"documento_{timestamp}.md"
        arquivo_atual = nome_arquivo

    # Monta o caminho completo
    caminho_completo = os.path.join(diretorio_documentos, nome_arquivo)

    # Salva o arquivo diretamente na pasta documentos
    try:
        with open(caminho_completo, "w", encoding="utf-8") as arquivo:
            arquivo.write(container)

        # Atualiza o título da janela
        tela.title(f"Bloco de Notas - {nome_arquivo}")

        # Mostra confirmação de sucesso
        messagebox.showinfo(
            "Sucesso",
            f"Arquivo salvo com sucesso!\n\n"
            f"Nome: {nome_arquivo}\n"
            f"Local: {caminho_completo}",
        )

    except Exception as e:
        messagebox.showerror(
            "Erro ao Salvar",
            f"Erro ao salvar o arquivo:\n{str(e)}\n\n" "Tente novamente.",
        )


def abrir_arquivo():
    global arquivo_atual

    arquivo_caminho = filedialog.askopenfilename(
        defaultextension=".md",
        filetypes=[
            ("Markdown files", "*.md"),
            ("Text files", "*.txt"),
            ("All files", "*.*"),
        ],
        title="Escolha um arquivo para abrir",
    )

    if arquivo_caminho:
        try:
            with open(arquivo_caminho, "r", encoding="utf-8") as arquivo:
                conteudo = arquivo.read()
                escrever_texto.delete(1.0, "end")
                escrever_texto.insert(1.0, conteudo)

            # Atualiza o arquivo atual com apenas o nome do arquivo
            arquivo_atual = os.path.basename(arquivo_caminho)

            # Atualiza o título da janela
            tela.title(f"Bloco de Notas - {arquivo_atual}")

            messagebox.showinfo(
                "Sucesso", f"Arquivo '{arquivo_atual}' aberto com sucesso!"
            )

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir o arquivo:\n{str(e)}")
            arquivo_atual = None
            tela.title("Bloco de Notas")


tela = tki.Tk()
tela.title("Bloco de Notas")
tela.geometry("640x480")
tela.resizable(width=True, height=True)

escrever_texto = tki.Text(tela, font=("Comic Sans MS", 12))
escrever_texto.pack()

iniciar_menu = tki.Menu(tela)
novo_menu = tki.Menu(iniciar_menu, tearoff=0)  # Abre a aba de menu sem desencaixar

novo_menu.add_command(label="Novo", command=novo_arquivo)
novo_menu.add_command(label="Abrir", command=abrir_arquivo)
novo_menu.add_command(label="Salvar", command=salvar_arquivo)
novo_menu.add_command(label="Mover arquivo")
novo_menu.add_command(label="Sair", command=tela.quit)

# Barra de menu/Aba de ações
iniciar_menu.add_cascade(
    label="Arquivo", menu=novo_menu
)  # Adiciona o menu "Arquivo" na barra de menu
tela.config(menu=iniciar_menu)

tela.mainloop()
