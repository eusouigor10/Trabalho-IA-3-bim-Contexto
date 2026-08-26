import customtkinter as ctk
from PIL import Image

class ContextoAlienistaApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("O Contexto do Alienista")
        self.geometry("800x600")
        self.resizable(False, False)

        # Configuração do container principal
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        self.carregar_tela_inicial()

    def carregar_tela_inicial(self):
        # Limpa widgets anteriores caso venha de outra tela
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Opcional: Imagem de fundo (descomente e aponte para sua imagem)
        # img = Image.open("capa_alienista.jpg")
        # bg_image = ctk.CTkImage(light_image=img, dark_image=img, size=(800, 600))
        # bg_label = ctk.CTkLabel(self.main_frame, image=bg_image, text="")
        # bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Painel central para os botões (garante contraste com o fundo)
        menu_card = ctk.CTkFrame(self.main_frame, corner_radius=15, fg_color=("#E5DCC3", "#1A1A1A"))
        menu_card.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        titulo = ctk.CTkLabel(
            menu_card,
            text="O Contexto do Alienista",
            font=ctk.CTkFont(family="Georgia", size=26, weight="bold")
        )
        titulo.pack(padx=30, pady=(30, 20))

        # 4 Botões obrigatórios
        btn_jogar = ctk.CTkButton(menu_card, text="Iniciar Jogo", width=200, command=self.acao_jogar)
        btn_jogar.pack(padx=30, pady=8)

        btn_ajuda = ctk.CTkButton(menu_card, text="Ajuda", width=200, command=self.acao_ajuda)
        btn_ajuda.pack(padx=30, pady=8)

        btn_sobre = ctk.CTkButton(menu_card, text="Sobre", width=200, command=self.acao_sobre)
        btn_sobre.pack(padx=30, pady=8)

        btn_sair = ctk.CTkButton(menu_card, text="Sair", width=200, fg_color="#A93226", hover_color="#7B241C", command=self.destroy)
        btn_sair.pack(padx=30, pady=(8, 30))

    def acao_jogar(self):
        print("Transição para a tela da partida...")

    def acao_ajuda(self):
        print("Transição para a tela de ajuda com regras de jogabilidade...")

    def acao_sobre(self):
        print("Transição para a tela de créditos/autores e informações da UNESPAR...")