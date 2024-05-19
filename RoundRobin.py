from builtins import print
from collections import deque

#modulo para graficar
from Graficar import draw_gantt_chart_pdf

#
import copy


#Cola de listos
cola_fifo = deque() 
#Lista de procesos
procesos = []
#lista de procesos original
procesos_original=[]
#Lista de los tiempos de espera
tiempos_espera=[]

#se crea un conjunto vacío para verificar qué procesos están o no en cola
nombres_en_cola = set()

#objeto que representa un objeto
class Proceso:
    def __init__(self, nombre, tiempo_llegada=0, quantum_necesario=0):
        self.nombre = nombre
        self.tiempo_llegada = tiempo_llegada
        self.quantum_necesario = quantum_necesario

#funcion para mostrar los objetos que hay en la cola fifo
def mostrarCola():
    print("Elementos de la cola:")
    for elemento in cola_fifo:
        print(elemento.nombre+" Tiempo entrada: "+str(elemento.tiempo_llegada)+" Quantum necesario "+ str(elemento.quantum_necesario))

#funcion para agregar un proceso al final de la cola_fifo (cola de listos)
def agregarFinalDeCola(nombre,tiempo_llegada,quantum_necesario):
    global proceso
    global cola_fifo
    proceso = Proceso(nombre=nombre, tiempo_llegada=tiempo_llegada,
                      quantum_necesario=quantum_necesario)
    cola_fifo.append(proceso)

#funcion para verificar que un proceso tiene E/S cuando el quantum necesario es 0
def verificarES(tiempo):
    global tiempos_espera
    global cantTerminados
    n= len(procesos)
    for i in range(n):
        if procesos[i]['quantum_necesario'] == 0:
            if procesos[i]['nombre'] in  nombres_en_cola:
                nombres_en_cola.remove(procesos[i]['nombre'])
            m = len(procesos[i]['lista_es'])
            #si tiene entradas y salidas se calcula la nueva entrada y la nueva NCPU
            if m>0:
                for j in range(m):
                    
                    llegada = procesos[i]['lista_es'][j]['es'] 
                    if llegada != 0:
                        nuevaLlegada=llegada+tiempo

                        tiempos_espera.append(procesos[i]['nombre']+":"+str(tiempo) + "+" + str(procesos[i]['lista_es'][j]['es']) + "=" +
                                            str(nuevaLlegada))

                        procesos[i]['lista_es'][j]['es']=0
                        qnecesario = procesos[i]['lista_es'][j]['es_necesaria']#1
                        procesos[i]['lista_es'][j]['es_necesaria']=0
                        #print(procesos)
                        actualizaProceso(procesos[i]['nombre'], nuevaLlegada, qnecesario)
                        break

#funcion que permite verificar si un proceso ya puede entrar o no
#segun su tiempo_llegada
def verificarProcesos(tiempo):
    global nombres_en_cola
    global procesos

    #los procesos se deben ordenar en funcion al tiempo de llegada
    procesos = sorted(procesos, key=lambda x: x['tiempo_llegada'])
    
    for i in range(len(procesos)):
        #print(procesos[i]['nombre']+": "+str(procesos[i]['tiempo_llegada']) + "<= " +str(tiempo)+ " Q nec" +str(procesos[i]['quantum_necesario']))
        #verifica que el tiempo de llegada sea menor que el tiempo, si sí, significa que ya puede ingresar
        if  procesos[i]['tiempo_llegada'] <= tiempo and procesos[i]['quantum_necesario'] !=0:
            # Verificar si el nombre ya está en la cola
            #para que no se ingresen repetidos
            if procesos[i]['nombre'] not in nombres_en_cola:
                #print(procesos[i]['nombre'] + ": agregada a la cola")

                agregarFinalDeCola(procesos[i]['nombre'], procesos[i]['tiempo_llegada'],procesos[i]['quantum_necesario'])

                # Agregar el nombre a la lista de nombres en la cola
                nombres_en_cola.add(procesos[i]['nombre'])

#se recibe un nuevo quantum_necesario y/o una nueva llegada
#esta informacion se actualiza en la lista de procesos 

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

