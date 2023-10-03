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

#valida fecha para que siempre tenga 2 digitos
def valida_fecha(fecha: str) -> str :
    fecha_valida: str
    if len(fecha) == 1 :
        fecha_valida = "0" + fecha
    else :
        fecha_valida = fecha
    return fecha_valida

#Extraer el año, mes y día de una fecha, las valida y crear el nombre de una
#carpeta backup para agregar a un diccionario
def crea_nombres_carpeta_segun_el_dia(fecha_de_hoy) :
    diccionario_por_dia = {} 
    dia_variante = 1

    while dia_variante <= 3 :
        fecha: datetime = fecha_de_hoy - timedelta(days=dia_variante)
        mes = str(fecha.month)
        dia = str(fecha.day)
        año_valido = str(fecha.year)
        mes_valido = valida_fecha(mes)
        dia_valido = valida_fecha(dia)
        nombre_carpeta_nueva = año_valido + mes_valido + dia_valido
        
        diccionario_por_dia[dia_variante] = nombre_carpeta_nueva

        dia_variante += 1

    return diccionario_por_dia

#devuelve el par [dia, mes] con n dias de antiguedad respecto a la fecha de hoy
def n_dias_antes(n, fecha_de_hoy) -> list:
    dia_mes = []

    fecha: datetime = fecha_de_hoy - timedelta(days=n)
    mes = str(fecha.month)
    dia = str(fecha.day)
    mes_valido = valida_fecha(mes)
    dia_valido = valida_fecha(dia)

    dia_mes.append(dia_valido)
    dia_mes.append(mes_valido)

    return dia_mes


#selecciona solo los archivos que tienen la fecha de ayer y los agrega a una lista
def selecciona_archivos_con_fecha_de(lista_de_listas, par_dia_mes) -> list :
    lista_bkp_recientes = []
    dia = par_dia_mes[0]
    mes = par_dia_mes[1]

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

#Declaro las variables de las rutas de las carpetas de orgine y destino,
#nombre de la carpeta a crear y lista de todos los archivos bakcup

nombre_carpeta_correspondiente = crea_nombres_carpeta_segun_el_dia(fecha_actual)

ruta_sql = "G:\\bkp_automatico_test\\"
ruta_admtar = "\\\\10.0.1.14\\ÚltimoAdmTar\\"
lista_todos_archivos_bak = os.listdir(ruta_sql)
carpetas_bkp_existentes = os.listdir(ruta_admtar)
#para test: lista_todos_archivos_bak = ['cwSGCore_backup_2023_09_27_231501_6803011.bak', 'master_backup_2023_09_27_231501_6803011.bak', 'cwSGCore_backup_2023_09_28_231501_6803011.bak', 'master_backup_2023_10_02_231501_6803011.bak', 'cwSGCore_backup_2023_09_29_231501_6803011.bak', 'master_backup_2023_09_29_231501_6803011.bak', 'cwSGCore_backup_2023_09_30_231501_6803011.bak', 'master_backup_2023_09_30_231501_6803011.bak', 'cwSGCore_backup_2023_10_01_231501_6803011.bak', 'master_backup_2023_10_01_231501_6803011.bak']


archivos_filtrados_por_base = filtra_por_base_de_datos(lista_todos_archivos_bak) 

archivos_a_copiar_1_dia_antes = selecciona_archivos_con_fecha_de(archivos_filtrados_por_base, n_dias_antes(1, fecha_actual))
archivos_a_copiar_2_dias_antes = selecciona_archivos_con_fecha_de(archivos_filtrados_por_base, n_dias_antes(2, fecha_actual))
archivos_a_copiar_3_dias_antes = selecciona_archivos_con_fecha_de(archivos_filtrados_por_base, n_dias_antes(3, fecha_actual))

pega_archivos_faltantes(ruta_sql, ruta_admtar, archivos_a_copiar_1_dia_antes, carpetas_bkp_existentes, nombre_carpeta_correspondiente[1])
pega_archivos_faltantes(ruta_sql, ruta_admtar, archivos_a_copiar_2_dias_antes, carpetas_bkp_existentes, nombre_carpeta_correspondiente[2])
pega_archivos_faltantes(ruta_sql, ruta_admtar, archivos_a_copiar_3_dias_antes, carpetas_bkp_existentes, nombre_carpeta_correspondiente[3])

