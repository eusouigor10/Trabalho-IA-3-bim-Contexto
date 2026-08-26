import customtkinter as ctk
from PIL import Image
import os

class ContextoAlienistaApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("O Contexto do Alienista")
        
        # 1. Define a resolução padrão ao restaurar/desmaximizar
        self.geometry("1280x720")
        
        # 2. Permite redimensionar a janela
        self.resizable(True, True)
        
        # 3. Define um tamanho mínimo para não quebrar o layout se o usuário encolher muito
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

        # Define quem será o "pai" do menu para a transparência funcionar
        parent_do_menu = self.main_frame 

        if os.path.exists(caminho_imagem):
            img_pil = Image.open(caminho_imagem)
            self.bg_image = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(1920, 1080))
            bg_label = ctk.CTkLabel(self.main_frame, image=self.bg_image, text="")
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            parent_do_menu = bg_label # O menu fica sobre a imagem

        # Painel central estilizado
        menu_card = ctk.CTkFrame(
            parent_do_menu, 
            corner_radius=20, 
            fg_color="#1E1E1E", # Fundo escuro fosco
            bg_color="transparent",
            border_width=2,
            border_color="#3A3A3A" # Borda sutil
        )
        menu_card.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        titulo = ctk.CTkLabel(
            menu_card,
            text="O Contexto do Alienista",
            text_color="#F0E6D2", # Tom de papel/creme
            font=ctk.CTkFont(family="Georgia", size=32, weight="bold")
        )
        titulo.pack(padx=40, pady=(35, 25))

        # Configuração padrão para todos os botões manterem o mesmo estilo
        btn_kwargs = {
            "width": 220,
            "height": 45,
            "font": ctk.CTkFont(family="Georgia", size=16),
            "corner_radius": 8,
            "fg_color": "#333333",
            "hover_color": "#555555",
            "text_color": "#FFFFFF"
        }

        # 4 Botões obrigatórios
        btn_jogar = ctk.CTkButton(menu_card, text="Iniciar Jogo", command=self.acao_jogar, **btn_kwargs)
        btn_jogar.pack(padx=40, pady=10)

        btn_ajuda = ctk.CTkButton(menu_card, text="Ajuda", command=self.acao_ajuda, **btn_kwargs)
        btn_ajuda.pack(padx=40, pady=10)

        btn_sobre = ctk.CTkButton(menu_card, text="Sobre", command=self.acao_sobre, **btn_kwargs)
        btn_sobre.pack(padx=40, pady=10)

        # O botão Sair ganha uma cor de destaque avermelhada
        btn_sair = ctk.CTkButton(
            menu_card, text="Sair", command=self.destroy,
            width=220, height=45, font=ctk.CTkFont(family="Georgia", size=16),
            corner_radius=8, fg_color="#6A2B2B", hover_color="#661313", text_color="#FFFFFF"
        )
        btn_sair.pack(padx=40, pady=(10, 35))

    def acao_jogar(self):
        self.carregar_tela_jogo()

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

        # Garante foco na janela modal
        self.transient(parent)
        self.grab_set()

        # Container principal com borda sutil
        card = ctk.CTkFrame(
            self, 
            corner_radius=15, 
            fg_color="#1E1E1E", 
            border_width=1, 
            border_color="#3A3A3A"
        )
        card.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        lbl_titulo = ctk.CTkLabel(
            card,
            text="Sobre o Projeto",
            text_color="#F0E6D2",
            font=ctk.CTkFont(family="Georgia", size=22, weight="bold")
        )
        lbl_titulo.pack(pady=(20, 15))

        # Texto descritivo e institucional
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

        # Botão Fechar
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
        self.geometry("620x540")
        self.resizable(False, False)

        # Garante foco na janela modal
        self.transient(parent)
        self.grab_set()

        # Card principal
        card = ctk.CTkFrame(
            self, 
            corner_radius=15, 
            fg_color="#1E1E1E", 
            border_width=1, 
            border_color="#3A3A3A"
        )
        card.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        lbl_titulo = ctk.CTkLabel(
            card,
            text="Como Jogar",
            text_color="#F0E6D2",
            font=ctk.CTkFont(family="Georgia", size=22, weight="bold")
        )
        lbl_titulo.pack(pady=(20, 15))

        # Regras resumidas e diretas baseadas na especificação
        texto_ajuda = (
            "Objetivo:\n"
            "Descubra a palavra secreta sorteada a partir do vocabulário do livro "
            "'O Alienista'.\n\n"
            "Regras e Mecânica:\n"
            "• Tentativas Ilimitadas: Digite palavras para testar sua proximidade semântica.\n"
            "• Ranking de Similaridade: Cada tentativa recebe uma posição. A palavra correta é a posição 1.\n"
            "• Quanto menor o número da posição, mais perto você está da resposta.\n"
            "• Dicas: Solicite uma dica para receber uma palavra mais próxima da solução do que suas tentativas atuais.\n"
            "• Desistência: Encerra a partida, revelando a palavra secreta e as mais próximas dela.\n"
            "• Sem limite de tempo: Jogue no seu próprio ritmo!"
        )

        lbl_conteudo = ctk.CTkLabel(
            card,
            text=texto_ajuda,
            text_color="#CCCCCC",
            font=ctk.CTkFont(family="Georgia", size=13),
            justify="left",
            wraplength=540
        )
        lbl_conteudo.pack(padx=25, pady=5)

        # Botão Fechar
        btn_fechar = ctk.CTkButton(
            card,
            text="Entendido",
            width=160,
            height=38,
            font=ctk.CTkFont(family="Georgia", size=14),
            corner_radius=8,
            fg_color="#2B2B2B",
            hover_color="#3D3D3D",
            text_color="#FFFFFF",
            command=self.destroy
        )
        btn_fechar.pack(pady=(20, 15))
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

        # Título
        lbl_titulo = ctk.CTkLabel(
            card,
            text="Como Jogar",
            text_color="#F0E6D2",
            font=ctk.CTkFont(family="Georgia", size=24, weight="bold")
        )
        lbl_titulo.pack(pady=(25, 20))

        # Container interno para os tópicos
        frame_conteudo = ctk.CTkFrame(card, fg_color="transparent")
        frame_conteudo.pack(fill="both", expand=True, padx=35)

        # 1. Seção Objetivo
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

        # 2. Seção Regras
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
            # pady=(0, 8) cria o espaçamento exato entre cada item da lista
            lbl_item.pack(fill="x", pady=(0, 8))

        # Botão Fechar
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
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Ajuda - Como Jogar")
        self.geometry("640x560")
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
        lbl_titulo.pack(pady=(25, 15))

        texto_ajuda = (
            "🎯 Objetivo Principal:\n"
            "Descubra a palavra secreta sorteada a partir do vocabulário do conto 'O Alienista'.\n\n"
            "📜 Regras e Mecânica:\n"
            "• Tentativas Ilimitadas: Digite palavras para medir a proximidade semântica.\n"
            "• Ranking de Similaridade: Cada tentativa recebe uma posição no ranking.\n"
            "• Posição 1: É a palavra secreta correta. Quanto menor o número, mais perto você está!\n"
            "• Dicas: Revela uma palavra intermediária mais próxima da resposta.\n"
            "• Desistência: Encerra a partida e revela a palavra secreta do dia.\n"
            "• Sem Pressão: Jogue sem limite de tempo no seu próprio ritmo."
        )

        lbl_conteudo = ctk.CTkLabel(
            card,
            text=texto_ajuda,
            text_color="#E0E0E0",
            font=ctk.CTkFont(family="Georgia", size=14),
            justify="left",
            wraplength=540,
            spacing3=8  # <-- Adiciona espaçamento vertical extra entre cada linha/parágrafo
        )
        lbl_conteudo.pack(padx=30, pady=(10, 20), fill="both", expand=True)

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
        btn_fechar.pack(pady=(0, 25))
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Ajuda - Como Jogar")
        self.geometry("620x540")
        self.resizable(False, False)

        # Garante foco na janela modal
        self.transient(parent)
        self.grab_set()

        # Card principal
        card = ctk.CTkFrame(
            self, 
            corner_radius=15, 
            fg_color="#1E1E1E", 
            border_width=1, 
            border_color="#3A3A3A"
        )
        card.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        lbl_titulo = ctk.CTkLabel(
            card,
            text="Como Jogar",
            text_color="#F0E6D2",
            font=ctk.CTkFont(family="Georgia", size=22, weight="bold")
        )
        lbl_titulo.pack(pady=(20, 15))

        # Regras resumidas e diretas baseadas na especificação
        texto_ajuda = (
            "Objetivo:\n"
            "Descubra a palavra secreta sorteada a partir do vocabulário do livro "
            "'O Alienista'.\n\n"
            "Regras e Mecânica:\n"
            "• Tentativas Ilimitadas: Digite palavras para testar sua proximidade semântica.\n"
            "• Ranking de Similaridade: Cada tentativa recebe uma posição. A palavra correta é a posição 1.\n"
            "• Quanto menor o número da posição, mais perto você está da resposta.\n"
            "• Dicas: Solicite uma dica para receber uma palavra mais próxima da solução do que suas tentativas atuais.\n"
            "• Desistência: Encerra a partida, revelando a palavra secreta e as mais próximas dela.\n"
            "• Sem limite de tempo: Jogue no seu próprio ritmo!"
        )

        lbl_conteudo = ctk.CTkLabel(
            card,
            text=texto_ajuda,
            text_color="#CCCCCC",
            font=ctk.CTkFont(family="Georgia", size=13),
            justify="left",
            wraplength=540
        )
        lbl_conteudo.pack(padx=25, pady=5)

        # Botão Fechar
        btn_fechar = ctk.CTkButton(
            card,
            text="Entendido",
            width=160,
            height=38,
            font=ctk.CTkFont(family="Georgia", size=14),
            corner_radius=8,
            fg_color="#2B2B2B",
            hover_color="#3D3D3D",
            text_color="#FFFFFF",
            command=self.destroy
        )
        btn_fechar.pack(pady=(20, 15))