import matplotlib.pyplot as plt
#calculos numericos
import numpy as np
#back



# Función para generar colores dinámicamente
def generar_colores(procesos):
    colores = {}
    # Asignar color verde al proceso 'I'
    colores['I'] = 'green'
    # Generar colores aleatorios para los otros procesos
    otros_procesos = set(proceso['proceso'] for proceso in procesos) - {'I'}
    num_otros_procesos = len(otros_procesos)
    colores_aleatorios = plt.cm.tab10(np.linspace(0, 1, num_otros_procesos))
    for proceso, color in zip(otros_procesos, colores_aleatorios):
        colores[proceso] = color
    return colores

# Función para dibujar el diagrama de Gantt
def draw_gantt_chart(data):
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Configuración del gráfico
    ax.set_title('Diagrama de Gantt')
    ax.set_xlabel('Tiempo')
    ax.set_ylabel('Proceso')
    #ax.grid(True, linewidth=1.5)  # Cambia el ancho de la cuadrícula aquí
    
    # Ordenar los datos para mostrar primero el proceso 'I'
    data.sort(key=lambda x: (x['proceso'] != 'I', x['inicio']))
    
    # Generar colores dinámicamente
    colores_procesos = generar_colores(data)
    
    # Agrupar los procesos para mostrarlos en la misma línea horizontal
    procesos = {}
    for tarea in data:
        if tarea['proceso'] in procesos:
            procesos[tarea['proceso']].append((tarea['inicio'], tarea['fin']))
        else:
            procesos[tarea['proceso']] = [(tarea['inicio'], tarea['fin'])]
    
    # Dibujo de las barras de proceso agrupadas
    for i, (proceso, tareas) in enumerate(procesos.items()):
        color = colores_procesos[proceso]
        for inicio, fin in tareas:
            ax.barh(y=i, width=fin - inicio, left=inicio, height=0.5, align='center', label=proceso, color=color)
            ax.text((inicio + fin) / 2, i, f'{inicio}-{fin}', va='center', ha='center', color='black', fontsize=8)
    
    # Etiquetas de los procesos
    ax.set_yticks(range(len(procesos)))
    ax.set_yticklabels([proceso for proceso in procesos.keys()])
    
    plt.show()
    