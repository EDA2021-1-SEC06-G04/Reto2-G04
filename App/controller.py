﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv
from DISClib.ADT import list as lt
from datetime import datetime
import time
import tracemalloc

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

#funciones de time y tracemalloc:
def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory

# Inicialización del Catálogo de videos
def initCatalog(estructura, metodo_colision, factor_carga):
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog(estructura, metodo_colision, factor_carga)
    return catalog

# Funciones para la carga de datos
def loadData(catalog, size_videos: int):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    #medir tiempo y memoria:
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
#   -----------------------------------  
    loadCategorias(catalog)
    loadVideos(catalog, size_videos)
    
    #loadPaises(catalog)
#   -----------------------------------  

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return delta_time, delta_memory


def loadVideos(catalog, size_videos: int):
    """
    Carga los videos del archivo.
    """
    videosfile = cf.data_dir + 'videos-large.csv'
    input_file = csv.DictReader(open(videosfile, encoding='utf-8'))
    contador_datos = 0
    for video_leido in input_file:
        video_agregar = {}
        info_deseada_strings = ['title','video_id', 'category_id', 'channel_title', \
             'country', 'publish_time']
        info_numerica = ['views', 'likes', 'dislikes']
        for info in info_deseada_strings:
            video_agregar[info] = video_leido[info]
        for info in info_numerica:
            video_agregar[info] = int(video_leido[info])
        
        video_agregar['category_id'] = int(video_agregar['category_id'])

        video_agregar['trending_date'] = datetime.strptime(video_leido['trending_date'], '%y.%d.%m').date()
        
        video_agregar['tags'] = lt.newList('ARRAY_LIST')
        for tag in video_leido['tags'].split('"|"'):
            tag.replace('"','')
            lt.addLast(video_agregar['tags'], tag)

        model.addVideo(catalog, video_agregar)
        contador_datos += 1
        if contador_datos >= size_videos:
            break


def loadCategorias(catalog):
    """
    Carga las categorias del archivo.
    """
    catsfile = cf.data_dir + 'category-id.csv'
    input_file = csv.DictReader(open(catsfile, encoding='utf-8'), delimiter = '\t')
    for cate_leida in input_file:
        cate_agregar = {}
        info_deseada = ['id','name']
        for info in info_deseada:
            cate_agregar[info] = (str(cate_leida[info]).lower()).replace(' ', '')
        model.addCategoria(catalog, cate_agregar)
        
#antiguo:
def loadPaises(catalog):
    """
    Carga los distintos paises del archivo.
    """
    model.loadPaises(catalog)




# Funciones de ordenamiento
#antiguo, 
def sortVideos(tad_lista, metodo:str, orden:str):
    """
    Ordena los videos por views
    metodo se refiere al algoritmo de sorting
    orden se refiere al criterio por el que se ordena: revisar las opciones en model.sortVideos
    """
    model.sortList(tad_lista, metodo, orden)

# Funciones de consulta sobre el catálogo
#antiguo:
def subListVideos(catalog, pos, number):
    return model.subListVideos(catalog, pos, number)

#nuevo
def subListVideos2(lista, pos, number):
    return model.subListVideos2(lista, pos, number)
#antiguo:
def subListVideos_porPais(tad_lista, pais):
    pais = pais.lower()
    return model.subListVideos_porPais(tad_lista, pais)

'''def subListVideos_porCategoria(tad_lista, categoria_id):
    categoria_id = str(categoria_id)
    return model.subListVideos_porCategoria(tad_lista, categoria_id)'''

#antiguo:
def getMostViewed(catalog, number, pais, categoria_id, metodo="merge"):
    """
    Primero organiza todos los videos por vistas 
    Retorna una sublista de los videos mas vistos
    """
    sublista = subListVideos(catalog, 1, number)

    sublista = subListVideos_porCategoria(sublista, categoria_id)

    sublista = subListVideos_porPais(sublista, pais)

    sublista = ObtenerVideosDistintos(sublista)
    
    sortVideos(sublista, metodo, "vistas")

    return sublista
#antiguo:
def primer_video(catalog):
    return model.primer_video(catalog)
#antiguo:
def pais_presente(catalog, pais):
    return model.pais_presente(catalog, pais)
#nuevo
def categoria_presente(catalog, categoria):
    categoria = str(categoria).lower()
    return model.categoria_presente(catalog, categoria)

#nuevo 
def VideoTrendingPais(catalog, pais):
    video = model.VideoTrendingPais(catalog, pais)
    return video

#antiguo:
def ObtenerVideosDistintos(tad_lista):
    """
    Carga los distintos videos del archivo.
    """
    sortVideos(tad_lista, 'merge', "video_id")
    return model.ObtenerVideosDistintos(tad_lista)

#antiguo:
def getMostTrending(catalog, pais):
    sublista = subListVideos_porPais(catalog['videos'], pais)
    sublista = ObtenerVideosDistintos(sublista)
    return model.getMaxReps(sublista)
#antiguo:
def subListVideos_porTag(tad_lista, tag:str):
    return model.subListVideos_porTag(tad_lista, tag)
#antiguo:
def getMostLiked_porPaisyTags(catalog, number, pais, tag, metodo="merge"):

    sublista = subListVideos(catalog, 1, number)

    sublista = subListVideos_porPais(sublista, pais)

    sublista = subListVideos_porTag(sublista, tag)

    sublista = ObtenerVideosDistintos(sublista)  

    sortVideos(sublista, metodo, "likes")  

    return sublista

#nuevo:
def subListVideos_porCategoria(catalog, categoria_id):
#medir el tiempo y memoria:
    
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

#-------------------------------------------
    videos = model.subListVideos_porCategoria(catalog, categoria_id)
#-------------------------------------------
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return videos, delta_time, delta_memory


#nuevo:
def getMostLiked_porPaisCategoria(catalog, categoria_id, pais):

    #medir tiempo y memoria:
    
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

#-------------------------------------------
    videos = model.subListVideos_porPais_Categoria(catalog, pais, categoria_id)
    videos = ObtenerVideosDistintos(videos)
    sortVideos(videos, 'merge', 'likes')
#-------------------------------------------
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return videos, delta_time, delta_memory
#quedó perfecta