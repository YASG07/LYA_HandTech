from tkinter import *
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox as mb
from lexico import tokens,reserved,lexer
from sintactico import parser, yacc
import tkinter as tk
from tkinter import filedialog, messagebox


#Estructura Visual del compilador y funciones basicas

#En la siguiente clase creamos un Scroll que tenga numeros al costado que contabiliza los renglones
#como es en los Compiladores habituales
'''
ACLARACION:
la clase ScrollTextWithLineNumbers simula como cuadro de codigo que simula al del cualquier compilador
pero existe un problema y es que no funciona tan bien como se esperaba ya que apesar de que se modifique
sus dimensiones la numeracion seguira aumentando más no se mostraran. Así que si ven que su limite es
24 lineas, apesar que el codigo sea de más renglones, no se pudo corregir este bug.
'''
class ScrollTextWithLineNumbers(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)  # Llama al constructor de la clase base (Frame)

        # Crear el widget de números de línea
        self.line_numbers = Text(self, width=4, padx=4, wrap='none')
        self.line_numbers.pack(side='left', fill='y')  # Empaqueta el widget en el lado izquierdo y lo hace llenar en la dirección y

        # Crear el widget de texto desplazable
        self.text_widget = ScrolledText(self, width=105, height=10)
        self.text_widget.pack(side='left', fill='both', expand=True)  # Empaqueta el widget en el lado izquierdo y lo hace llenar en ambas direcciones y expandir su tamaño

        # Crear la barra de desplazamiento
        self.scrollbar = Scrollbar(self, command=self._scroll_text)
        self.scrollbar.pack(side='right', fill='y')  # Empaqueta la barra de desplazamiento en el lado derecho y lo hace llenar en la dirección y

        # Configurar los comandos de desplazamiento
        self.text_widget.config(yscrollcommand=self.scrollbar.set)  # Configura el comando de desplazamiento vertical
        self.scrollbar.config(command=self.text_widget.yview)  # Configura el comando de la barra de desplazamiento

        # Asignar eventos a los widgets de texto
        self.text_widget.bind_all('<Key>', self._on_text_change)  # Asigna el evento Key (tecla) al método _on_text_change
        self.text_widget.bind('<Return>', self._on_text_change)  # Asigna el evento Return (retorno) al método _on_text_change
        self.text_widget.bind('<Button-4>', self._scroll_up)  # Asigna el evento Button-4 (rueda del mouse hacia arriba) al método _scroll_up
        self.text_widget.bind('<Button-5>', self._scroll_down)  # Asigna el evento Button-5 (rueda del mouse hacia abajo) al método _scroll_down
        
        # Actualizar los números de línea
        self._update_line_numbers()
        
    def _scroll_text(self, *args):
        self.text_widget.yview(*args)
        self._update_line_numbers()
        
    def _on_text_change(self, event):
        self._update_line_numbers()
        
    def _scroll_up(self, event):
        self.text_widget.yview_scroll(-1, 'units')
        self._update_line_numbers()
        
    def _scroll_down(self, event):
        self.text_widget.yview_scroll(1, 'units')
        self._update_line_numbers()
        
    def _update_line_numbers(self):
        lines = self.text_widget.get(1.0, 'end').split('\n')
        line_numbers = '\n'.join(str(i) for i in range(1, len(lines)))
        self.line_numbers.config(state='normal')
        self.line_numbers.delete(1.0, 'end')
        self.line_numbers.insert(1.0, line_numbers)
        self.line_numbers.config(state='disabled')

    def get_text(self):
        return self.text_widget.get(1.0, 'end-1c')
    
    def set_text(self, new_text):
        self.text_widget.delete(1.0, 'end')  # Borra el texto existente
        self.text_widget.insert('end', new_text)  # Inserta el nuevo texto al final del widget
        self._update_line_numbers()  # Actualiza la numeración de líneas

    def clear_scroll_text(self):
        self.text_widget.delete(1.0, 'end')  # Borra todo el texto en el widget
        self._update_line_numbers()  # Actualiza la numeración de líneas

#LISTA DE FUNCIONES EXISTENTES

def analisisSintactico():
    cadena = scroll_text_widget.get_text()
    if len(cadena) > 0:
        try:
            resultado = parser.parse(cadena)
            mostrarAnalisisSintactico2(resultado)
        except yacc.YaccError as e:
            print("Error durante el análisis sintáctico:", e)
            mb.showerror("Error", str(e))
    else:
        mb.showwarning("ERROR", "Debes escribir código")
       
'''
def mostrarAnalisisSintactico(data):
    scrollAnalisis.config(state="normal")  # Cambiar el estado a normal para permitir la edición
    scrollAnalisis.delete(1.0, END)  # Borrar el contenido previo
    if isinstance(data, (int, float)):
        scrollAnalisis.insert(END, str(data) + '\n')
    else:
        for item in data:
            scrollAnalisis.insert(END, str(item) + '\n')
    scrollAnalisis.config(state="disabled")  # Volver a deshabilitar la edición      
'''

