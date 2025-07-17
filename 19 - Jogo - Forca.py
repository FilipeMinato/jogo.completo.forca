# Jogo da Forca com Interface Gráfica
# O jogador tenta adivinhar uma palavra secreta letra por letra.
# São permitidas até 6 tentativas incorretas.
# A interface é feita com Tkinter.

import tkinter as tk
from tkinter import messagebox
import random
import unicodedata

# ===============================
# Lista de palavras do jogo
# ===============================
# Temas variados: futebol, F1, economia, política, geografia, história...
lista_original = [
    'campeonato','goleiro','zagueiro','penalidade','escanteio','cartão','drible','torcida','uniforme','chuteira',
    'trave','gramado','falta','tecnico','volante','atacante','meio','estadio','escalação','tabela','passe',
    'marcação','substituição','impedimento','rebaixamento','liderança','largada','pódio','corrida','pneu','motor',
    'aerodinâmica','freio','volante','curva','boxe','combustível','parada','tempo','classificação','aceleração',
    'velocidade','ultrapassagem','pista','acidente','bandeira','pole','treino','vácuo','retardatário','equilíbrio',
    'inflação','juros','câmbio','balanço','ações','divida','lucro','crédito','investimento','salário','tributo',
    'banco','mercado','consumo','produto','capital','renda','importação','exportação','demanda','oferta',
    'recessão','déficit','superávit','carteira','governo','política','democracia','ditadura','revolução',
    'constituição','congresso','parlamento','ministro','exército','voto','urna','protesto','imposto','presidência',
    'nacionalismo','guerra','aliança','colonialismo','imperialismo','reforma','movimento','crise','poder',
    'território','planeta','continente','oceano','cordilheira','planície','deserto','floresta','rio','montanha',
    'vulcão','clima','latitude','longitude','altitude','bússola','mapa','região','costa','ilha','fronteira',
    'trópico','hemisfério','reserva','cachoeira','caverna','império','cavalo','feudalismo','idade','castelo',
    'armadura','nobreza','servidão','caravela','navegação','colonização','escravidão','indústria','renascimento',
    'invenção','ciência','progresso','iluminismo','república','monarquia','descobrimento','tradição','costume',
    'evento'
]

# Lista embaralhada de palavras disponíveis
palavras_disponiveis = []

# Variáveis do jogo
tentativas = 6  # Tentativas restantes
palavra = ""  # Palavra sorteada
letras_descobertas = []  # Letras corretas já reveladas


# ===============================
# Funções do jogo
# ===============================

def remover_acentos(txt):
    """
    Remove acentos da palavra para facilitar a comparação.
    Ex: 'é' vira 'e', 'ã' vira 'a'
    """
    return ''.join(c for c in unicodedata.normalize('NFD', txt) if unicodedata.category(c) != 'Mn')

def sortear_palavra():
    """
    Sorteia uma nova palavra da lista original, sem repetir até esgotar.
    """
    global palavras_disponiveis
    if not palavras_disponiveis:
        palavras_disponiveis = lista_original[:]
        random.shuffle(palavras_disponiveis)
    return palavras_disponiveis.pop()

def iniciar_jogo():
    """
    Inicia um novo jogo: sorteia palavra, reseta tentativas e letras descobertas.
    """
    global palavra, letras_descobertas, tentativas
    palavra = sortear_palavra()
    letras_descobertas = ['_' for _ in palavra]
    tentativas = 6
    atualizar_textos()

def atualizar_textos():
    """
    Atualiza os textos da interface: palavra parcial e tentativas restantes.
    """
    texto_palavra.config(text=' '.join(letras_descobertas))
    texto_tentativas.config(text=f'🧠 Você ainda tem {tentativas} chance(s)!')

def verificar_letra():
    """
    Verifica se a letra digitada está correta. Atualiza tentativas e a interface.
    """
    global tentativas
    letra_digitada = campo_letra.get().lower()  # Captura o texto digitado
    campo_letra.delete(0, tk.END)  # Limpa o campo após envio

    # Validação: apenas uma letra do alfabeto
    if len(letra_digitada) != 1 or not letra_digitada.isalpha():
        messagebox.showwarning("🚨 Atenção!", "Digite apenas UMA letra do alfabeto.")
        return

    # Verifica se a letra aparece na palavra
    acertou = False
    for i, letra_real in enumerate(palavra):
        if remover_acentos(letra_real) == remover_acentos(letra_digitada):
            letras_descobertas[i] = letra_real
            acertou = True

    # Se não acertou, perde uma tentativa
    if not acertou:
        tentativas -= 1

    # Atualiza os textos na interface
    atualizar_textos()

    # Vitória: não há mais letras ocultas
    if '_' not in letras_descobertas:
        jogar_novamente = messagebox.askyesno("🎉 Parabéns!", f"Você acertou! A palavra era '{palavra}'.\n\nDeseja jogar novamente?")
        if jogar_novamente:
            iniciar_jogo()
        else:
            janela.destroy()

    # Derrota: acabou as tentativas
    elif tentativas == 0:
        jogar_novamente = messagebox.askyesno("💀 Fim de jogo", f"Suas chances acabaram. A palavra era '{palavra}'.\n\nDeseja tentar de novo?")
        if jogar_novamente:
            iniciar_jogo()
        else:
            janela.destroy()


# ===============================
# Interface Gráfica com Tkinter
# ===============================

# Janela principal
janela = tk.Tk()
janela.title("🪂 Jogo da Forca - Mostre seu vocabulário!")
janela.geometry("460x360")
janela.resizable(False, False)

# Texto de explicação do jogo
explicacao = tk.Label(
    janela,
    text="💡 Adivinhe a palavra secreta, uma letra por vez!\n"
         "Você tem 6 chances. Cada erro custa uma tentativa.\n"
         "Pode
