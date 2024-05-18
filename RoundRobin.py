from builtins import print
from collections import deque
#graficar 

#modulo para graficar
from Graficar import draw_gantt_chart

cola_fifo = deque()
procesos = []
tiempos_espera=[]

class Proceso:
    def __init__(self, nombre, tiempo_llegada, quantum_necesario):
        self.nombre = nombre
        self.tiempo_llegada = tiempo_llegada
        self.quantum_necesario = quantum_necesario

def mostrarCola():
    print("Elementos de la cola:")
    for elemento in cola_fifo:
        print(elemento.nombre+" Tiempo entrada: "+str(elemento.tiempo_llegada)+" Quantum necesario "+ str(elemento.quantum_necesario))
        
def agregarFinalDeCola(nombre,tiempo_llegada,quantum_necesario):
    global proceso
    global cola_fifo
    proceso = Proceso(nombre=nombre, tiempo_llegada=tiempo_llegada,
                      quantum_necesario=quantum_necesario)
    cola_fifo.append(proceso)

# Definir un conjunto para almacenar nombres ya agregados a la cola

def verificarES(tiempo):
    global tiempos_espera
    n= len(procesos)
    for i in range(n):
        if procesos[i]['quantum_necesario'] == 0:
            if procesos[i]['nombre'] in  nombres_en_cola:
                nombres_en_cola.remove(procesos[i]['nombre'])
            m = len(procesos[i]['lista_es'])
            for j in range(m):

                llegada = procesos[i]['lista_es'][j]['es']
                if llegada != 0:
                    nuevaLlegada=llegada+tiempo

                    tiempos_espera.append(procesos[i]['nombre']+":"+str(tiempo) + "+" + str(procesos[i]['lista_es'][j]['es']) + "=" +
                                          str(nuevaLlegada))

                    procesos[i]['lista_es'][j]['es']=0
                    qnecesario = procesos[i]['lista_es'][j]['es_necesaria']
                    procesos[i]['lista_es'][j]['es_necesaria']=0
                    #print(procesos)
                    actualizaProceso(procesos[i]['nombre'], nuevaLlegada, qnecesario)
                    break
nombres_en_cola = set()
def verificarProcesos(tiempo):
    global nombres_en_cola
    global procesos
    n= len(procesos)
    for i in range(n):
        print(procesos[i]['nombre']+": "+str(procesos[i]['tiempo_llegada']) + "<= " +str(tiempo)+ " Q nec" +str(procesos[i]['quantum_necesario']))

        if  procesos[i]['tiempo_llegada'] <= tiempo and procesos[i]['quantum_necesario'] !=0:
            # Verificar si el nombre ya está en la cola
            #para que no se ingresen repetidos
            if procesos[i]['nombre'] not in nombres_en_cola:
                print(procesos[i]['nombre'] + ": agregada a la cola")
                agregarFinalDeCola(procesos[i]['nombre'], procesos[i]['tiempo_llegada'],procesos[i]['quantum_necesario'])

                # Agregar el nombre a la lista de nombres en la cola
                nombres_en_cola.add(procesos[i]['nombre'])

def actualizaProceso(nombre,llegada, quantum_necesario):
    global procesos
    # Buscar el proceso por nombre
    proceso_encontrado = None
    for proceso_info in procesos:
        if proceso_info['nombre'] == nombre:
            proceso_encontrado = proceso_info
            break

    # Verificar si se encontró el proceso
    if proceso_encontrado:
        # Actualizar quantum_necesario
        proceso_encontrado['tiempo_llegada'] = llegada
        proceso_encontrado['quantum_necesario'] = quantum_necesario   # Reemplaza "nuevo_valor_quantum" con el valor que desees

        # Imprimir para verificar la actualización
        print(f"Proceso {nombre} actualizado. entrada: {llegada} Nuevo valor de quantum_necesario: {proceso_encontrado['quantum_necesario']}")
    #else:
    #    print(f"No se encontró un proceso con el nombre {nombre}")