#Mostrar el analisis sintactico en un ventana aparte 
def mostrarAnalisisSintactico2(data):
    # Crear una nueva ventana
    nueva_ventana = tk.Toplevel()
    nueva_ventana.title("Análisis Sintáctico")
    # Crear un Text widget con un Scrollbar
    text_area = Text(nueva_ventana, wrap='word')
    scrollbar = Scrollbar(nueva_ventana, command=text_area.yview)
    text_area.configure(yscrollcommand=scrollbar.set)

    # Configurar la posición de los widgets
    text_area.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')

    # Insertar datos en el Text widget
    text_area.config(state="normal")  # Cambiar el estado a normal para permitir la edición
    text_area.delete(1.0, END)  # Borrar el contenido previo
    if isinstance(data, (int, float)):
        text_area.insert(END, str(data) + '\n')
    else:
        for item in data:
            text_area.insert(END, str(item) + '\n')
    text_area.config(state="disabled")  # Volver a deshabilitar la edición


#Mostrar el analisis lexico en un ventana aparte 
def mostrarAnalisisLexico2(tokens):
    # Crear una nueva ventana
    nueva_ventana = tk.Toplevel()
    nueva_ventana.title("Análisis Léxico")

    # Crear un Text widget con un Scrollbar
    text_area = Text(nueva_ventana, wrap='word')
    scrollbar = Scrollbar(nueva_ventana, command=text_area.yview)
    text_area.configure(yscrollcommand=scrollbar.set)

    # Configurar la posición de los widgets
    text_area.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')

    # Insertar datos en el Text widget
    text_area.config(state="normal")  # Cambiar el estado a normal para permitir la edición
    text_area.delete(1.0, END)  # Borrar el contenido previo
    for token in tokens:
        token_type, token_value, token_lineno, token_lexpos = token
        text_area.insert(INSERT, f'Tipo: {token_type}, Valor: {token_value}, Ren: {token_lineno}, Col: {token_lexpos}\n')  # Insertar cada token en una nueva línea
    text_area.config(state="disabled")  # Volver a deshabilitar la edición

'''
def mostrarAnalisisLexico(tokens):
    scrollAnalisis.config(state="normal")  # Cambiar el estado a normal para permitir la edición
    scrollAnalisis.delete(1.0, END)  # Borrar el contenido previo
    for token in tokens:
        token_type, token_value, token_lineno, token_lexpos = token
        scrollAnalisis.insert(INSERT, f'Tipo: {token_type}, Valor: {token_value}, Ren: {token_lineno}, Col: {token_lexpos}\n')  # Insertar cada token en una nueva línea
    scrollAnalisis.config(state="disabled")  # Volver a deshabilitar la edición
'''
'''
 token_type, token_value, token_lineno, token_lexpos = token
 scrollAnalisis.insert(INSERT, f'Tipo: {token_type}, Valor: {token_value}, Ren: {token_lineno}, Col: {token_lexpos}\n')
'''

def AbrirArchivos():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Text files", "*.txt"), ("Ht files", "*.ht"), ("all files", "*.*")))
    if filename != '':
        if filename.endswith((".txt", ".ht")):  # Pa' abrir archivos .txt o .ht
            root.title("Compilador Python   code: " + filename)
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read()
                scroll_text_widget.clear_scroll_text()
                scroll_text_widget.set_text(content)
                scroll_text_widget._update_line_numbers()
        else:
            mb.showerror("Error", "El archivo seleccionado no es de tipo .txt o .ht")


def GuardarComo():
    filename = filedialog.asksaveasfilename(initialdir="/", title="Guardar como",
                                            filetypes=(("txt files", "*.txt"), ("ht files", "*.ht"), ("todos los archivos", "*.*")))
    if filename != '':
        if filename.endswith((".txt", ".ht")):  # Pa' guardar como .txt o .ht
            root.title("Compilador Python   code: " + filename)
            with open(filename, "w", encoding="utf-8") as file:
                file.write(scroll_text_widget.get_text())
            messagebox.showinfo("Información", "Los datos fueron guardados en el archivo.")
        else:
            messagebox.showerror("Error", "El archivo debe contener la extension .txt o .ht")


def Guardar():
    filename = root.title()
    if filename.startswith("Compilador Python   code: "):
        filename = filename.lstrip("Compilador Python   code: ")
        if filename.endswith((".txt", ".ht")):                  # Pa' guardar como .txt o .ht
            with open(filename, "w", encoding="utf-8") as file:
                file.write(scroll_text_widget.get_text())
            messagebox.showinfo("Información", "Los cambios fueron guardados en el archivo.")
        else:
            GuardarComo()
    else:
        GuardarComo()


def NuevoArchivo():
    root.title("Compilador Python")
    scroll_text_widget.clear_scroll_text()

def AunSinAgregar():
    mb.showerror("Atención","Aun no se agrega esta funcion al compilador.")