#inicio del ciclo principal
def round_robin(procesos, quantum, tiempo_intcambio):
    global cola_fifo
    global tiempos_espera
    global procesos_original

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

    #mientras no todos los procesos tengan necesidad de quantum igual a cero
    while not all(proceso['quantum_necesario']==0 for proceso in procesos):

        #si hay alguien en la cola
        if len(cola_fifo) >0:
            #print('*********** Tiempo *********** ->>>' +str(tiempo))

            # Extraer el primer proceso de la cola, osea el primero que entró
            proceso_actual = cola_fifo.popleft()

            #verificamos que en efecto el tiempo de llegada es menor que el tiempo del sistema
            if proceso_actual.tiempo_llegada <= tiempo and proceso_actual.quantum_necesario != 0:

                #mostramos por cosola la validacion
                #print(proceso_actual.nombre + '- ' + str(proceso_actual.tiempo_llegada) + ' Q necesario: ' + str(
                #    proceso_actual.quantum_necesario))

                #recibimos el tiempo restante del proceso actual
                tiempo_restante=proceso_actual.quantum_necesario 

                #verificamos si hay procesos que no necesiten quantum (0) y además
                #tiene entradas y salidas E/S con necesidad de quantum
                verificarES(tiempo)
                
                #cuando inicia el proceso actual, se actualiza el tmpInicial de ese proceso
                #solo se actualiza la primera vez que entra el proceso
                indice_proceso = next(
                    (i for i, proceso in enumerate(tmpProcesos) if proceso['nombre'] == proceso_actual.nombre), None)
                #doble verificacion
                if tiempo_restante == procesos[indice_proceso]['quantum_necesario'] and tmpProcesos[indice_proceso][
                    'tmpInicial'] == 'Null':
                    tmpProcesos[indice_proceso]['tmpInicial'] = tiempo

                #verificamos que el tiempo restante sea mayor que el quantum
                #para que no quede negativo el tiempo restante
                if tiempo_restante>quantum:
                    tiempo += quantum
                    tiempo_restante -= quantum

                    #antes de agregar el proceso de nuevo al final de la cola
                    #verificamos si hay procesos esperando
                    verificarProcesos(tiempo) 

                    #print(proceso_actual.nombre + ": agregada a la cola")

                    #se agrega al final de la cola el procesos con la necesidad de quantum restada
                    agregarFinalDeCola(proceso_actual.nombre, proceso_actual.tiempo_llegada, tiempo_restante)
                
                else:
                    #si entra acá significa que ese proceso ya no necesita quantum [muere]
                    #se le suma al tiempo, el tiempo restante para que no se pierda
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
                #se hace porque la funcion verificarProcesos(tiempo) se vasa en ese arreglo [procesos]
                actualizaProceso(proceso_actual.nombre, proceso_actual.tiempo_llegada, tiempo_restante)

                #print("Resta: "+procesado.nombre+"->"+str(procesado.quantum_necesario))

                #guardamos el proceso en un arreglo con el rango de tiempo en el que estuvo
                diagrama_gantt.append({'proceso': proceso_actual.nombre, 'inicio': tiempo - quantum, 'fin': tiempo})

                #guardamos la cola, la que ya pasó por la cola de procesos y fue procesada (en un string)
                cola_listos.append("""
                                    <table border="1" align="center">
                                        <tr>
                                            <td align="center">{}</td>
                                        </tr>
                                        <tr>
                                            <td align="center">{}</td>
                                        </tr>
                                    </table>
                                    """.format(proceso_actual.nombre, proceso_actual.quantum_necesario/quantum))

                #if co ==10:
                #    cola_listos.append("\n")
                #    co=0
                #co+=1

                #con esta funcion mostramos la cola en cada iteracion
                mostrarCola()

                #mostramos cuando fué el intercambio
                #print('*********** intercambio ****** ->>>' + str(tiempo)+"+"+str(tiempo_intcambio))
                
                #verificarProcesos(tiempo)

                #se actualiza el tiempo sumandole el tiempo de intercambio
                tiempo += tiempo_intcambio

                #se agrega al diagrama de grant para que se observe el intercambio
                diagrama_gantt.append({'proceso': 'Intercambio', 'inicio': tiempo - tiempo_intcambio, 'fin': tiempo})

                verificarES(tiempo)
        else:
            #verificamos si llegó alguien en el tiempo
            verificarES(tiempo)
            verificarProcesos(tiempo)

            #sumamos quantum 
            tiempo+=quantum
            diagrama_gantt.append({'proceso': 'Inactivo', 'inicio': tiempo - quantum, 'fin': tiempo})

            #sumamos intercambio
            tiempo+=tiempo_intcambio
            diagrama_gantt.append({'proceso': 'Intercambio', 'inicio': tiempo - tiempo_intcambio, 'fin': tiempo})

            #verificamos si llegó alguien despúes de hacer la sumatoria
            verificarES(tiempo)
            verificarProcesos(tiempo)
            
            mostrarCola() 
            #print("*********** inactivo ****** ")
    if len(diagrama_gantt)!=0:
        diagrama_gantt.pop()

    # Mostrar cola de listos
    #print("\nCola de Listos:")
    #print(" -> ".join(cola_listos))
    StringColaListos="<html> <h3>Cola de listos</h3><br/>"
    StringColaListos+=" -> ".join(cola_listos)

    # Mostrar diagrama de Gantt
    #print("\n************************************************Diagrama de Gantt:************************************************\n Inicio - Fin : Proceso")
    #i=0
    #for entrada in diagrama_gantt:
    #    if i == 10:
    #        print("\n")
    #        i=0
    #    print(f"|{entrada['inicio']}-{entrada['proceso']}-{entrada['fin']}", end='')
    #    i+=1
    #print("\n************************************************ Fin diagrama ************************************************")
    # Mostrar tiempos de espera
    #print("\nCola de Espera (E/S):")
    #print(tiempos_espera)
    #print("\n******************** tiempo de vuelta ********************")
    StringColaListos+=f"<br/> <br/>Cola de Espera (E/S):<br/>{"<br/>".join(tiempos_espera)}"

    #calculamos el tiempo de vuelta
    tmpVuelta=[]
    tmpVueltaTotal=0
    StringTiempoVuelta="Tiempo de vuelta por cada proceso<br/>"
    n=len(tmpProcesos)
    for i in range(n):
        #tiempo de vuelta es igual a: [tiempo en el que termina sin intercambio] menos [tiempo menos ]
        tmpVuelta.append(tmpProcesos[i]['tmpFinal']-tmpProcesos[i]['restaES'])
        tmpVueltaTotal+=tmpVuelta[i]
        #print(" Tiempo de vuelta del Proceso ["+tmpProcesos[i]['nombre']+"]: "+ str(tmpVuelta[i]))
        StringTiempoVuelta+="Tiempo de vuelta del Proceso ["+tmpProcesos[i]['nombre']+"]: "+ str(tmpVuelta[i])+"<br/>"

    #print("\n******************** calculo de entrada y salida ********************")
    #calculamos el tiempo de espera
    tmpEspera=[]
    tmpEsperaTotal=0
    StringTiempoVuelta+="<br/><h3>Tiempo de espera por cada proceso</h3><br/>"
    for i in range(n):
        tmpEspera.append(int(tmpProcesos[i]['tmpInicial'] if tmpProcesos[i]['tmpInicial'] != 'Null' else 0)-int(tmpProcesos[i]['tmpLlegada']))
        tmpEsperaTotal+=tmpEspera[i]
        #print(" Tiempo de espera promedio del Proceso [" + tmpProcesos[i]['nombre'] + "]: " + str(tmpEspera[i]))
        StringTiempoVuelta+=" Tiempo de espera promedio del Proceso [" + tmpProcesos[i]['nombre'] + "]: " + str(tmpEspera[i]) +"<br/>"
    #print("\n******************** tiempo de vuelta promedio ********************")
    if n!=0:
        print(tmpVueltaTotal/n)
        StringTiempoVuelta+=f"<br/><h3>Tiempo medio de vuelta</h3><br/> {tmpVueltaTotal} / {n} = {tmpVueltaTotal/n} <br/>"
    else:
        print("0")

    #print("\n******************** tiempo de espera promedio ********************")
    if n!=0:
        print(tmpEsperaTotal/n)
        StringTiempoVuelta+=f"<br/><h3>Tiempo medio de espera</h3><br/> {tmpEsperaTotal} / {n} = {tmpVueltaTotal/n}<br/>"
    else:
        print("0")
    StringColaListos+="</html>"
    draw_gantt_chart_pdf(diagrama_gantt,len(procesos),StringColaListos,StringTiempoVuelta,procesos_original,"gantt_chart.pdf")
    

# Solicitar entrada al usuario para cada proceso
def obtener_ie():
    ie = int(input('Ingrese E/S: '))
    ie_necesaria = int(input('Ingrese el quantum Necesario E/S: '))
    return {'es': ie, 'es_necesaria': ie_necesaria}

def obtener_entrada_usuario(info):
    global procesos
    global procesos_original

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
    procesos_original = copy.deepcopy(procesos)
    for proceso in procesos_original:
        proceso['tiempo_llegada'] = proceso['tiempo_llegada']  # No se necesita cambiar, simplemente se asigna el mismo valor
        proceso['quantum_necesario'] = proceso['quantum_necesario'] / quantum
        for es in proceso['lista_es']:
            es['es'] = es['es'] / quantum
            es['es_necesaria'] = es['es_necesaria'] / quantum
    round_robin(procesos, quantum, tiempo_intcambio)
    

# Ejecutar el programa
#obtener_entrada_usuario()
