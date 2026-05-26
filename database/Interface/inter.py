import customtkinter as ctk

ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.geometry("400x300")

texto = ctk.CTkLabel(app, text="Interfaz moderna")
texto.pack(pady=20)

def boton_click():
    texto.configure(text="Botón presionado")

boton = ctk.CTkButton(app, text="Click", command=boton_click)
boton.pack(pady=20)

app.mainloop()


