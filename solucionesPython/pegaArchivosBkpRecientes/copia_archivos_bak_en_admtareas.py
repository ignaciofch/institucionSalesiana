import os
from datetime import datetime, timedelta
import shutil

def filtra_por_base_de_datos(lista_archivos) :
    lista_archivos_Core_solo= []   
    lista_archivos_Model_solo = []
    lista_archivos_CoreModel = []
    lista_archivos_DONBOSCO = []
    lista_archivos_master = []
    lista_archivos_model = []
    lista_archivos_msdb = []

    lista_de_listas_filtradas = []

    for archivo in lista_archivos:
        if es_Core_solo(archivo) :
            lista_archivos_Core_solo.append(archivo)
        elif es_Model_solo(archivo) :
            lista_archivos_Model_solo.append(archivo)
        elif es_CoreModel(archivo) :
            lista_archivos_CoreModel.append(archivo)
        elif es_DONBOSCO(archivo) :
            lista_archivos_DONBOSCO.append(archivo)
        elif es_master(archivo) :
            lista_archivos_master.append(archivo)
        elif es_model(archivo) :
            lista_archivos_model.append(archivo)
        elif es_msdb(archivo) :
            lista_archivos_msdb.append(archivo)
       
    lista_de_listas_filtradas.append(lista_archivos_Core_solo)
    lista_de_listas_filtradas.append(lista_archivos_Model_solo)
    lista_de_listas_filtradas.append(lista_archivos_CoreModel)
    lista_de_listas_filtradas.append(lista_archivos_DONBOSCO)
    lista_de_listas_filtradas.append(lista_archivos_master)
    lista_de_listas_filtradas.append(lista_archivos_model)
    lista_de_listas_filtradas.append(lista_archivos_msdb) 

    return lista_de_listas_filtradas

def es_Core_solo(nombre_archivo) :
    return ("cwSGCore_") in nombre_archivo

def es_Model_solo(nombre_archivo) :
    return ("cwSGModel_") in nombre_archivo

def es_CoreModel(nombre_archivo) :
    return ("cwSGCoreModel_") in nombre_archivo

def es_DONBOSCO(nombre_archivo) :
    return ("DONBOSCO_") in nombre_archivo

def es_master(nombre_archivo) :
    return ("master_") in nombre_archivo

def es_model(nombre_archivo) :
    return ("model_") in nombre_archivo

def es_msdb(nombre_archivo) :
    return ("msdb_") in nombre_archivo

#valida fecha para crear el nombre de la nueva carpeta de la forma: "AAAMMDD"
def valida_fecha(fecha: str) -> str :
    fecha_valida: str
    if len(fecha) == 1 :
        fecha_valida = "0" + fecha
    else :
        fecha_valida = fecha
    return fecha_valida

#selecciona solo los archivos que tienen la fecha de ayer y los agrega a una lista
def selecciona_archivos_con_fecha_de_ayer(lista_de_listas, dia, mes) -> list :
    lista_bkp_recientes = []

    for lista_de_una_base in lista_de_listas:
        lista_de_una_base: list

        for archivo in lista_de_una_base:
                
                if (("_" + dia + "_") in archivo) and (("_" + mes + "_") in archivo) :
                    lista_bkp_recientes.append(archivo) 

    return lista_bkp_recientes

#verifica si hay archivos para hacer backup y los pega en la carpeta de AdmTar
def pega_archivos_faltantes(ruta_original, ruta_destino, archivos_a_copiar, carpetas_existentes, nombre_carpeta):
    if not(nombre_carpeta in carpetas_existentes):
        os.mkdir(ruta_destino + nombre_carpeta)     
        for archivo in archivos_a_copiar:
            shutil.copy(ruta_original + archivo, ruta_destino + nombre_carpeta + "\\") 

# Obtener la fecha de ayer
fecha_actual = datetime.now()
fecha_ayer = fecha_actual - timedelta(days=1)

# Extraer el año, mes y día de la fecha de ayer y validarlas
mes = str(fecha_ayer.month)
dia = str(fecha_ayer.day)
año_valido = str(fecha_ayer.year)
mes_valido = valida_fecha(mes)
dia_valido = valida_fecha(dia)

#Declaro las variables de las rutas de las carpetas de orgine y destino,
#nombre de la carpeta a crear y lista de todos los archivos bakcup

ruta_sql = "G:\\bkp_automatico_test\\"
ruta_admtar = "\\\\10.0.1.14\\ÚltimoAdmTar\\"
nombre_carpeta_nueva = año_valido + mes_valido + dia_valido
lista_todos_archivos_bak = os.listdir(ruta_sql)
carpetas_bkp_existentes = os.listdir(ruta_admtar)

archivos_filtrados_por_base = filtra_por_base_de_datos(lista_todos_archivos_bak) 

archivos_a_copiar = selecciona_archivos_con_fecha_de_ayer(archivos_filtrados_por_base, dia_valido, mes_valido)

pega_archivos_faltantes(ruta_sql, ruta_admtar, archivos_a_copiar, carpetas_bkp_existentes, nombre_carpeta_nueva)
