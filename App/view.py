﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import time
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf




'''
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
'''
def initCatalog(estructura, metodo_colision, factor_carga):
    """
    Inicializa el catalogo de libros
    """
    return controller.initCatalog(estructura, metodo_colision, factor_carga)


def loadData(catalog, size_videos: int, estructura='ARRAY_LIST'):
    """
    Carga los libros en la estructura de datos
    """
    return controller.loadData(catalog, size_videos)


def printVideosTrendingPais(video,num_dias, pais_R2):
    """
    Imprime el video más trending por el país pasado por parámetro
    """
    print("El video que más días ha sido trending para el país "+pais_R2+" es:")
    print('Título: '+ video['title'])
    print('Título de canal: '+video['channel_title']) 
    print('País: ' + video['country'])
    print('Número de días tendencia: '+ str(num_dias))


def printVideosPorTagsR4(resultados, n):
    if not lt.isEmpty(resultados):
        print("Lista de " + str(n) + " videos con más likes para el tag y país dados: ")
        contador = 0
        
        for video in lt.iterator(resultados):
            print("----------------------------------------------------------------------------------------------------------------------------------------------------------")
            print(str(contador+1)+':')
            print("Título: " + video['title'])
            print("Título del canal: " + video['channel_title'])
            print("Fecha de publicación: " + video['publish_time'])
            print("Views: " + str(video['views']))
            print("Likes: " + str(video['likes']))
            print("Dislikes: " + str(video['dislikes']))
            print("Tags: " + str(video['tags']['elements']))
            
            contador += 1
            if contador >= n:
                break 
    else:
        print("Ningún video de este país tiene el tag especificado.")


