import os
import customtkinter as ctk
from PIL import Image
from cliente import Cliente

class ContextoAlienistaApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("O Contexto do Alienista")
        self.geometry("1280x720")
        self.resizable(True, True)
        self.minsize(900, 600)
        self.after(0, lambda: self.state("zoomed"))

        # Conexão com o servidor RPC
        try:
            self.cliente_rpc = Cliente()
        except Exception as e:
            self.cliente_rpc = None
            print(f"Erro ao instanciar cliente RPC: {e}")

        self.historico_palpites = []  # Lista com as tentativas do jogador

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        self.carregar_tela_inicial()

    def carregar_tela_inicial(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        caminho_base = os.path.dirname(os.path.abspath(__file__))
        caminho_imagem = os.path.join(caminho_base, "assets", "capa_alienista_1080p.png")

        parent_do_menu = self.main_frame

        if os.path.exists(caminho_imagem):
            img_pil = Image.open(caminho_imagem)
            self.bg_image = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(1920, 1080))
            bg_label = ctk.CTkLabel(self.main_frame, image=self.bg_image, text="")
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            parent_do_menu = bg_label

        menu_card = ctk.CTkFrame(
            parent_do_menu,
            corner_radius=20,
            fg_color="#1E1E1E",
            bg_color="transparent",
            border_width=2,
            border_color="#3A3A3A"
        )
        menu_card.place(relx=0.5, rely=0.5, anchor="center")

        titulo = ctk.CTkLabel(
            menu_card,
            text="O Contexto do Alienista",
            text_color="#F0E6D2",
            font=ctk.CTkFont(family="Georgia", size=32, weight="bold")
        )
        titulo.pack(padx=40, pady=(35, 25))

        btn_kwargs = {
            "width": 220,
            "height": 45,
            "font": ctk.CTkFont(family="Georgia", size=16),
            "corner_radius": 8,
            "fg_color": "#333333",
            "hover_color": "#555555",
            "text_color": "#FFFFFF"
        }

        btn_jogar = ctk.CTkButton(menu_card, text="Iniciar Jogo", command=self.acao_jogar, **btn_kwargs)
        btn_jogar.pack(padx=40, pady=10)

        btn_ajuda = ctk.CTkButton(menu_card, text="Ajuda", command=self.acao_ajuda, **btn_kwargs)
        btn_ajuda.pack(padx=40, pady=10)

        btn_sobre = ctk.CTkButton(menu_card, text="Sobre", command=self.acao_sobre, **btn_kwargs)
        btn_sobre.pack(padx=40, pady=10)

        btn_sair = ctk.CTkButton(
            menu_card, text="Sair", command=self.destroy,
            width=220, height=45, font=ctk.CTkFont(family="Georgia", size=16),
            corner_radius=8, fg_color="#6A2B2B", hover_color="#661313", text_color="#FFFFFF"
        )
        btn_sair.pack(padx=40, pady=(10, 35))

    def acao_jogar(self):
        try:
            # Chama o sorteio no servidor
            self.cliente_rpc.iniciar_jogo()
            self.historico_palpites = []
            self.carregar_tela_jogo()
        except Exception as e:
            self.mostrar_alerta(f"Não foi possível conectar ao servidor RPC:\n{e}")

    def carregar_tela_jogo(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        top_bar = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top_bar.pack(fill="x", padx=40, pady=(20, 10))

        btn_voltar = ctk.CTkButton(
            top_bar,
            text="← Voltar ao Menu",
            width=140,
            height=35,
            font=ctk.CTkFont(family="Georgia", size=13),
            corner_radius=8,
            fg_color="#2B2B2B",
            hover_color="#3D3D3D",
            command=self.carregar_tela_inicial
        )
        btn_voltar.pack(side="left")

        lbl_titulo_jogo = ctk.CTkLabel(
            top_bar,
            text="O Contexto do Alienista",
            text_color="#F0E6D2",
            font=ctk.CTkFont(family="Georgia", size=24, weight="bold")
        )
        lbl_titulo_jogo.pack(side="right")

        game_container = ctk.CTkFrame(
            self.main_frame,
            corner_radius=15,
            fg_color="#1E1E1E",
            border_width=1,
            border_color="#3A3A3A"
        )
        game_container.pack(fill="both", expand=True, padx=40, pady=(0, 20))

        input_frame = ctk.CTkFrame(game_container, fg_color="transparent")
        input_frame.pack(fill="x", padx=30, pady=(20, 5))

        self.entry_palavra = ctk.CTkEntry(
            input_frame,
            placeholder_text="Digite seu palpite...",
            height=45,
            font=ctk.CTkFont(family="Georgia", size=15),
            border_color="#3A3A3A",
            fg_color="#141414"
        )
        self.entry_palavra.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry_palavra.bind("<Return>", lambda event: self.processar_palpite())

        btn_enviar = ctk.CTkButton(
            input_frame,
            text="Enviar",
            width=120,
            height=45,
            font=ctk.CTkFont(family="Georgia", size=15, weight="bold"),
            fg_color="#2B2B2B",
            hover_color="#3D3D3D",
            command=self.processar_palpite
        )
        btn_enviar.pack(side="right")

        self.lbl_feedback = ctk.CTkLabel(
            game_container,
            text="",
            text_color="#E74C3C",
            font=ctk.CTkFont(family="Georgia", size=13)
        )
        self.lbl_feedback.pack(fill="x", padx=30, pady=(0, 5))

        header_table = ctk.CTkFrame(game_container, fg_color="#141414", height=35, corner_radius=6)
        header_table.pack(fill="x", padx=30, pady=(5, 5))

        lbl_h_pos = ctk.CTkLabel(header_table, text="Posição", font=ctk.CTkFont(family="Georgia", size=13, weight="bold"), text_color="#A0A0A0", width=90)
        lbl_h_pos.pack(side="left", padx=10)

        lbl_h_palavra = ctk.CTkLabel(header_table, text="Palpite", font=ctk.CTkFont(family="Georgia", size=13, weight="bold"), text_color="#A0A0A0")
        lbl_h_palavra.pack(side="left", padx=20)

        lbl_h_sim = ctk.CTkLabel(header_table, text="Distância", font=ctk.CTkFont(family="Georgia", size=13, weight="bold"), text_color="#A0A0A0", width=120)
        lbl_h_sim.pack(side="right", padx=15)

        self.scroll_historico = ctk.CTkScrollableFrame(game_container, fg_color="transparent")
        self.scroll_historico.pack(fill="both", expand=True, padx=30, pady=(0, 10))

        bottom_bar = ctk.CTkFrame(game_container, fg_color="transparent")
        bottom_bar.pack(fill="x", padx=30, pady=(10, 20))

        btn_dica = ctk.CTkButton(
            bottom_bar,
            text="💡 Pedir Dica",
            height=40,
            font=ctk.CTkFont(family="Georgia", size=14),
            fg_color="#2B2B2B",
            hover_color="#3D3D3D",
            command=self.solicitar_dica
        )
        btn_dica.pack(side="left")

        btn_desistir = ctk.CTkButton(
            bottom_bar,
            text="🏴 Desistir",
            height=40,
            font=ctk.CTkFont(family="Georgia", size=14),
            fg_color="#4A1C1C",
            hover_color="#5E2323",
            command=self.solicitar_desistencia
        )
        btn_desistir.pack(side="right")

        self.entry_palavra.focus()

    def processar_palpite(self):
        palpite = self.entry_palavra.get().strip().lower()
        if not palpite:
            return

        self.entry_palavra.delete(0, "end")
        self.lbl_feedback.configure(text="")

        try:
            resposta = self.cliente_rpc.tentar_palavra(palpite)

            if not resposta.get("sucesso", False):
                self.lbl_feedback.configure(text=resposta.get("mensagem", "Palavra inválida."))
                return

            # Adiciona ao histórico local se ainda não tentou
            if not any(item["palavra"] == resposta["palavra"] for item in self.historico_palpites):
                self.historico_palpites.append(resposta)

            self.atualizar_tabela_historico()

            if resposta.get("acertou", False):
                desistencia = self.cliente_rpc.desistir()
                self.carregar_tela_fim_jogo(
                    motivo="vitoria",
                    palavra_secreta=resposta["palavra"],
                    top_proximas=desistencia.get("top_ranking", [])[:30]
                )

        except Exception as e:
            self.lbl_feedback.configure(text=f"Erro na comunicação com o servidor: {e}")

    def solicitar_dica(self):
        self.lbl_feedback.configure(text="")
        try:
            resposta = self.cliente_rpc.pedir_dica()
            if not resposta.get("sucesso", False):
                self.lbl_feedback.configure(text=resposta.get("mensagem", "Sem dicas disponíveis."))
                return

            if not any(item["palavra"] == resposta["palavra"] for item in self.historico_palpites):
                self.historico_palpites.append(resposta)

            self.atualizar_tabela_historico()
            self.lbl_feedback.configure(text=f"💡 Dica recebida: {resposta['palavra']} (Posição #{resposta['posicao']})", text_color="#F4D03F")

        except Exception as e:
            self.lbl_feedback.configure(text=f"Erro ao solicitar dica: {e}")

    def solicitar_desistencia(self):
        try:
            dados = self.cliente_rpc.desistir()
            self.carregar_tela_fim_jogo(
                motivo="desistencia",
                palavra_secreta=dados.get("palavra_sorteada", "---"),
                top_proximas=dados.get("top_ranking", [])[:30]
            )
        except Exception as e:
            self.mostrar_alerta(f"Erro ao desistir: {e}")

    def atualizar_tabela_historico(self):
        # Limpa widgets anteriores do histórico
        for widget in self.scroll_historico.winfo_children():
            widget.destroy()

        # Ordena as tentativas: menor posição primeiro (mais próxima do 1)
        ordenados = sorted(self.historico_palpites, key=lambda x: x["posicao"])

        for item in ordenados:
            pos = item["posicao"]

            # Cores ajustadas para manter contraste nítido com texto claro ou escuro
            if pos == 1:
                cor_barra = "#196F3D"  # Verde escuro vitorioso
                cor_texto = "#FFFFFF"
                cor_num = "#A9DFBF"
            elif pos <= 10:
                cor_barra = "#1E8449"  # Verde equilibrado
                cor_texto = "#FFFFFF"
                cor_num = "#D5F5E3"
            elif pos <= 50:
                cor_barra = "#B7950B"  # Mostarda escuro (substitui o amarelo claro ofuscante)
                cor_texto = "#FFFFFF"
                cor_num = "#F9E79F"
            elif pos <= 200:
                cor_barra = "#A04000"  # Laranja terroso/queimado
                cor_texto = "#FFFFFF"
                cor_num = "#EDBB99"
            else:
                cor_barra = "#212121"  # Fundo neutro discreto
                cor_texto = "#D5D5D5"
                cor_num = "#85929E"

            row = ctk.CTkFrame(self.scroll_historico, fg_color=cor_barra, height=38, corner_radius=6)
            row.pack(fill="x", pady=2)

            lbl_p = ctk.CTkLabel(
                row, 
                text=f"#{pos}", 
                font=ctk.CTkFont(family="Georgia", size=13, weight="bold"), 
                text_color=cor_num, 
                width=90
            )
            lbl_p.pack(side="left", padx=10)

            lbl_w = ctk.CTkLabel(
                row, 
                text=item["palavra"], 
                font=ctk.CTkFont(family="Georgia", size=14, weight="bold"), 
                text_color=cor_texto
            )
            lbl_w.pack(side="left", padx=15)

            dist_val = f"{item['distancia']:.4f}" if isinstance(item["distancia"], float) else str(item["distancia"])
            lbl_s = ctk.CTkLabel(
                row, 
                text=dist_val, 
                font=ctk.CTkFont(family="Georgia", size=13), 
                text_color=cor_texto, 
                width=120
            )
            lbl_s.pack(side="right", padx=15)

    def carregar_tela_fim_jogo(self, motivo="desistencia", palavra_secreta="---", top_proximas=None):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        if top_proximas is None:
            top_proximas = []

        end_card = ctk.CTkFrame(
            self.main_frame,
            corner_radius=15,
            fg_color="#1E1E1E",
            border_width=1,
            border_color="#3A3A3A"
        )
        end_card.pack(fill="both", expand=True, padx=80, pady=30)

        titulo_texto = "🎉 Parabéns! Você Acertou!" if motivo == "vitoria" else "Partida Encerrada (Desistência)"
        cor_titulo = "#52BE80" if motivo == "vitoria" else "#E74C3C"

        lbl_status = ctk.CTkLabel(
            end_card,
            text=titulo_texto,
            text_color=cor_titulo,
            font=ctk.CTkFont(family="Georgia", size=26, weight="bold")
        )
        lbl_status.pack(pady=(20, 5))

        frame_resposta = ctk.CTkFrame(end_card, fg_color="#141414", corner_radius=10)
        frame_resposta.pack(fill="x", padx=60, pady=8)

        lbl_resposta_rotulo = ctk.CTkLabel(
            frame_resposta,
            text="A palavra secreta era:",
            text_color="#A0A0A0",
            font=ctk.CTkFont(family="Georgia", size=13)
        )
        lbl_resposta_rotulo.pack(pady=(6, 0))

        lbl_palavra_certa = ctk.CTkLabel(
            frame_resposta,
            text=palavra_secreta.upper(),
            text_color="#F0E6D2",
            font=ctk.CTkFont(family="Georgia", size=28, weight="bold")
        )
        lbl_palavra_certa.pack(pady=(0, 6))

        lbl_sub = ctk.CTkLabel(
            end_card,
            text="Top palavras mais próximas:",
            text_color="#CCCCCC",
            font=ctk.CTkFont(family="Georgia", size=14, weight="bold")
        )
        lbl_sub.pack(pady=(8, 4))

        scroll_proximas = ctk.CTkScrollableFrame(end_card, fg_color="transparent")
        scroll_proximas.pack(fill="both", expand=True, padx=60, pady=(0, 10))

        for item in top_proximas:
            row = ctk.CTkFrame(scroll_proximas, fg_color="#262626", height=34, corner_radius=6)
            row.pack(fill="x", pady=2)

            lbl_p = ctk.CTkLabel(row, text=f"#{item['posicao']}", font=ctk.CTkFont(family="Georgia", size=12, weight="bold"), text_color="#52BE80", width=60)
            lbl_p.pack(side="left", padx=10)

            lbl_w = ctk.CTkLabel(row, text=item["palavra"], font=ctk.CTkFont(family="Georgia", size=13), text_color="#FFFFFF")
            lbl_w.pack(side="left", padx=15)

            lbl_s = ctk.CTkLabel(row, text=f"Dist: {item['similaridade']}", font=ctk.CTkFont(family="Georgia", size=12), text_color="#A0A0A0")
            lbl_s.pack(side="right", padx=15)

        bottom_actions = ctk.CTkFrame(end_card, fg_color="transparent")
        bottom_actions.pack(fill="x", padx=60, pady=(10, 15))

        btn_jogar_de_novo = ctk.CTkButton(
            bottom_actions,
            text="🔄 Jogar Novamente",
            height=40,
            width=180,
            font=ctk.CTkFont(family="Georgia", size=13, weight="bold"),
            fg_color="#2B2B2B",
            hover_color="#3D3D3D",
            command=self.acao_jogar
        )
        btn_jogar_de_novo.pack(side="left")

        btn_menu = ctk.CTkButton(
            bottom_actions,
            text="🏠 Voltar ao Início",
            height=40,
            width=180,
            font=ctk.CTkFont(family="Georgia", size=13),
            fg_color="#333333",
            hover_color="#444444",
            command=self.carregar_tela_inicial
        )
        btn_menu.pack(side="right")

    def mostrar_alerta(self, mensagem):
        janela = ctk.CTkToplevel(self)
        janela.geometry("380x180")
        janela.title("Aviso")
        janela.transient(self)
        janela.grab_set()

        lbl = ctk.CTkLabel(janela, text=mensagem, wraplength=320, font=ctk.CTkFont(family="Georgia", size=13))
        lbl.pack(expand=True, pady=15)

        btn = ctk.CTkButton(janela, text="OK", command=janela.destroy, width=100)
        btn.pack(pady=(0, 15))

    def acao_ajuda(self):
        JanelaAjuda(self)

    def acao_sobre(self):
        JanelaSobre(self)


class JanelaSobre(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Sobre - O Contexto do Alienista")
        self.geometry("560x480")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        card = ctk.CTkFrame(
            self, 
            corner_radius=15, 
            fg_color="#1E1E1E", 
            border_width=1, 
            border_color="#3A3A3A"
        )
        card.pack(fill="both", expand=True, padx=20, pady=20)

        lbl_titulo = ctk.CTkLabel(
            card,
            text="Sobre o Projeto",
            text_color="#F0E6D2",
            font=ctk.CTkFont(family="Georgia", size=22, weight="bold")
        )
        lbl_titulo.pack(pady=(20, 15))

        texto_sobre = (
            "Desenvolvimento de um jogo eletrônico inspirado na mecânica do "
            "Contexto, utilizando como corpus textual o livro 'O Alienista' "
            "de Machado de Assis.\n\n"
            "Desenvolvido por:\n"
            "• Igor Gabriel Daré Grubisich\n"
            "• Kauan Gomes Cardoso\n\n"
            "Instituição:\n"
            "UNESPAR - Universidade Estadual do Paraná\n"
            "Bacharelado em Ciência da Computação\n\n"
            "Disciplinas Integradas:\n"
            "• Inteligência Artificial\n"
            "• Redes de Computadores e Sistemas Distribuídos\n\n"
            "Docente Responsável:\n"
            "Profª. Dra. Lailla Milainny Siqueira Bine"
        )

        lbl_conteudo = ctk.CTkLabel(
            card,
            text=texto_sobre,
            text_color="#CCCCCC",
            font=ctk.CTkFont(family="Georgia", size=13),
            justify="center",
            wraplength=480
        )
        lbl_conteudo.pack(padx=20, pady=5)

        btn_fechar = ctk.CTkButton(
            card,
            text="Voltar",
            width=160,
            height=38,
            font=ctk.CTkFont(family="Georgia", size=14),
            corner_radius=8,
            fg_color="#2B2B2B",
            hover_color="#3D3D3D",
            text_color="#FFFFFF",
            command=self.destroy
        )
        btn_fechar.pack(pady=(15, 15))


class JanelaAjuda(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Ajuda - Como Jogar")
        self.geometry("640x580")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        card = ctk.CTkFrame(
            self, 
            corner_radius=15, 
            fg_color="#1E1E1E", 
            border_width=1, 
            border_color="#3A3A3A"
        )
        card.pack(fill="both", expand=True, padx=25, pady=25)

        lbl_titulo = ctk.CTkLabel(
            card,
            text="Como Jogar",
            text_color="#F0E6D2",
            font=ctk.CTkFont(family="Georgia", size=24, weight="bold")
        )
        lbl_titulo.pack(pady=(25, 20))

        frame_conteudo = ctk.CTkFrame(card, fg_color="transparent")
        frame_conteudo.pack(fill="both", expand=True, padx=35)

        lbl_obj_titulo = ctk.CTkLabel(
            frame_conteudo,
            text="🎯 Objetivo Principal:",
            text_color="#F0E6D2",
            font=ctk.CTkFont(family="Georgia", size=15, weight="bold"),
            anchor="w"
        )
        lbl_obj_titulo.pack(fill="x", pady=(0, 4))

        lbl_obj_texto = ctk.CTkLabel(
            frame_conteudo,
            text="Descubra a palavra secreta sorteada a partir do vocabulário do conto 'O Alienista'.",
            text_color="#CCCCCC",
            font=ctk.CTkFont(family="Georgia", size=13),
            justify="left",
            wraplength=520,
            anchor="w"
        )
        lbl_obj_texto.pack(fill="x", pady=(0, 18))

        lbl_regras_titulo = ctk.CTkLabel(
            frame_conteudo,
            text="📜 Regras e Mecânica:",
            text_color="#F0E6D2",
            font=ctk.CTkFont(family="Georgia", size=15, weight="bold"),
            anchor="w"
        )
        lbl_regras_titulo.pack(fill="x", pady=(0, 6))

        regras_itens = [
            "• Tentativas Ilimitadas: Digite palavras para testar a proximidade semântica.",
            "• Ranking de Similaridade: Cada tentativa recebe uma posição no ranking.",
            "• Posição 1: É a palavra correta. Quanto menor o número, mais perto você está!",
            "• Dicas: Revela uma palavra intermediária mais próxima da resposta.",
            "• Desistência: Encerra a partida e revela a palavra secreta e o ranking.",
            "• Sem Pressão: Jogue sem limite de tempo no seu próprio ritmo."
        ]

        for item in regras_itens:
            lbl_item = ctk.CTkLabel(
                frame_conteudo,
                text=item,
                text_color="#CCCCCC",
                font=ctk.CTkFont(family="Georgia", size=13),
                justify="left",
                wraplength=520,
                anchor="w"
            )
            lbl_item.pack(fill="x", pady=(0, 8))

        btn_fechar = ctk.CTkButton(
            card,
            text="Entendido",
            width=160,
            height=40,
            font=ctk.CTkFont(family="Georgia", size=15),
            corner_radius=8,
            fg_color="#2B2B2B",
            hover_color="#3D3D3D",
            text_color="#FFFFFF",
            command=self.destroy
        )
        btn_fechar.pack(pady=(15, 20))