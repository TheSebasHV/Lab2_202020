"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 * Contribución de:
 *
 * Cristian Camilo Castellanos
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
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

"""
  Este módulo es una aplicación básica con un menú de opciones para cargar datos, contar elementos, y hacer búsquedas sobre una lista .
"""

import config as cf
import sys
import csv
from ADT import list as lt
from Sorting import insertionsort   
from Sorting import mergesort  
from Sorting import quicksort   
from Sorting import selectionsort  
from Sorting import shellsort 
from DataStructures import listiterator as it
from DataStructures import liststructure as lt

from time import process_time 


def loadCSVFile (file, sep=";"):
    """
    Carga un archivo csv a una lista
    Args:
        file
            Archivo csv del cual se importaran los datos
        sep = ";"
            Separador utilizado para determinar cada objeto dentro del archivo
        Try:
        Intenta cargar el archivo CSV a la lista que se le pasa por parametro, si encuentra algun error
        Borra la lista e informa al usuario
    Returns: None  
    """
    #lst = lt.newList("SINGLE_LINKED") #Usando implementacion linkedlist
    lst = lt.newList("ARRAY_LIST") #Usando implementacion linkedlist
    print("Cargando archivo ....")
    t1_start = process_time() #tiempo inicial
    dialect = csv.excel()
    dialect.delimiter=sep
    try:
        with open(file, encoding="utf-8") as csvfile:
            spamreader = csv.DictReader(csvfile, dialect=dialect)
            for row in spamreader: 
                lt.addLast(lst,row)
    except:
        print("Hubo un error con la carga del archivo")
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    return lst


def printMenu():
    """
    Imprime el menu de opciones
    """
    print("\nBienvenido")
    print("1- Cargar Datos")
    print("2- Contar los elementos de la Lista")
    print("3- Contar elementos filtrados por palabra clave")
    print("4- Consultar elementos a partir de dos listas")
    print("5- Ordenar una lista por su calificación promedio o cantidad de votos")
    print("6- Conocer el trabajo de un director")
    print("0- Salir")

def countElementsFilteredByColumn(criteria, column, lst):
    """
    Retorna cuantos elementos coinciden con un criterio para una columna dada  
    Args:
        criteria:: str
            Critero sobre el cual se va a contar la cantidad de apariciones
        column
            Columna del arreglo sobre la cual se debe realizar el conteo
        list
            Lista en la cual se realizará el conteo, debe estar inicializada
    Return:
        counter :: int
            la cantidad de veces ue aparece un elemento con el criterio definido
    """
    if lst['size']==0:
        print("La lista esta vacía")  
        return 0
    else:
        t1_start = process_time() #tiempo inicial
        counter=0
        iterator = it.newIterator(lst)
        while  it.hasNext(iterator):
            element = it.next(iterator)
            if criteria.lower() in element[column].lower(): #filtrar por palabra clave 
                counter+=1           
        t1_stop = process_time() #tiempo final
        print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    return counter

def orderElementsByCriteria(function, lst, criteria, elements):
    """
    Retorna el ranking de películas con base en los parámetros
     Args:
        function
            Función de ordenamiento que se va a usar
        column:: str
            Columna que se usa para realiza el ordenamiento (vote_average o vote_count)   
        lst
            Lista encadenada o arreglo     
        criteria:: str
            Critero para ordenar (less o greater)
        elements:: int
            Cantidad de elementos para el ranking
    Return:
        counter :: int
            la cantidad de veces ue aparece un elemento con el criterio definido
    """
    t1_start = process_time() #tiempo inicial
    if function == "selectionsort":
       selectionsort.selectionSort(lst, criteria)
    if function == "insertionsort":
       insertionsort.insertionSort(lst, criteria)
    if function == "mergesort":
       mergesort.mergesort(lst, criteria)
    if function == "quicksort":
       quicksort.quickSort(lst, criteria)
    if function == "shellsort":
       shellsort.shellSort(lst, criteria)
    i = 0
    ordenado = []
    while i < elements:
       i += 1
       pelicula = lt.getElement(lst,i)
       ordenado.append(pelicula)
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")       
    return ordenado