def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Consultar top x videos por vistas, dado el país y la categoría")
    print("3- Consultar el video con mayor cantidad de dias de tendencia de un pais")
    print("4- Videos por categoria")
    print("5- Consultar top x videos por LIKES, dado el país y UN tag")

    print('Reto 2:')
    print('6- Consultar n videos con más likes en una categoria por pais')
    print('7- Consultar el video con más días de trending para un país específico.')
    print('8- Consultar el video con más días de trending para una categoría específica.')
    print('9- Consultar n videos con más likes en un país y tag específico.')
    print("0- Salir")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        if catalog == None:
            
            
            print("Cuantos videos desea cargar maximo: (escribe T para todos)")
            cantidad_datos = input("")

            print("¿Cuál mecanismo de colisión deseas usar para cargar los videos?")
            escogio = False
            while not escogio:
                print("1: Probing")
                print("2: Chaning")
                metodo_colision = input("")
                if metodo_colision == "1":
                    escogio = True
                    metodo_colision = 'PROBING'
                elif metodo_colision == "2":
                    escogio = True
                    metodo_colision = 'CHAINING'
                else:
                    print("Por favor escoge una de las opciones disponibles.")
            
            
            print("¿Cuál número de factor de carga desea utilizar?")
            escogido = False
            while not escogido:
                factor_carga = float(input(""))
                if factor_carga <= 0.0:
                    print("Por favor escoge un número adecuado.")
                else:
                    escogido = True

            print("Cargando información de los archivos ....")
            if str(cantidad_datos).lower() == 't':
                cantidad_datos = 375942
            cantidad_datos = int(cantidad_datos)
            if cantidad_datos >= 375942:
                print("Espera mientras se cargan todos los datos, recuerda que el archivo Large tiene {} videos".format(str(375942)))
            estructura = "ARRAY_LIST"
            catalog = initCatalog(estructura, metodo_colision, factor_carga)
            answer = loadData(catalog, cantidad_datos)
            tiempo = answer[0]
            memoria = answer[1]
            print('Videos cargados: ' + str(lt.size(catalog['videos'])))
            categorias_mapa = catalog['Categorias']
            print('Categorias cargadas: ' + str(mp.size(categorias_mapa)))
            print('Las categorias cargadas son :')
            posicion_imprimir = 1
            for cate in lt.iterator(mp.keySet(categorias_mapa)):
                print(str(posicion_imprimir),": " + "ID: " + str(cate) + "  ,  Nombre: " + me.getValue(mp.get(categorias_mapa, cate))['nombre_categoria'])
                posicion_imprimir += 1
            primer_video = controller.primer_video(catalog)
            print('El primer video cargado es:')
            print("Titulo: " + primer_video["title"] + ", Canal: " + primer_video["channel_title"] + ", Fecha de tendencia: " + \
                str(primer_video["trending_date"]) + ", País: " + primer_video["country"] + ", Vistas: " + str(primer_video["views"]) + \
                    ", Likes: " + str(primer_video["likes"]) + ", Dislikes: " + str(primer_video["dislikes"]))
            print('Los paises distintos de los videos son :')
            contador_paises = 1
            for pais in lt.iterator(catalog['paises']):
                print(str(contador_paises),':',pais)
                contador_paises += 1
            print("Tiempo [ms]: ", f"{tiempo:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{memoria:.3f}")
            #print(mp.get(catalog['VideosPorPais'],"canada"))
            #print(mp.get(me.getValue(mp.get(catalog['VideosPorPais_y_CategoriaId'],"canada")), 10))
        else:
            print('Los datos ya han sido cargados, recuerda que el programa solo tiene permitido cargar\
los datos una vez de los archivos. \n Para recargar, reinicia la aplicación.')
        
        
    
    elif int(inputs[0]) == 2:
        n = lt.size(catalog['videos'])
        print("Buscando en el país: ")
        ha_escogido_pais = False
        while not ha_escogido_pais:
            pais = input("")
            if controller.pais_presente(catalog, pais):
                ha_escogido_pais = True
            else:
                print("Por favor ingresa un pais disponible.")
        print("Buscando en la categoria de ID: ")
        ha_escogido_categoria = False
        while not ha_escogido_categoria:
            categoria_id = input("")
            if controller.categoria_id_presente(catalog, categoria_id):
                ha_escogido_categoria = True
            else:
                print("Por favor ingresa el id de una categoria disponible.")
        print("Revisar entre los primeros x videos: (escribe T para todos)")
        ha_escogido_tamaño = False
        while not ha_escogido_tamaño:
            tamaño_muestra = input("")
            if str(tamaño_muestra).lower() == 't':
                ha_escogido_tamaño = True
                tamaño_muestra = n
            tamaño_muestra = int(tamaño_muestra)
            if tamaño_muestra <= n:
                ha_escogido_tamaño = True
            else:
                print("Recuerda que hay " + str(n) + " videos cargados")
        print("¿Cual algoritmo deseas usar para organizar los videos?")
        ha_escogido_metodo = False
        print("1: Shell Sort ")
        print("2: Selection Sort")
        print("3: Insertion Sort")
        print("4: Quick (Recomendado) Sort")
        print("5: Merge (Recomendado) Sort")
        while not ha_escogido_metodo:
            escogencia = str(input(""))
            if escogencia == "1":
                ha_escogido_metodo = True
                metodo = 'shell'
            elif escogencia == "2":
                ha_escogido_metodo = True
                metodo = 'selection'
            elif escogencia == "3":
                ha_escogido_metodo = True
                metodo = 'insertion'
            elif escogencia == "4":
                ha_escogido_metodo = True
                metodo = 'quick'
            elif escogencia == "5":
                ha_escogido_metodo = True
                metodo = 'merge'
            else:
                print("Por favor escoge una de las cinco opciones de algoritmos de ordenamiento")
        ha_escogido_tamaño_a_mostrar = False
        print("Aunque se organizaran " + str(tamaño_muestra) + " videos, puedes escoger cuantos mostrar en pantalla:")
        while not ha_escogido_tamaño_a_mostrar:
            tamaño_a_mostrar = int(input(""))
            if tamaño_a_mostrar <= tamaño_muestra :
                ha_escogido_tamaño_a_mostrar = True
            else:
                print("Recuerda que organizaras " + str(tamaño_muestra) + " videos")
        ha_escogido_metodo = False
        print("Organizando datos con {}sort, por favor espera...".format(str(metodo)))
        time_1 = time.process_time()
        mas_vistos = controller.getMostViewed(catalog, tamaño_muestra, pais, categoria_id, metodo)
        time_2 = time.process_time()
        posicion_imprimir = 1
        for video in lt.iterator(mas_vistos):
            print(str(posicion_imprimir),": " + "Titulo: " + video["title"] + ", Vistas: " + str(video["views"]) + ", Fecha de tendencia: " \
+ str(video["trending_date"]) + ", Canal: " + video["channel_title"] + ", Likes: " + str(video["likes"]) + ", Dislikes: "\
+ str(video["dislikes"]) + ", Fecha publicación: " + video["publish_time"])
            posicion_imprimir += 1
            if posicion_imprimir > tamaño_a_mostrar:
                break
        print('Milisegundos de carga :{}'.format(str((time_2-time_1)*1000)))
        
    
    elif int(inputs[0]) == 3:
        print("Buscando en el país: ")
        pais = input("")
        print('Cargando informacion, por favor espera...')
        time_1 = time.process_time()
        mas_trending = controller.getMostTrending(catalog, pais)[0]
        time_2 = time.process_time()
        print("El video con mayor cantidad de dias en tendencia en {} es : ".format(pais))
        print("Titulo: " + mas_trending["title"] + ", Canal: " + mas_trending["channel_title"] + ", Dias en tendencia: "\
 + str(mas_trending["repeticiones"]) + ", Pais: " + mas_trending["country"] + " ID: " + mas_trending["video_id"])
        print('Milisegundos de carga :{}'.format(str((time_2-time_1)*1000)))
