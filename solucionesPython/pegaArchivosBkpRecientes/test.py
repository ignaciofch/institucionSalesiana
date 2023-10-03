import datetime

# Define la fecha inicial
fecha_inicial = datetime.date(2023, 9, 27)

# Número de archivos que deseas generar
numero_de_archivos = 5

# Directorio donde se guardarán los archivos (ajusta esto a tu ubicación)
directorio = "/ruta/del/directorio"

lista = []
# Genera y guarda los archivos con fechas distintas
for i in range(numero_de_archivos):
    fecha = fecha_inicial + datetime.timedelta(days=i)
    nombre_archivo = f"cwSGCore_backup_{fecha.strftime('%Y_%m_%d')}_231501_6803011.bak"
    nombre_archivo2 = f"master_backup_{fecha.strftime('%Y_%m_%d')}_231501_6803011.bak"
    # Guarda el archivo o imprime la ruta
    # Aquí puedes usar código para crear o copiar el archivo según tus necesidades
    # Por ejemplo, para crear archivos vacíos:
    lista.append(nombre_archivo)
    lista.append(nombre_archivo2)


print(lista)