def analisisLexico():
    cadena = scroll_text_widget.get_text()
    if len(cadena) > 0:
        lexer.input(cadena)
        a_tok = []
        for tok in lexer:
            a_tok.append((tok.type, tok.value, tok.lineno, tok.lexpos))
        mostrarAnalisisLexico2(a_tok)
    else:
        mb.showwarning("ERROR", "Debes escribir código")

#a_tok.append((tok.type, tok.value, tok.lineno, tok.lexpos))
#Configuracion del entorno
root = Tk()
root.resizable(False,False) # Con esto denegamos que se ajuste el tamaño de la ventana de largo y ancho
root.geometry("924x596") #definimos las dimesiones de la ventana
root.title("Compilador Python") #Titulo de la ventana

#En este punto realizamos una serie de calculos para que cada que se ejecute este codigo
#la pantalla del compilador inicie desde el centro de la pantalla
wtotal = root.winfo_screenwidth()
htotal = root.winfo_screenheight()
wventana = 930
hventana = 599
pwidth = round(wtotal/2-wventana/2)
pheight = round(htotal/2-hventana/2)
root.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))

#Mandamos a llamar a ScrollTextWithLine y definimos donde estará
scroll_text_widget = ScrollTextWithLineNumbers(root)
scroll_text_widget.grid(row=1,column=0,padx=10,pady=10)

#Este codigo medio funciona
def mostrarResultados(tokens,reserved,lexer):
    sintactico_window = Toplevel(root)
    sintactico_window.title("Analisis Sintactico")
    sintactico_window.geometry("450x450")

    sintactico_scroll = Scrollbar(sintactico_window)
    sintactico_scroll.pack(side=RIGHT, fill=Y)

    sintactico_text = Text(sintactico_window, yscrollcommand=sintactico_scroll.set)
    sintactico_text.pack(expand=True, fill=BOTH)

    for asin in tokens,reserved,lexer:
        idMethod,tipo,idParam,bloque = asin
        # Por ejemplo:token_type, token_value, = token
        sintactico_text.insert(INSERT, f" {idMethod} {tipo} {idParam} {{\n{bloque}\n}}")
        # sintactico_text.insert(INSERT, f"{token_type} {token_value}\n")
        pass  # Esto es solo para mostrar un marcador de posición
    sintactico_scroll.config(command=sintactico_text.yview)

#Las siguientes lineas comentadas son para que se den un ejemplo de como funcionan las funciones
#de get_Text y set_Text
'''
def obtenerText():
    text = scroll_text_widget.get_text()
    msg=messagebox.showinfo("Contenido",text+"")

boton = Button(root,text="Hello", command=obtenerText)
boton.grid(row=0,column=0)'''

'''
def PonerText():
    new_text = "Este es el nuevo texto que quiero colocar en el ScrolledText."
    scroll_text_widget.set_text(new_text)

boton = Button(root,text="Hello", command=PonerText)
boton.grid(row=0,column=0)'''

#Este scroll es el que muestra mensajes o errores que surjan durante los analisis
scrollAnalisis = ScrolledText(root, width=100,  height=8, font = ("Console", 11), state="disabled")
scrollAnalisis.grid(row=2,column=0,padx=10,pady=10)

def cambiar_tamaño_letra(size):
    scroll_text_widget.text_widget.config(font=("Console", size))

#El menu bar donde estarán funciones de manejo de archivos y otras cosas
menubar = Menu(root, background='#ff8000', foreground='black', activebackground='white', activeforeground='black')  
file = Menu(menubar, tearoff=1)  
file.add_command(label="New",command=NuevoArchivo)  
file.add_command(label="Open",command=AbrirArchivos)  
file.add_command(label="Save", command=Guardar)  
file.add_command(label="Save as", command=GuardarComo)    
file.add_separator()  
file.add_command(label="Exit", command=root.quit)  
menubar.add_cascade(label="File", menu=file)  

analisis = Menu(menubar, tearoff=0)   
analisis.add_command(label="Lexico",command=analisisLexico)  
analisis.add_command(label="Sintactico", command=analisisSintactico)  
menubar.add_cascade(label="Analizar", menu=analisis)  

tablas = Menu(menubar,tearoff=0)
tablas.add_command(label="Estatica")
tablas.add_command(label="Dinamica")
menubar.add_cascade(label="Tablas", menu=tablas)

# Menú para seleccionar el tamaño de la fuente No jala bien de momento
font_menu = Menu(menubar, tearoff=0)
font_menu.add_command(label="10", command=lambda: cambiar_tamaño_letra(10))
font_menu.add_command(label="12", command=lambda: cambiar_tamaño_letra(12))
font_menu.add_command(label="14", command=lambda: cambiar_tamaño_letra(14))
font_menu.add_command(label="16", command=lambda: cambiar_tamaño_letra(16))
font_menu.add_command(label="18", command=lambda: cambiar_tamaño_letra(18))
font_menu.add_command(label="20", command=lambda: cambiar_tamaño_letra(20))

menubar.add_cascade(label="Tamaño de la letra xd", menu=font_menu)

root.config(menu=menubar)
root.mainloop()