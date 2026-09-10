import customtkinter as ctk
from interface import ContextoAlienistaApp

if __name__ == "__main__":
    # Configurações visuais do CustomTkinter
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Inicializa e roda a interface gráfica
    app = ContextoAlienistaApp()
    app.mainloop()