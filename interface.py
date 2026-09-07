import customtkinter as ctk
from PIL import Image
import os
import random

class ContextoAlienistaApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("O Contexto do Alienista")
        
        # 1. Define a resolução padrão ao restaurar/desmaximizar
        self.geometry("1280x720")
        
        # 2. Permite redimensionar a janela
        self.resizable(True, True)
        
        # 3. Define um tamanho mínimo para não quebrar o layout
        self.minsize(900, 600)

        # 4. Abre maximizado logo na inicialização
        self.after(0, lambda: self.state("zoomed"))

        # Container principal
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

        # Painel central estilizado
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
        self.carregar_tela_jogo()

    def carregar_tela_jogo(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.historico_tentativas = []
        # Palavra secreta mockada temporariamente
        self.palavra_secreta_mock = "a"

        # --- Top Bar ---
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

        # --- Container Central do Jogo ---
        game_container = ctk.CTkFrame(
            self.main_frame,
            corner_radius=15,
            fg_color="#1E1E1E",
            border_width=1,
            border_color="#3A3A3A"
        )
        game_container.pack(fill="both", expand=True, padx=40, pady=(0, 20))

        # --- Entrada de Palavra ---
        input_frame = ctk.CTkFrame(game_container, fg_color="transparent")
        input_frame.pack(fill="x", padx=30, pady=(20, 10))

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

        # --- Cabeçalho da Tabela ---
        header_table = ctk.CTkFrame(game_container, fg_color="#141414", height=35, corner_radius=6)
        header_table.pack(fill="x", padx=30, pady=(10, 5))

        lbl_h_pos = ctk.CTkLabel(header_table, text="Posição", font=ctk.CTkFont(family="Georgia", size=13, weight="bold"), text_color="#A0A0A0", width=80)
        lbl_h_pos.pack(side="left", padx=10)

        lbl_h_palavra = ctk.CTkLabel(header_table, text="Palpite", font=ctk.CTkFont(family="Georgia", size=13, weight="bold"), text_color="#A0A0A0")
        lbl_h_palavra.pack(side="left", padx=20)

        lbl_h_sim = ctk.CTkLabel(header_table, text="Proximidade", font=ctk.CTkFont(family="Georgia", size=13, weight="bold"), text_color="#A0A0A0", width=120)
        lbl_h_sim.pack(side="right", padx=10)

        # --- Lista de Tentativas ---
        self.scroll_historico = ctk.CTkScrollableFrame(game_container, fg_color="transparent")
        self.scroll_historico.pack(fill="both", expand=True, padx=30, pady=(0, 10))

        # --- Barra Inferior ---
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

    def processar_palpite(self):
        palpite = self.entry_palavra.get().strip().lower()
        if not palpite:
            return

        self.entry_palavra.delete(0, "end")

        # Mock: Verifica se acertou a palavra secreta ("a")
        if palpite == self.palavra_secreta_mock:
            self.carregar_tela_fim_jogo(motivo="vitoria", palavra_secreta=self.palavra_secreta_mock)
            return

        # Mock provisório enquanto o servidor não está conectado
        posicao_ficticia = random.randint(2, 500)
        
        self.historico_tentativas.append({"palavra": palpite, "posicao": posicao_ficticia})
        self.historico_tentativas.sort(key=lambda item: item["posicao"])
        
        self.atualizar_tabela_historico()

    def atualizar_tabela_historico(self):
        for widget in self.scroll_historico.winfo_children():
            widget.destroy()

        for item in self.historico_tentativas:
            row = ctk.CTkFrame(self.scroll_historico, fg_color="#262626", height=40, corner_radius=6)
            row.pack(fill="x", pady=4)

            cor_pos = "#52BE80" if item["posicao"] <= 50 else ("#F4D03F" if item["posicao"] <= 200 else "#E74C3C")

            lbl_pos = ctk.CTkLabel(row, text=f"#{item['posicao']}", font=ctk.CTkFont(family="Georgia", size=14, weight="bold"), text_color=cor_pos, width=80)
            lbl_pos.pack(side="left", padx=10)

            lbl_palavra = ctk.CTkLabel(row, text=item["palavra"], font=ctk.CTkFont(family="Georgia", size=14), text_color="#FFFFFF")
            lbl_palavra.pack(side="left", padx=20)

            barra_progresso = ctk.CTkProgressBar(row, width=120, height=10)
            progresso = max(0.05, 1.0 - (item["posicao"] / 500.0))
            barra_progresso.set(progresso)
            barra_progresso.pack(side="right", padx=10)

    def solicitar_dica(self):
        # Simulação temporária de dica
        self.historico_tentativas.append({"palavra": "alienista", "posicao": 42})
        self.historico_tentativas.sort(key=lambda item: item["posicao"])
        self.atualizar_tabela_historico()

    def solicitar_desistencia(self):
        # Quando o RPC estiver pronto, o servidor retornará a palavra secreta e a lista de palavras mais próximas.
        # Por enquanto, chamamos a tela com a palavra secreta 'a'.
        self.carregar_tela_fim_jogo(motivo="desistencia", palavra_secreta=self.palavra_secreta_mock)

    def carregar_tela_fim_jogo(self, motivo="desistencia", palavra_secreta="a", top_proximas=None):
        # Limpa widgets da tela anterior
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Mock de palavras mais próximas caso nenhuma lista venha do servidor
        if top_proximas is None:
            top_proximas = [
                {"palavra": "bacamarte", "posicao": 2, "similaridade": "0.94"},
                {"palavra": "alienista", "posicao": 3, "similaridade": "0.91"},
                {"palavra": "itaguai", "posicao": 4, "similaridade": "0.88"},
                {"palavra": "loucura", "posicao": 5, "similaridade": "0.85"},
                {"palavra": "hospicio", "posicao": 6, "similaridade": "0.81"}
            ]

        # Card Central de Resultado
        end_card = ctk.CTkFrame(
            self.main_frame,
            corner_radius=15,
            fg_color="#1E1E1E",
            border_width=1,
            border_color="#3A3A3A"
        )
        end_card.pack(fill="both", expand=True, padx=80, pady=40)

        # Cabeçalho de Status
        if motivo == "vitoria":
            titulo_texto = "🎉 Parabéns! Você Acertou!"
            cor_titulo = "#52BE80"
        else:
            titulo_texto = "Partida Encerrada (Desistência)"
            cor_titulo = "#E74C3C"

        lbl_status = ctk.CTkLabel(
            end_card,
            text=titulo_texto,
            text_color=cor_titulo,
            font=ctk.CTkFont(family="Georgia", size=26, weight="bold")
        )
        lbl_status.pack(pady=(25, 10))

        # Destaque da Palavra Secreta
        frame_resposta = ctk.CTkFrame(end_card, fg_color="#141414", corner_radius=10)
        frame_resposta.pack(fill="x", padx=60, pady=10)

        lbl_resposta_rotulo = ctk.CTkLabel(
            frame_resposta,
            text="A palavra secreta era:",
            text_color="#A0A0A0",
            font=ctk.CTkFont(family="Georgia", size=14)
        )
        lbl_resposta_rotulo.pack(pady=(10, 0))

        lbl_palavra_certa = ctk.CTkLabel(
            frame_resposta,
            text=palavra_secreta.upper(),
            text_color="#F0E6D2",
            font=ctk.CTkFont(family="Georgia", size=32, weight="bold")
        )
        lbl_palavra_certa.pack(pady=(0, 10))

        # Subtítulo das palavras mais próximas
        lbl_sub = ctk.CTkLabel(
            end_card,
            text="Palavras mais próximas da palavra secreta:",
            text_color="#CCCCCC",
            font=ctk.CTkFont(family="Georgia", size=15, weight="bold")
        )
        lbl_sub.pack(pady=(15, 5))

        # Tabela com as palavras mais próximas
        scroll_proximas = ctk.CTkScrollableFrame(end_card, fg_color="transparent")
        scroll_proximas.pack(fill="both", expand=True, padx=60, pady=(0, 15))

        for item in top_proximas:
            row = ctk.CTkFrame(scroll_proximas, fg_color="#262626", height=38, corner_radius=6)
            row.pack(fill="x", pady=3)

            lbl_p = ctk.CTkLabel(row, text=f"#{item['posicao']}", font=ctk.CTkFont(family="Georgia", size=13, weight="bold"), text_color="#52BE80", width=60)
            lbl_p.pack(side="left", padx=10)

            lbl_w = ctk.CTkLabel(row, text=item["palavra"], font=ctk.CTkFont(family="Georgia", size=14), text_color="#FFFFFF")
            lbl_w.pack(side="left", padx=15)

            lbl_s = ctk.CTkLabel(row, text=f"Sim: {item['similaridade']}", font=ctk.CTkFont(family="Georgia", size=13), text_color="#A0A0A0")
            lbl_s.pack(side="right", padx=15)

        # Botões de Ação Final
        bottom_actions = ctk.CTkFrame(end_card, fg_color="transparent")
        bottom_actions.pack(fill="x", padx=60, pady=(10, 25))

        btn_jogar_de_novo = ctk.CTkButton(
            bottom_actions,
            text="🔄 Jogar Novamente",
            height=42,
            width=200,
            font=ctk.CTkFont(family="Georgia", size=14, weight="bold"),
            fg_color="#2B2B2B",
            hover_color="#3D3D3D",
            command=self.carregar_tela_jogo
        )
        btn_jogar_de_novo.pack(side="left")

        btn_menu = ctk.CTkButton(
            bottom_actions,
            text="🏠 Voltar ao Início",
            height=42,
            width=200,
            font=ctk.CTkFont(family="Georgia", size=14),
            fg_color="#333333",
            hover_color="#444444",
            command=self.carregar_tela_inicial
        )
        btn_menu.pack(side="right")

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