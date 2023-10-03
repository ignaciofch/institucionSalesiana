import os
from datetime import datetime, timedelta

#Este programa. al ejecutarse diariamente, verifica que siempre haya
# a lo sumo 7 carpetas backup de los ultimos 7 dias.

#Si la carpeta no esta vacia, elimina sus arcivos y luego la carpeta.


################################ FUNCIONES #################################

#elimina la carpeta, y si contiene archivos, tambien los elimina
def eliminar_carpeta_y_sus_archivos(carpeta, directorio):
    dir = os.listdir(directorio + carpeta)
    if not(dir == []):
        for archivo in dir:
            os.remove(directorio + carpeta + '/' + archivo) 
    os.rmdir(directorio + carpeta)

#crea una lista con la estructura de los nombres que tendrian las carpetas con mas de 7 dias de antiguedad
def crear_lista_de_nombres_de_carpetas_antiguas(fecha) -> list :
    lista_carpetas_antiguas = []
    i = 8

    while i < 27 :
        fecha_para_crear_nombre: datetime = fecha - timedelta(days=i)
        mes = str(fecha_para_crear_nombre.month)
        dia = str(fecha_para_crear_nombre.day)
        año_valido = str(fecha_para_crear_nombre.year)
        mes_valido = valida_fecha(mes)
        dia_valido = valida_fecha(dia)
        nombre_carpeta_creada = año_valido + mes_valido + dia_valido
        lista_carpetas_antiguas.append(nombre_carpeta_creada)
        i += 1
    
    return lista_carpetas_antiguas

#valida fecha para crear el nombre de la nueva carpeta de la forma: "AAAMMDD"
def valida_fecha(fecha: str) -> str :
    fecha_valida: str
    if len(fecha) == 1 :
        fecha_valida = "0" + fecha
    else :
        fecha_valida = fecha
    return fecha_valida

#Si existe la carpeta de Syncthing, la elimina de la lista
def verifica_y_eliminar_carpeta_syncthing(carpeta_syncthing, lista_carpetas: list):
    if carpeta_syncthing in lista_carpetas :
        lista_carpetas.remove(carpeta_syncthing)    

#Elimina cada carpeta que tenga mas de 7 dias de antiguedad
def elimina_careptas_bkp_viejas(lista_carpetas: list, directorio, fecha):

    carpeta_syncthing = ".stfolder"
    verifica_y_eliminar_carpeta_syncthing(carpeta_syncthing, lista_carpetas_bkp)
    lista_carpetas.sort()

    lista_carpetas_antiguas = crear_lista_de_nombres_de_carpetas_antiguas(fecha)

    for carpeta_bkp in lista_carpetas :

        if carpeta_bkp in lista_carpetas_antiguas :
            eliminar_carpeta_y_sus_archivos(carpeta_bkp, directorio)
            print("Se elimino la carpeta " + carpeta_bkp)


################################################################

# Obtener la fecha de ayer, la ruta y la lista de carpetas backup
fecha_actual = datetime.now()
directorio_raiz = "/media/nacho/bkp_sql/ultimoBackup/"
lista_carpetas_bkp = os.listdir(directorio_raiz)

#Entra a la funcion con un lista que ira variando, ruta del backup y un copa de la lista pero esta se mantendrá fija
elimina_careptas_bkp_viejas(lista_carpetas_bkp, directorio_raiz, fecha_actual)

