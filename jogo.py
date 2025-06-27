import tkinter as tk
from tkinter import messagebox
import random
import time

def dividir_em_grupos(lista, tamanho_grupo):
    return [lista[i:i + tamanho_grupo] for i in range(0, len(lista), tamanho_grupo)]

def mediana_manual(grupo):
    grupo_ordenado = sorted(grupo)
    meio = len(grupo_ordenado) // 2
    return grupo_ordenado[meio]

class MedianMasterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("🧠 Median Master - Avançado")
        self.pontos = 0
        self.rodadas = 0
        self.max_rodadas = 10
        self.dificuldade = 'Fácil'
        self.tempo_limite = 30
        self.start_time = 0
        self.tamanho_grupo = 5
        self.total_numeros = 25
        self.timer_id = None

        # Título e Instruções
        tk.Label(master, text="Escolha a Dificuldade:", font=("Helvetica", 13)).pack()
        self.dificuldade_var = tk.StringVar(value="Fácil")
        for diff in ["Fácil", "Médio", "Difícil"]:
            tk.Radiobutton(master, text=diff, variable=self.dificuldade_var, value=diff, command=self.ajustar_dificuldade).pack()

        self.label_instrucao = tk.Label(master, text="Clique em 'Nova Rodada' para começar!", font=("Helvetica", 14))
        self.label_instrucao.pack(pady=10)

        self.text_area = tk.Text(master, height=18, width=70, font=("Courier", 11))
        self.text_area.pack(pady=5)

        self.entry = tk.Entry(master, font=("Helvetica", 14))
        self.entry.pack()

        self.button_verificar = tk.Button(master, text="Verificar", command=self.verificar_resposta, font=("Helvetica", 12))
        self.button_verificar.pack(pady=5)

        self.button_nova = tk.Button(master, text="Nova Rodada", command=self.nova_rodada, font=("Helvetica", 12))
        self.button_nova.pack(pady=5)

        self.label_pontos = tk.Label(master, text="Pontos: 0", font=("Helvetica", 12, "bold"))
        self.label_pontos.pack(pady=5)

        self.label_tempo = tk.Label(master, text="⏱️ Tempo restante: --", font=("Helvetica", 12, "bold"))
        self.label_tempo.pack()
    
    def ajustar_dificuldade(self):
        dificuldade = self.dificuldade_var.get()
        if dificuldade == "Fácil":
            self.tamanho_grupo = 5
            self.total_numeros = 25
        elif dificuldade == "Médio":
            self.tamanho_grupo = 7
            self.total_numeros = 49
        else:
            self.tamanho_grupo = 9
            self.total_numeros = 81

    def iniciar_timer(self):
        self.start_time = time.time()
        self.atualizar_timer()

    def atualizar_timer(self):
        tempo_passado = int(time.time() - self.start_time)
        tempo_restante = self.tempo_limite - tempo_passado
        self.label_tempo.config(text=f"⏱️ Tempo restante: {tempo_restante}s")
        if tempo_restante <= 0:
            self.label_tempo.config(text="⏱️ Tempo esgotado!")
            messagebox.showwarning("Tempo!", "⏰ O tempo acabou!")
            self.verificar_resposta(timeout=True)
        else:
            self.timer_id = self.master.after(1000, self.atualizar_timer)

    def nova_rodada(self):
        if self.rodadas >= self.max_rodadas:
            messagebox.showinfo("Fim de Jogo", f"🏁 Você completou {self.max_rodadas} rodadas.\nPontuação final: {self.pontos}")
            self.master.quit()
            return

        self.ajustar_dificuldade()
        self.rodadas += 1
        self.entry.delete(0, tk.END)
        self.text_area.delete("1.0", tk.END)

        self.lista = random.sample(range(1, 200), self.total_numeros)
        self.grupos = dividir_em_grupos(self.lista, self.tamanho_grupo)
        self.medianas = [mediana_manual(g) for g in self.grupos]
        self.resposta_correta = mediana_manual(self.medianas)

        self.text_area.insert(tk.END, f"🎯 Rodada {self.rodadas}/{self.max_rodadas} - Dificuldade: {self.dificuldade_var.get()}\n\n")
        self.text_area.insert(tk.END, "📊 Lista completa:\n")
        self.text_area.insert(tk.END, f"{self.lista}\n\n")

        for i, g in enumerate(self.grupos):
            self.text_area.insert(tk.END, f"Grupo {i+1}: {g} → Mediana: {mediana_manual(g)}\n")

        self.text_area.insert(tk.END, f"\n🧮 Medianas: {self.medianas}")
        self.text_area.insert(tk.END, f"\n\n👉 Digite abaixo qual é a *Mediana das Medianas*:")

        if self.timer_id:
            self.master.after_cancel(self.timer_id)

        self.iniciar_timer()



  