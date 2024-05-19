#graficos de python
import tkinter as tk
#procesar 
from RoundRobin import obtener_entrada_usuario
puedeContinuar=True
cantProcesos=0
class Proceso:
    def __init__(self, nombre="nuevo", tiempo_llegada=0, ncpu=0, es=None):
        self.nombre = nombre
        self.tiempo_llegada = tiempo_llegada
        self.ncpu = ncpu
        self.es = es if es is not None else []

class ProcesoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ingresar procesos")
        self.btn_agregar_proceso = tk.Button(root, text="Agregar proceso", command=self.agregar_proceso , name="noDel_1")
        self.btn_agregar_proceso.grid(row=0, column=0, padx=10, pady=10)
        
        self.btn_agregar_es = tk.Button(root, text="Agregar E/S", command=self.agregar_es, name="noDel_2")
        self.btn_agregar_es.grid(row=0, column=1, padx=10, pady=10)
        
        self.btn_ejecutar = tk.Button(root, text="Ejecutar", command=self.ejecutar, name="noDel_3")
        self.btn_ejecutar.grid(row=0, column=2, padx=10, pady=10)

        self.tamanoQ_label = tk.Label(text="Tam.Quantum", bg="#FFEEDD", name="noDel_4")
        self.tamanoQ_label.grid(row=0, column=3, padx=10, pady=10)

        self.tamanoQ= tk.StringVar()
        self.tamanoQ.set("50")
        self.tamanoQ_Entry = tk.Entry(textvariable = self.tamanoQ, width="10",name="noDel_5")
        self.tamanoQ_Entry.bind("<FocusIn>", lambda event, widget=self.tamanoQ_Entry: widget.select_range(0, 'end'))
        #self.tamanoQ_Entry.bind("<KeyRelease>", lambda variable=self.tamanoQ: self.verificarEntryQuantum(variable))
        self.tamanoQ_Entry.grid(row=0, column=4, padx=10, pady=10)

        self.tamanoI_label = tk.Label(text="Tam.Intercambio", bg="#FFEEDD",name="noDel_6")
        self.tamanoI_label.grid(row=0, column=5, padx=10, pady=10)

        self.tamanoI= tk.StringVar()
        self.tamanoI.set("10")
        self.tamanoI_Entry = tk.Entry(textvariable=self.tamanoI, width="10",name="noDel_7")
        self.tamanoI_Entry.bind("<FocusIn>", lambda event, widget=self.tamanoI_Entry: widget.select_range(0, 'end'))
        #self.tamanoI_Entry("<KeyRelease>", lambda event, variable=self.tamanoI: self.verificarEntryQuantum(variable))
        self.tamanoI_Entry.grid(row=0, column=6, padx=10, pady=10)
        
        self.procesos = []
        self.columnas = ["Acción", "Nombre de proceso", "Tiempo de llegada", "NCPU"]
        self.crear_encabezado()
        
    
        
    def crear_encabezado(self):
        for i, columna in enumerate(self.columnas):
            lbl = tk.Label(self.root, text=columna)
            lbl.grid(row=1, column=i, padx=10, pady=10)
    
    def agregar_proceso(self):
        global cantProcesos
        proceso = Proceso(nombre=f"P{cantProcesos}")
        cantProcesos+=1
        self.procesos.append(proceso)
        self.mostrar_procesos()
    
    def agregar_es(self):
        for i in range(len(self.procesos)
        ):
            self.procesos[i].es.append({"es": 0, "es_necesaria": 0})
        self.columnas.extend(["E/S", "NCPU"])
        self.crear_encabezado()
        self.mostrar_procesos()
    
    def guardar_cambios(self, row, column, variable):
        global puedeContinuar
        #print(f"Guardando Cambios... {row} : {column}")
        new_value = variable.get()
        #print(f"Nuevo valor {new_value}")
       
        if column == 1:  # Nombre de proceso
            self.procesos[row].nombre = new_value
        elif column == 2:  # Tiempo de llegada
            try:
                if new_value=="":
                    self.procesos[row].tiempo_llegada=0
                    variable.set(self.procesos[row].tiempo_llegada)
                elif self.procesos[row].tiempo_llegada==0 and new_value.endswith('0'):
                    self.procesos[row].tiempo_llegada=int(new_value[:-1])
                else:

                    self.procesos[row].tiempo_llegada = int(new_value)
                    puedeContinuar = int(new_value)>=0
                    if not puedeContinuar:
                        return
                    
                variable.set(str(self.procesos[row].tiempo_llegada))
            except ValueError:
                # Si el valor no es un entero, mantener el valor anterior
                variable.set(self.procesos[row].tiempo_llegada)
                puedeContinuar=True
                return
            
        elif column == 3:  # NCPU 
            try:
                if new_value=="":
                    self.procesos[row].ncpu=0
                    variable.set(self.procesos[row].ncpu)
                    puedeContinuar=True
                elif self.procesos[row].ncpu==0 and new_value.endswith('0'):
                    self.procesos[row].ncpu=int(new_value[:-1])
                    puedeContinuar=True
                else:
                    self.procesos[row].ncpu = int(new_value)
                    puedeContinuar = int(new_value)>=0
                    if not puedeContinuar:
                        return
                    
                variable.set(str(self.procesos[row].ncpu))
            except ValueError:
                # Si el valor no es un entero, mantener el valor anterior
                variable.set(self.procesos[row].ncpu)
                puedeContinuar=True
                return
            
        elif column % 2 == 0:  # Entradas de E/S
            try:
                if new_value=="":
                    self.procesos[row].es[(column - 4) // 2]["es"]=0
                    variable.set(self.procesos[row].es[(column - 4) // 2]["es"])
                    puedeContinuar=True
                elif self.procesos[row].es[(column - 4) // 2]["es"]==0 and new_value.endswith('0'):
                    self.procesos[row].es[(column - 4) // 2]["es"]=int(new_value[:-1])
                    puedeContinuar=True
                else:
                    self.procesos[row].es[(column - 4) // 2]["es"] = int(new_value)
                    puedeContinuar = int(new_value)>=0
                    if not puedeContinuar:
                        return
                    
                variable.set(str(self.procesos[row].es[(column - 4) // 2]["es"]))
            except ValueError:
                # Si el valor no es un entero, mantener el valor anterior
                variable.set(self.procesos[row].es[(column - 4) // 2]["es"])
                puedeContinuar=True
                return
        else:  # Entradas de NCPU en E/S
            try:
                if new_value=="":
                    self.procesos[row].es[(column - 5) // 2]["es_necesaria"]=0
                    variable.set(self.procesos[row].es[(column - 5) // 2]["es_necesaria"])
                    puedeContinuar=True
                elif self.procesos[row].es[(column - 5) // 2]["es_necesaria"]==0 and new_value.endswith('0'):
                    self.procesos[row].es[(column - 5) // 2]["es_necesaria"]=int(new_value[:-1])
                    puedeContinuar=True
                else:
                    self.procesos[row].es[(column - 5) // 2]["es_necesaria"] = int(new_value)
                    puedeContinuar = int(new_value)>=0
                    if not puedeContinuar:
                        return
                    
                variable.set(str(self.procesos[row].es[(column - 5) // 2]["es_necesaria"]))
            except ValueError:
                # Si el valor no es un entero, mantener el valor anterior
                variable.set(self.procesos[row].es[(column - 5) // 2]["es_necesaria"])
                puedeContinuar=True
                return
        #print(f"Puede continuar finalizando cambios [{puedeContinuar}]")
        
    def eliminar_fila(self, row):
        del self.procesos[row]
        self.mostrar_procesos()
    
    def mostrar_procesos(self):
        # Limpiar solo los widgets relacionados con los procesos
        for widget in self.root.winfo_children():
            if widget.winfo_class() not in ["Label"] and "noDel" not in widget.winfo_name() :
                widget.destroy()
        
        self.crear_encabezado()
        for i, proceso in enumerate(self.procesos):
            btn_eliminar = tk.Button(self.root, text="Eliminar", command=lambda row=i: self.eliminar_fila(row))
            btn_eliminar.grid(row=i+2, column=0, padx=10, pady=10)
            
            nombre_var = tk.StringVar(value=proceso.nombre)
            nombre_entry = tk.Entry(self.root, textvariable=nombre_var)
            nombre_entry.grid(row=i+2, column=1, padx=10, pady=10)
            nombre_entry.bind("<FocusIn>", lambda event, widget=nombre_entry: widget.select_range(0, 'end'))
            nombre_entry.bind("<KeyRelease>", lambda event, row=i, column=1, variable=nombre_var: self.guardar_cambios( row, column, variable))
            
            tiempo_var = tk.StringVar(value=str(proceso.tiempo_llegada))
            tiempo_entry = tk.Entry(self.root, textvariable=tiempo_var)
            tiempo_entry.grid(row=i+2, column=2, padx=10, pady=10)
            tiempo_entry.bind("<FocusIn>", lambda event, widget=tiempo_entry: widget.select_range(0, 'end'))
            tiempo_entry.bind("<KeyRelease>", lambda event, row=i, column=2, variable=tiempo_var: self.guardar_cambios(row, column, variable))
            
            ncpu_var = tk.StringVar(value=str(proceso.ncpu))
            ncpu_entry = tk.Entry(self.root, textvariable=ncpu_var)
            ncpu_entry.grid(row=i+2, column=3, padx=10, pady=10)
            ncpu_entry.bind("<FocusIn>", lambda event, widget=ncpu_entry: widget.select_range(0, 'end'))
            ncpu_entry.bind("<KeyRelease>", lambda event, row=i, column=3, variable=ncpu_var: self.guardar_cambios(row, column, variable))
            
            if proceso.es:
                for j in range(len(proceso.es)):
                    es_var = tk.StringVar(value=str(proceso.es[j]["es"]))
                    es_entry = tk.Entry(self.root, textvariable=es_var)
                    es_entry.grid(row=i+2, column=4+j*2, padx=10, pady=10)
                    es_entry.bind("<FocusIn>", lambda event, widget=es_entry: widget.select_range(0, 'end'))
                    es_entry.bind("<KeyRelease>", lambda event, row=i, column=4+j*2, variable=es_var: self.guardar_cambios( row, column, variable))
                    
                    ncpu_es_var = tk.StringVar(value=str(proceso.es[j]["es_necesaria"]))
                    ncpu_es_entry = tk.Entry(self.root, textvariable=ncpu_es_var)
                    ncpu_es_entry.grid(row=i+2, column=5+j*2, padx=10, pady=10)
                    ncpu_es_entry.bind("<FocusIn>", lambda event, widget=ncpu_es_entry: widget.select_range(0, 'end'))
                    ncpu_es_entry.bind("<KeyRelease>", lambda event, row=i, column=5+j*2, variable=ncpu_es_var: self.guardar_cambios( row, column, variable))

    def ejecutar(self):
        global puedeContinuar
        global procesos
        #print(f"Puede continuar al ejecutar {puedeContinuar}")
        if puedeContinuar and len(self.procesos) >0:
            procesos = {}

            # Asigna los valores a las variables dentro de tu función o método
            
            
            try:
                tamanoQ = int(self.tamanoQ.get())
                tamanoI= int( self.tamanoI.get())
                if tamanoQ<=0:
                    print("El quantum debe ser mayor que [0]")
                    return
                if tamanoI<=0:
                    print("El intercambio debe ser mayor que [0]")
                    return
            except ValueError:
                print("Caracter invalido")
                return           
            #multiplicamos cada valor por el tamaño del quantum para
            #enviar todo en ms
            for proceso in self.procesos:
                proceso.tiempo_llegada = int(proceso.tiempo_llegada)
                proceso.ncpu = int(proceso.ncpu) * tamanoQ
                for es in proceso.es:
                    es['es'] = int(es['es']) * tamanoQ
                    es['es_necesaria'] = int(es['es_necesaria']) * tamanoQ

            #print(procesos)
            procesos['tamanoQ'] = tamanoQ
            procesos['tamanoI'] = tamanoI
            procesos['procesos'] = self.procesos

            #oculta la ventana
            self.root.withdraw()
            #se sale del programa, entrega la informacion y continua con el round robin
            self.root.quit()
        elif puedeContinuar:
            print("No se ingresaron procesos")
        else:
            print("Existe un cáracter invalido")

def ejecutar():
    
    root = tk.Tk()
    app = ProcesoApp(root)
    root.mainloop()
    print(procesos)
    procesosFin = []
    for proceso in procesos['procesos']:
        proceso_dict = {
            'nombre': proceso.nombre,
            'tiempo_llegada': proceso.tiempo_llegada,
            'quantum_necesario': proceso.ncpu,
            'lista_es': proceso.es
        }
        procesosFin.append(proceso_dict)
    print(procesosFin)
    obtener_entrada_usuario(procesos)

ejecutar()