def round_robin(procesos, quantum, tiempo_intcambio):
    global cola_fifo
    global tiempos_espera
    #inicializamos las variables
    tiempo = 0
    diagrama_gantt = []
    cola_listos = []
    tiempos_espera = []
    #para controlar el salto de linea de la cola de listos
    #sólo es estetica
    co=0
    #extraemos los nombres de los procesos y los guardamos en en un arreglo nuevo
    #inicializamos el tiempo final en 0| tmp = tiempo
   
    tmpProcesos = [{'nombre': proceso['nombre'],'tmpLlegada':proceso['tiempo_llegada'],'tmpInicial': 'Null', 'tmpFinal': 0, 'restaES': 0} for proceso in procesos]
    
    #restaES: suma todos las ES para calcular el tiempo de vuelta
    for i in range(len(procesos)):
        tmpProcesos[i]['restaES']+= procesos[i]['tiempo_llegada']
        m = len(procesos[i]['lista_es'])
        for j in range(m):
            tmpProcesos[i]['restaES']+=procesos[i]['lista_es'][j]['es']

    #llenamos la cola con el primer elemento
    verificarProcesos(tiempo)
    """
    falta añadir que cuando no haya nadie en la cola el tiempo siga avanzando, porque en este caso el
    ciclo se rompe si no hay nadie en la cola y puede que no haya nadie pero llegue más tarde (Tiempo inactivo)
    """
    while len(cola_fifo) > 0:

        print('*********** Tiempo *********** ->>>' +str(tiempo))
        # Extraer el primer proceso de la cola, osea el primero que entró
        proceso_actual = cola_fifo.popleft()

        #verificamos que en efecto el tiempo de llegada es menor que el tiempo del sistema
        if proceso_actual.tiempo_llegada <= tiempo and proceso_actual.quantum_necesario != 0:
            #mostramos por cosola la validacion
            print(proceso_actual.nombre + '- ' + str(proceso_actual.tiempo_llegada) + ' Q necesario: ' + str(
                proceso_actual.quantum_necesario))

            #recibimos el tiempo restante del proceso actual
            tiempo_restante=proceso_actual.quantum_necesario

            #verificamos si hay procesos que no necesiten quantum (0) y además
            #tiene entradas y salidas E/S con necesidad de quantum
            verificarES(tiempo)

            indice_proceso = next(
                (i for i, proceso in enumerate(tmpProcesos) if proceso['nombre'] == proceso_actual.nombre), None)
            if tiempo_restante == procesos[indice_proceso]['quantum_necesario'] and tmpProcesos[indice_proceso][
                'tmpInicial'] == 'Null':
                tmpProcesos[indice_proceso]['tmpInicial'] = tiempo

            #verificamos que el tiempo restante sea mayor que el quantum
            #para que no quede negativo el tiempo restante
            if tiempo_restante>quantum:
                tiempo += quantum
                tiempo_restante -= quantum
                #antes de agretgar el proceso de nuevo al final de la cola
                #verificamos si hay procesos esperando
                verificarProcesos(tiempo)
                print(proceso_actual.nombre + ": agregada a la cola")
                #se agrega al final de la cola el procesos con la necesidad de quantum restada
                agregarFinalDeCola(proceso_actual.nombre, proceso_actual.tiempo_llegada, tiempo_restante)
            else:
                #si entra acá significa que ese proceso ya no necesita quantum
                #se le suma al tiempo el tiempo restante para que no se pierda
                tiempo += tiempo_restante
                tiempo_restante = 0
                #se agrega el tiempo final cuando terminó el proceso
                indice_proceso = next(
                    (i for i, proceso in enumerate(tmpProcesos) if proceso['nombre'] == proceso_actual.nombre), None)
                tmpProcesos[indice_proceso]['tmpFinal']=tiempo
                print(f"{proceso_actual.nombre}  termina en  {tiempo}")
                #verificamos si hay procesos esperando
                verificarProcesos(tiempo)
            #actualizamos los procesos en arreglo de procesos
            #se hace porque la funcion verificarProcesos(tiempo) se vasa en ese arreglo
            actualizaProceso(proceso_actual.nombre, proceso_actual.tiempo_llegada, tiempo_restante)

            #print("Resta: "+procesado.nombre+"->"+str(procesado.quantum_necesario))

            #guardamos el proceso en un arreglo con el rango de tiempo en el que estuvo
            diagrama_gantt.append({'proceso': proceso_actual.nombre, 'inicio': tiempo - quantum, 'fin': tiempo})

            #guardamos la cola, la que ya pasó por la cola de procesos y fue procesada (en un string)
            cola_listos.append("|" + str(proceso_actual.quantum_necesario) + "|" + proceso_actual.nombre)
            if co ==10:
                cola_listos.append("\n")
                co=0
            co+=1

            #con esta funcion mostramos la cola en cada iteracion
            mostrarCola()

            #mostramos cuando fué el intercambio
            print('*********** intercambio ****** ->>>' + str(tiempo)+"+"+str(tiempo_intcambio))
            
            #verificarProcesos(tiempo)
            #se actualiza el tiempo sumandole el tiempo de intercambio
            tiempo += tiempo_intcambio
            #se agrega al diagrama de grant para que se observe el intercambio
            diagrama_gantt.append({'proceso': 'I', 'inicio': tiempo - tiempo_intcambio, 'fin': tiempo})
    diagrama_gantt.pop()

    # Mostrar cola de listos
    print("\nCola de Listos:")
    print(" -> ".join(cola_listos))

    # Mostrar diagrama de Gantt
    print("\n************************************************Diagrama de Gantt:************************************************\n Inicio - Fin : Proceso")
    i=0
    for entrada in diagrama_gantt:
        if i == 10:
            print("\n")
            i=0
        print(f"|{entrada['inicio']}-{entrada['proceso']}-{entrada['fin']}", end='')
        i+=1
    print("\n************************************************ Fin diagrama ************************************************")
    # Mostrar tiempos de espera
    print("\nTiempos de Espera:")
    print(tiempos_espera)
    print("\n******************** tiempo de vuelta ********************")

    #calculamos el tiempo de vuelta
    tmpVuelta=[]
    tmpVueltaTotal=0
    n=len(tmpProcesos)
    for i in range(n):
        tmpVuelta.append(tmpProcesos[i]['tmpFinal']-tmpProcesos[i]['restaES'])
        tmpVueltaTotal+=tmpVuelta[i]
        print(" Tiempo de vuelta del Proceso ["+tmpProcesos[i]['nombre']+"]: "+ str(tmpVuelta[i]))
    print("\n******************** calculo de entrada y salida ********************")
    #calculamos el tiempo de espera
    tmpEspera=[]
    tmpEsperaTotal=0
    for i in range(n):
        tmpEspera.append(tmpProcesos[i]['tmpInicial']-tmpProcesos[i]['tmpLlegada'])
        tmpEsperaTotal+=tmpEspera[i]
        print(" Tiempo de espera promedio del Proceso [" + tmpProcesos[i]['nombre'] + "]: " + str(tmpEspera[i]))
    print("\n******************** tiempo de vuelta promedio ********************")
    print(tmpVueltaTotal/n)
    print("\n******************** tiempo de espera promedio ********************")
    print(tmpEsperaTotal/n)
    draw_gantt_chart(diagrama_gantt)
    

# Solicitar entrada al usuario para cada proceso
def obtener_ie():
    ie = int(input('Ingrese E/S: '))
    ie_necesaria = int(input('Ingrese el quantum Necesario E/S: '))
    return {'es': ie, 'es_necesaria': ie_necesaria}

def obtener_entrada_usuario(info):
    global procesos
    
    
    print(info['tamanoQ'])
    quantum=int(info['tamanoQ']) #ms
    tiempo_intcambio= int(info['tamanoI'])
    
    procesos = []
    for proceso in info['procesos']:
        proceso_dict = {
            'nombre': proceso.nombre,
            'tiempo_llegada': proceso.tiempo_llegada,
            'quantum_necesario': proceso.ncpu,
            'lista_es': proceso.es
        }
        procesos.append(proceso_dict)
    
    print(procesos)
    
    round_robin(procesos, quantum, tiempo_intcambio)
    

# Ejecutar el programa
#obtener_entrada_usuario()
