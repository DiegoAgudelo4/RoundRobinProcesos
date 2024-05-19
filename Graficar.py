import matplotlib.pyplot as plt
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
import os
#abrir pdf
import subprocess

# Función para generar la tabla de procesos
def generar_tabla_procesos(procesos):
    # Determinar el número máximo de columnas basado en la lista_es más larga
    max_columnas_es = max(len(proceso['lista_es']) for proceso in procesos)

    # Construir los encabezados dinámicamente
    encabezados = ["Nombre", "Tiempo de \nLlegada (MS)", "Quantum \nNecesario (Q)"]
    for i in range(max_columnas_es):
        encabezados.append(f"Gasta en \nE/S(Q)")
        encabezados.append(f"NCPU \n(Q)")

    # Construir los datos de la tabla
    data = [encabezados]
    for proceso in procesos:
        fila = [proceso['nombre'], proceso['tiempo_llegada'], proceso['quantum_necesario']]
        for es in proceso['lista_es']:
            fila.append(es['es'])
            fila.append(es['es_necesaria'])
        # Rellenar con espacios vacíos si es necesario para mantener la estructura de la tabla
        fila += [""] * (max_columnas_es - len(proceso['lista_es'])) * 2
        data.append(fila)

    return data


# Función para generar colores dinámicamente
def generar_colores(procesos):
    colores = {}
    colores['Intercambio'] = 'green'
    otros_procesos = set(proceso['proceso'] for proceso in procesos) - {'Intercambio'}
    num_otros_procesos = len(otros_procesos)
    colores_aleatorios = plt.cm.tab10(np.linspace(0, 1, num_otros_procesos))
    for proceso, color in zip(otros_procesos, colores_aleatorios):
        colores[proceso] = color
    return colores

# Función para dibujar el diagrama de Gantt y guardarlo como imagen
def draw_gantt_chart(data, cantProcesos):
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Añadir más espacio arriba y abajo del gráfico
    fig.subplots_adjust(top=0.8, bottom=cantProcesos / 10)
    
    ax.set_title('Diagrama de Gantt: Procesos en funcion del tiempo')
    ax.set_xlabel('Tiempo (ms)')
    ax.set_ylabel('Proceso')
    
    data.sort(key=lambda x: (x['proceso'] != 'Intercambio', x['inicio']))
    
    colores_procesos = generar_colores(data)
    
    procesos = {}
    for tarea in data:
        if tarea['proceso'] in procesos:
            procesos[tarea['proceso']].append((tarea['inicio'], tarea['fin']))
        else:
            procesos[tarea['proceso']] = [(tarea['inicio'], tarea['fin'])]
    
    for i, (proceso, tareas) in enumerate(procesos.items()):
        color = colores_procesos[proceso]
        for inicio, fin in tareas:
            ax.barh(y=i, width=fin - inicio, left=inicio, height=0.5, align='center', label=proceso, color=color)
            ax.text((inicio + fin) / 2, i, f'{inicio}-{fin}', va='center', ha='center', color='black', fontsize=8)
    
    ax.set_yticks(range(len(procesos)))
    ax.set_yticklabels([proceso for proceso in procesos.keys()])
    
    # Guardar el gráfico como una imagen
    img_filename = "gantt_chart.png"
    plt.savefig(img_filename)
    plt.close()

    return img_filename

# Función para crear el PDF
def draw_gantt_chart_pdf(data, cantProcesos, texto_superior, texto_inferior,procesos, output_filename):
    # Crear el documento PDF
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    story = []

    # Estilo para el texto
    styles = getSampleStyleSheet()
    estilo_superior = styles['Normal']

    tabla_procesos = Table(generar_tabla_procesos(procesos))
    tabla_procesos.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                        ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    story.append(tabla_procesos)
    story.append(Spacer(1, 12))

    # Agregar texto superior
    story.append(Paragraph(texto_superior, estilo_superior))
    story.append(Spacer(1, 12))

    # Generar y agregar la imagen del gráfico
    img_filename = draw_gantt_chart(data, cantProcesos)
    story.append(Image(img_filename, width=480, height=240))
    story.append(Spacer(1, 12))

    # Agregar texto inferior
    story.append(Paragraph(texto_inferior, estilo_superior))

    # Construir el PDF
    doc.build(story)

    # Eliminar la imagen después de usarla
    os.remove(img_filename)
    subprocess.Popen([output_filename], shell=True)
"""
# Ejemplo de uso
data = [
    {'proceso': 'A', 'inicio': 0, 'fin': 5},
    {'proceso': 'B', 'inicio': 3, 'fin': 10},
    {'proceso': 'Intercambio', 'inicio': 1, 'fin': 2},
    {'proceso': 'Intercambio', 'inicio': 6, 'fin': 8},
]
texto_superior = "Texto superior: Hola mundo"
texto_inferior = "Texto inferior: Adiós mundo"
output_filename = "gantt_chart.pdf"
cantProcesos = 4

draw_gantt_chart_pdf(data, cantProcesos, texto_superior, texto_inferior, output_filename)
"""