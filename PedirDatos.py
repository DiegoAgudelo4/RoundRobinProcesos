import tkinter as tk

class Proceso:
    def __init__(self, nombre="Nuevo", tiempo_llegada=0, ncpu=0, es=None):
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
        self.tamanoQ_Entry = tk.Entry(textvariable = self.tamanoQ, width="10",name="noDel_5")
        self.tamanoQ_Entry.grid(row=0, column=4, padx=10, pady=10)

        self.tamanoI_label = tk.Label(text="Tam.Intercambio", bg="#FFEEDD",name="noDel_6")
        self.tamanoI_label.grid(row=0, column=5, padx=10, pady=10)

        self.tamanoI= tk.StringVar()
        self.tamanoI_Entry = tk.Entry(textvariable=self.tamanoI, width="10",name="noDel_7")
        self.tamanoI_Entry.grid(row=0, column=6, padx=10, pady=10)
        
        self.procesos = []
        self.columnas = ["Acción", "Nombre de proceso", "Tiempo de llegada", "NCPU"]
        self.crear_encabezado()
        

        
    def crear_encabezado(self):
        for i, columna in enumerate(self.columnas):
            lbl = tk.Label(self.root, text=columna)
            lbl.grid(row=1, column=i, padx=10, pady=10)
    
    def agregar_proceso(self):
        self.guardar_cambios_todos()
        proceso = Proceso()
        self.procesos.append(proceso)
        self.mostrar_procesos()
    
    def agregar_es(self):
        self.guardar_cambios_todos()
        for i in range(len(self.procesos)):
            self.procesos[i].es.append({"ie": 0, "ie_necesaria": 0})
        self.columnas.extend(["E/S", "NCPU"])
        self.crear_encabezado()
        self.mostrar_procesos()
    
    def guardar_cambios(self, row, column, variable):
        new_value = variable.get()
        if column == 1:  # Nombre de proceso
            self.procesos[row].nombre = new_value
        elif column == 2:  # Tiempo de llegada
            try:
                self.procesos[row].tiempo_llegada = int(new_value)
            except ValueError:
                # Si el valor no es un entero, mantener el valor anterior
                pass
        elif column == 3:  # NCPU
            try:
                self.procesos[row].ncpu = int(new_value)
            except ValueError:
                # Si el valor no es un entero, mantener el valor anterior
                pass
        elif column % 2 == 0:  # Entradas de E/S
            try:
                self.procesos[row].es[(column - 4) // 2]["ie"] = int(new_value)
            except ValueError:
                # Si el valor no es un entero, mantener el valor anterior
                pass
        else:  # Entradas de NCPU en E/S
            try:
                self.procesos[row].es[(column - 5) // 2]["ie_necesaria"] = int(new_value)
            except ValueError:
                # Si el valor no es un entero, mantener el valor anterior
                pass

    def guardar_cambios_todos(self):
        for i, proceso in enumerate(self.procesos):
            for j in range(1, len(self.columnas)):
                widget = self.root.grid_slaves(row=i+2, column=j)[0]
                if isinstance(widget, tk.Entry):
                    self.guardar_cambios(i, j, widget)

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
            nombre_entry.bind("<FocusOut>", lambda event, row=i, column=1, variable=nombre_var: self.guardar_cambios( row, column, variable))
            
            tiempo_var = tk.StringVar(value=str(proceso.tiempo_llegada))
            tiempo_entry = tk.Entry(self.root, textvariable=tiempo_var)
            tiempo_entry.grid(row=i+2, column=2, padx=10, pady=10)
            tiempo_entry.bind("<FocusOut>", lambda event, row=i, column=2, variable=tiempo_var: self.guardar_cambios(row, column, variable))
            
            ncpu_var = tk.StringVar(value=str(proceso.ncpu))
            ncpu_entry = tk.Entry(self.root, textvariable=ncpu_var)
            ncpu_entry.grid(row=i+2, column=3, padx=10, pady=10)
            ncpu_entry.bind("<FocusOut>", lambda event, row=i, column=3, variable=ncpu_var: self.guardar_cambios(row, column, variable))
            
            if proceso.es:
                for j in range(len(proceso.es)):
                    es_var = tk.StringVar(value=str(proceso.es[j]["ie"]))
                    es_entry = tk.Entry(self.root, textvariable=es_var)
                    es_entry.grid(row=i+2, column=4+j*2, padx=10, pady=10)
                    es_entry.bind("<FocusOut>", lambda event, row=i, column=4+j*2, variable=es_var: self.guardar_cambios( row, column, variable))
                    
                    ncpu_es_var = tk.StringVar(value=str(proceso.es[j]["ie_necesaria"]))
                    ncpu_es_entry = tk.Entry(self.root, textvariable=ncpu_es_var)
                    ncpu_es_entry.grid(row=i+2, column=5+j*2, padx=10, pady=10)
                    ncpu_es_entry.bind("<FocusOut>", lambda event, row=i, column=5+j*2, variable=ncpu_es_var: self.guardar_cambios( row, column, variable))

    def ejecutar(self):
        global procesos
        self.guardar_cambios_todos()
        procesos = {}

        # Asigna los valores a las variables dentro de tu función o método
        
        #multiplicamos cada valor por el tamaño del quantum para
        #enviar todo en ms

        tamanoQ = int(self.tamanoQ.get())

        for proceso in self.procesos:
            proceso.tiempo_llegada = int(proceso.tiempo_llegada)
            proceso.ncpu = int(proceso.ncpu) * tamanoQ
            for ie in proceso.es:
                ie['ie'] = int(ie['ie']) * tamanoQ
                ie['ie_necesaria'] = int(ie['ie_necesaria']) * tamanoQ

        #quantum_necesario = ncpu 
        #es= lista_ie
        
        #print(procesos)
        procesos['tamanoQ'] = tamanoQ
        procesos['tamanoI'] = self.tamanoI.get()
        procesos['procesos'] = self.procesos
        self.root.quit()

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
            'lista_ie': proceso.es
        }
        procesosFin.append(proceso_dict)
    print(procesosFin)
    return procesos