def countElementsByCriteria(director,datos):
    r=0
    numero_peliculas=0
    lista=[]
    id_peliculas=[]
    while r<len(datos):
        p=datos[r]
        if p["director_name"]== director:
            numero_peliculas+=1
            lista.append(p)
            id_peliculas.append(p["id"])
        r+=1
    return numero_peliculas,lista,id_peliculas
def votos_media(id_peliculasa,lista):
    r=0
    suma=0
    promedio=0
    while r<len(lista):
        p=lista[r]
        for i in id_peliculasa:
            if i == p["id"]:
                suma+=float(p["vote_average"])
        r+=1
    if suma > 0:
        promedio=suma/len(id_peliculasa)
    return promedio
def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados
    Instancia una lista vacia en la cual se guardarán los datos cargados desde el archivo
    Args: None
    Return: None 
    """
    lista = lt.newList()   # se require usar lista definida
    while True:
        printMenu() #imprimir el menu de opciones en consola
        inputs =input('Seleccione una opción para continuar\n') #leer opción ingresada
        if len(inputs)>0:
            if int(inputs[0])==1: #opcion 1
                lista = loadCSVFile("Data/theMoviesdb/SmallMoviesDetailsCleaned.csv") #llamar funcion cargar datos
                print("Datos cargados, ",lista['size']," elementos cargados")
            elif int(inputs[0])==2: #opcion 2
                if lista==None or lista['size']==0: #obtener la longitud de la lista
                    print("La lista esta vacía")    
                else: print("La lista tiene ",lista['size']," elementos")
            elif int(inputs[0])==3: #opcion 3
                if lista==None or lista['size']==0: #obtener la longitud de la lista
                    print("La lista esta vacía")
                else:   
                    criteria =input('Ingrese el criterio de búsqueda\n')
                    counter=countElementsFilteredByColumn(criteria, "nombre", lista) #filtrar una columna por criterio  
                    print("Coinciden ",counter," elementos con el crtierio: ", criteria  )
            elif int(inputs[0])==4: #opcion 4
                if lista==None or lista['size']==0: #obtener la longitud de la lista
                    print("La lista esta vacía")
                else:
                    criteria =input('Ingrese el criterio de búsqueda\n')
                    counter=countElementsByCriteria(criteria,0,lista)
                    print("Coinciden ",counter," elementos con el crtierio: '", criteria ,"' (en construcción ...)")
            elif int(inputs[0])==5:
                if lista==None or lista['size']==0: #obtener la longitud de la lista
                    print("La lista esta vacía")
                else:   
                    print("Hay 5 algoritmos de ordenamiento: \ninsertionsort\nmergesort\nquicksort\nselectionsort\nshellsort")    
                    ## Pide los parámetros al usuario
                    algoritmo = input("Escriba el algoritmo de ordenamiento que desee usar: ")
                    columna = input("Escriba la columna a utilizar (vote_average o vote_count): ")  
                    criteria = input("Escriba el criterio a utilizar (less o greater): ") 
                    elements = int(input("¿Cuántas películas quiere ver en el ranking?: "))
                    def less(element1, element2, column=columna): # Agregué "column" para poder escoger, por ejemplo, entre vote_average y vote_count
                        if float(element1[column]) < float(element2[column]):
                           return True
                        return False
                    def greater(element1, element2,column=columna):
                        if float(element1[column]) > float(element2[column]):
                           return True
                        return False  
                    if criteria == "less":
                       lista = orderElementsByCriteria(algoritmo, lista, less, elements)
                    elif criteria == "greater":
                       lista = orderElementsByCriteria(algoritmo, lista, greater, elements)
                    print("Películas ordenadas: \n")   
                    print(lista)    
            elif int(inputs[0])==6:
                print("Escriba el director")
                t=input()
                u=loadCSVFile("Data/theMoviesdb/MoviesCastingRaw-small.csv")
                p=u["elements"]
                e=countElementsByCriteria(t,p)
                o=loadCSVFile("Data/theMoviesdb/SmallMoviesDetailsCleaned.csv")
                y=o["elements"]
                w=votos_media(e[2],y)
                print(w)
                print("el numero de peliculas dirigidas por {0} fueron {1} con un promedio de {2}".format(t,e[0],w))
                print("la lista de las peliculas dirigidas son {o}")
                print(e[1])
            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)
                
if __name__ == "__main__":
   main()