#        print(mas_trending['video_id'])
    
    elif int(inputs[0]) == 4:
        categoria = input("Digite el nombre de la categoría que desea buscar")
        categoryCatalog = controller.getVideosByCategory(catalog, categoria, catalog)
        video = controller.masDiasTrending(catalog)
        print("El vídeo con más días de tendencia en la categoría {0} fue: Nombre: {1} -- Canal: {2} -- ID de la Categoría: {3} -- Días en Trending: {4}".format(categoryName, video['title'], video['channel_title'], video['category_id'], video['dias_t']))
    
    elif int(inputs[0]) == 5:
        n = lt.size(catalog['videos'])
        print("Buscando en el país: ")
        ha_escogido_pais = False
        while not ha_escogido_pais:
            pais = input("")
            if controller.pais_presente(catalog, pais):
                ha_escogido_pais = True
            else:
                print("Por favor ingresa un pais disponible.")
        print("Buscando videos con el tag: ")
        tag = str(input(''))
        print("Revisar entre los primeros x videos: (escribe T para todos)")
        ha_escogido_tamaño = False
        while not ha_escogido_tamaño:
            tamaño_muestra = input("")
            if str(tamaño_muestra).lower() == 't':
                ha_escogido_tamaño = True
                tamaño_muestra = n
            tamaño_muestra = int(tamaño_muestra)
            if tamaño_muestra <= n:
                ha_escogido_tamaño = True
            else:
                print("Recuerda que hay " + str(n) + " videos cargados")
        print("¿Cual algoritmo deseas usar para organizar los videos?")
        ha_escogido_metodo = False
        print("1: Shell Sort ")
        print("2: Selection Sort")
        print("3: Insertion Sort")
        print("4: Quick (Recomendado) Sort")
        print("5: Merge (Recomendado) Sort")
        while not ha_escogido_metodo:
            escogencia = str(input(""))
            if escogencia == "1":
                ha_escogido_metodo = True
                metodo = 'shell'
            elif escogencia == "2":
                ha_escogido_metodo = True
                metodo = 'selection'
            elif escogencia == "3":
                ha_escogido_metodo = True
                metodo = 'insertion'
            elif escogencia == "4":
                ha_escogido_metodo = True
                metodo = 'quick'
            elif escogencia == "5":
                ha_escogido_metodo = True
                metodo = 'merge'
            else:
                print("Por favor escoge una de las cinco opciones de algoritmos de ordenamiento")
        ha_escogido_tamaño_a_mostrar = False
        print("Aunque se organizaran " + str(tamaño_muestra) + " videos, puedes escoger cuantos mostrar en pantalla:")
        while not ha_escogido_tamaño_a_mostrar:
            tamaño_a_mostrar = int(input(""))
            if tamaño_a_mostrar <= tamaño_muestra :
                ha_escogido_tamaño_a_mostrar = True
            else:
                print("Recuerda que organizaras " + str(tamaño_muestra) + " videos")
        
        ha_escogido_metodo = False
        print("Organizando datos con {}sort, por favor espera...".format(str(metodo)))
        time_1 = time.process_time()
        mas_likes = controller.getMostLiked_porPaisyTags(catalog, tamaño_muestra, pais, tag, metodo)
        time_2 = time.process_time()
        posicion_imprimir = 1
        for video in lt.iterator(mas_likes):
            print(str(posicion_imprimir),": " + "Titulo: " + video["title"] + ", Vistas: " + str(video["views"]) +\
", Canal: " + video["channel_title"] + ", Likes: " + str(video["likes"]) + ", Dislikes: " + str(video["dislikes"])\
+ "Fecha publicación: " + video["publish_time"])
            print('Tags del video: ' )
            for tag in lt.iterator(video['tags']):
                print(tag)
            posicion_imprimir += 1
            if posicion_imprimir > tamaño_a_mostrar:
                break
        print('Milisegundos de carga :{}'.format(str((time_2-time_1)*1000)))
        
    elif int(inputs[0]) == 6:
        print("Buscando en la categoria con nombre: \n")
        ha_escogido_categoria = False
        while not ha_escogido_categoria:
            categoria_nombre = input("")
            id_presente = controller.categoria_presente(catalog, categoria_nombre)
            if id_presente[0]:
                ha_escogido_categoria = True
                categoria_id = id_presente[1]
            else:
                print("Por favor ingresa una categoria disponible.")
                
        
            
        print('Mostrar en pantalla los primeros:\n')
        
        tamaño_mostrar = int(input(""))
            
        
        pais = input("Escoger pais: \n")
        respuesta = controller.getMostViewed_porPaisCategoria(catalog, categoria_id, pais)
        tiempo = respuesta[1]
        memoria = respuesta[2]
        mas_likeados = respuesta[0]
        contador = 0
        print('--------------------------------------------------------------------------------------------------------------')
        print('--------------------------------------------------------------------------------------------------------------')
        for video in lt.iterator(mas_likeados):
            contador += 1
            print(str(contador)+': '+'Titulo: '+(video['title']))
            print(' Views: ' + str(video['views'])) 
            print('Trending date: '+ str(video['trending_date']))
            print('Título de canal: ' + video['channel_title'])
            print('Fecha publicación: ' + str(video['publish_time']))
            print('Likes: ' + str(video['likes'])) 
            print('Dislikes: ' + str(video['dislikes']))
            if contador >= tamaño_mostrar:
                break
        print('--------------------------------------------------------------------------------------------------------------')
        print("Tiempo [ms]: ", f"{tiempo:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{memoria:.3f}")
        print('--------------------------------------------------------------------------------------------------------------')
        print('--------------------------------------------------------------------------------------------------------------')

    elif int(inputs[0])== 7:
        print("¿Para cuál país quiere obtener la información? ")
        pais_R2 = input("")
        print('Cargando informacion, por favor espera...')
        func = controller.VideoTrendingPais(catalog, pais_R2)
        video = func[0][0]
        num_dias = func[0][1]
        tiempo = func[1]
        memoria = func[2]
        print('--------------------------------------------------------------------------------------------------------------')
        print('--------------------------------------------------------------------------------------------------------------')
        printVideosTrendingPais(video, num_dias, pais_R2)
        print('--------------------------------------------------------------------------------------------------------------')
        print("Tiempo [ms]: ", f"{tiempo:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{memoria:.3f}")
        print('--------------------------------------------------------------------------------------------------------------')
        print('--------------------------------------------------------------------------------------------------------------')

    elif int(inputs[0]) == 8:
        print('¿Para cuál categoría quiere obtener la información?')
        ha_escogido_categoria = False
        while not ha_escogido_categoria:
            categoria_nombre = input("")
            id_presente = controller.categoria_presente(catalog, categoria_nombre)
            if id_presente[0]:
                ha_escogido_categoria = True
                categoria_id = id_presente[1]
            else:
                print("Por favor ingresa una categoria disponible.")
        
        print('Cargando información para la categoría...')
        resultado = controller.getMostTrending_Categoria(catalog, categoria_id)
        video = resultado[0][0]
        N_dias = resultado[0][1]
        tiempo = resultado[1]
        memoria = resultado[2]
        print('¿Quieres ver las fechas del video?')
        print('1:Si')
        print('2:No')
        imprimir_fechas = False
        r = input('')
        if r=='1':
            imprimir_fechas = True
        print('--------------------------------------------------------------------------------------------------------------')
        print('--------------------------------------------------------------------------------------------------------------')
        print("El video de la categoria {} que mas días distintos fue trending en el mundo es:".format(categoria_nombre))
        print('Titulo: '+(video['title']))
        print('Título de canal: ' + video['channel_title'])
        print('ID de Categoria: ' + str(video['category_id']))
        print('Estuvo en tendencia {} dias distintos'.format(str(N_dias)))
        print('--------------------------------------------------------------------------------------------------------------')
        print("Tiempo [ms]: ", f"{tiempo:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{memoria:.3f}")
        if imprimir_fechas:

            print(video['lista_de_fechas']['elements'])
        print('--------------------------------------------------------------------------------------------------------------')
        print('--------------------------------------------------------------------------------------------------------------')
        

        

    elif int(inputs[0])== 9:
        print("¿Para qué país desea obtener información?")
        pais_R4 = input("")
        print("¿Cuántos videos quiere listar?")
        n = int(input(""))
        print("Escoja un tag específico: ")
        tag = str(input(""))
        resultados = controller.masLikesPaisTag(catalog, pais_R4, tag)
        videos = resultados[0]
        tiempo = resultados[1]
        memoria = resultados[2]
        printVideosPorTagsR4(videos, n)
        print('--------------------------------------------------------------------------------------------------------------')
        print("Tiempo [ms]: ", f"{tiempo:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{memoria:.3f}")
        print('--------------------------------------------------------------------------------------------------------------')
        print('--------------------------------------------------------------------------------------------------------------')




    else:
        sys.exit(0)

sys.exit(0)
        
# falta pulir view, dejar bien hechos los nuevos, borrar los viejos si lo requieren
