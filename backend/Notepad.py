import tkinter as tki
from tkinter import filedialog, messagebox
import os
from datetime import datetime


def novo_arquivo():
    escrever_texto.delete(1.0, "end")
    pass


def mostrar_notificacao_diretorio_padrao(caminho_salvo):
    """Mostra uma notificação informando que o arquivo foi salvo no diretório padrão"""
    messagebox.showinfo(
        "Diretório não escolhido",
        f"Nenhum diretório foi selecionado.\n"
        f"Arquivo salvo no diretório padrão:\n\n"
        f"{caminho_salvo}",
    )


def salvar_arquivo():
    container = escrever_texto.get(1.0, "end")

    # Define o diretório padrão (pasta 'documentos' dentro do projeto)
    diretorio_padrao = os.path.join(os.path.dirname(__file__), "documentos")

    # Cria o diretório padrão se não existir
    if not os.path.exists(diretorio_padrao):
        os.makedirs(diretorio_padrao)

    # Abre diálogo para escolher onde salvar o arquivo
    arquivo_caminho = filedialog.asksaveasfilename(
        defaultextension=".md",
        filetypes=[
            ("Markdown files", "*.md"),
            ("Text files", "*.txt"),
            ("All files", "*.*"),
        ],
        title="Escolha onde salvar o arquivo (ou cancele para usar diretório padrão)",
    )

    # Se o usuário escolheu um caminho
    if arquivo_caminho:
        with open(arquivo_caminho, "w", encoding="utf-8") as arquivo:
            arquivo.write(container)
        messagebox.showinfo("Sucesso", f"Arquivo salvo em:\n{arquivo_caminho}")
    else:
        # Usuário cancelou - salva no diretório padrão
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo_padrao = f"documento_{timestamp}.md"
        caminho_padrao = os.path.join(diretorio_padrao, nome_arquivo_padrao)

        with open(caminho_padrao, "w", encoding="utf-8") as arquivo:
            arquivo.write(container)

        # Mostra notificação personalizada
        mostrar_notificacao_diretorio_padrao(caminho_padrao)


def abrir_arquivo():
    with filedialog.askopenfilename(
        defaultextension=".md",
        filetypes=[
            ("Markdown files", "*.md"),
            ("Text files", "*.txt"),
            ("All files", "*.*"),
        ],
        title="Escolha um arquivo para abrir",
    ) as arquivo:
        escrever_texto.delete(1.0, "end")
        escrever_texto.insert(1.0, arquivo.read())
    pass


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
novo_menu.add_command(label="Salvar Como")
novo_menu.add_command(label="Sair", command=tela.quit)

# Barra de menu/Aba de ações
iniciar_menu.add_cascade(
    label="Arquivo", menu=novo_menu
)  # Adiciona o menu "Arquivo" na barra de menu
tela.config(menu=iniciar_menu)

tela.mainloop()
