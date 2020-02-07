#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Agente Viajero con Algoritmo Génetico
# Miriam del Carmen García Martínez gammc7@gmail.com
# Febrero de 2020

from math      import sqrt, log
from itertools import permutations as permutaciones
from itertools import islice as rango
from random    import randrange as aleatorio
from random    import random

#Diccionario global donde se guardan las distancias de una ciudad a otra.
distancias = {}

#Método que calcula el factorial de un número.
def fact(n): return 1 if n < 2 else n * fact(n-1)

#Método que crea nuestras ciudades a partir de un archivo
def parserCiudades(archivo):
	fcd = open(archivo,"r")
	lineas = fcd.readlines()
	fcd.close()
	ciudades = []
	for i, linea in enumerate (lineas):
		nums = linea.split(" ")
		ciudades.append( ciudad(i, float(nums[0]), float(nums[1])) )
	return ciudades


#ciudad clase cuyas instancias representan las ciudades que forman parte del
#territorio

class ciudad:
	#constructor de la clase
	def __init__(self, id, x, y):
		self.__id = id
		self.__x = x
		self.__y = y

	#representación de una ciudad como cadena de caracteres
	def __str__(self):
		return "%d" % (self.__id)

	#destructor de la clase ciudad
	def __del__(self):
		del self.__id
		del self.__x
		del self.__y

	#devuelve el valor del id de la ciudad
	def getid(self):
		return self.__id

	#devuelve el valor de x de la ciudad
	def getx(self):
		return self.__x

	#devuelve el valor de y de la ciudad
	def gety(self):
		return self.__y


#cromosoma clase cuyas instancias representan posibles soluciones al problema
#de optimización

class cromosoma:
	#constructor de la clase
	def __init__(self, ciudades = []):
		self.__ciudades = list(ciudades)


	#copia un cromosoma.
	def copy( self ):
		return cromosoma( self.getciudades())

	#destructor de la clase cromosoma
	def __del__(self):
		while self.__ciudades:
			ciudad = self.__ciudades.pop()
			del ciudad

	#devuelve el valor de una ciudad
	def getciudades(self):
		return self.__ciudades

	#representación como cadena de caracteres del cromosoma
	def __str__(self):
		s  = "["
		for ciudad in self.getciudades() :
			s += " %s," % (str(ciudad))
		s +=" %2s ]" % (self.getciudades()[0])
		return s


	#Método que calcula la distancia de una ciudad a otra.
	def distancia(self, cd1, cd2):
		a,b = (cd1, cd2) if cd1.getid() < cd2.getid() else (cd2, cd1)
		key = "%d-%d" % (a.getid(),b.getid())
		if distancias.has_key(key):
			dist= distancias[key]
		else:
			x= b.getx() - a.getx()
			y= b.gety() - a.gety()
			dist= sqrt(x**2 + y**2)
			distancias[key]= dist
		return dist


	#Método que calcula la aptitud asociada a un cromosoma.
	#Método que calcula la distancia total de un recorrido de ciudades.
	def aptitud( self ):
		apt = 0
		orig= self.getciudades()
		dest= list(orig)
		tmp= dest.pop(0)
		dest.append(tmp)
		for a,b in zip(orig,dest):
			apt += self.distancia(a,b)
		return apt

	#Método para comparar dos cromosomas.
	def __cmp__(self, otro):
		return int(self.aptitud() - otro.aptitud())


	#Método para encontrar la posición de una ciudad en la lista.
	def index( self, nodo ):
		return self.___ciudades.index(nodo)


	#Método que implementa la cruza de dos cromosomas.
	#Cruzamiento por ciclos
	def cruzar(self, otro):
		p1, p2 = self.getciudades(), otro.getciudades()
		h1, h2 = list(p2), list(p1)
		idx = [0]
		i = 0
		cont = True
		while cont:
			ciudad = p2[i]
			i = p1.index(ciudad)
			idx.append(i)
			cont = not p1[0] is p2[i]

		for i in idx:
			h1[i], h2[i] = h2[i], h1[i]

		return cromosoma(h1), cromosoma(h2)



	#Método con el que un cromosoma muta.
	#Mutación por inversión.
	def mutar(self):
		lista = self.getciudades()
		mitad = len(lista)/2
		ini = aleatorio(0, mitad)
		fin = aleatorio(mitad, len(lista))
		a, b, c = lista[0:ini], lista[ini:fin], lista[fin:]
		b.reverse()
		del self.__ciudades
		self.__ciudades = a + b + c
		del a
		del b
		del c



#Método que ordena la población de mejor aptitud a peor aptitud.
def sort( self ):
	self.__ciudades.sort()


#Método que calcula la desvión estándar.
def desvestandar(poblacion =[]):
	tam = len(poblacion)
	aptitudes = map(cromosoma.aptitud, poblacion)
	xprom = sum(aptitudes)/tam
	desvs = sqrt(sum(map(lambda x: (x-xprom)**2, aptitudes))/ (tam - 1))
	return desvs, xprom



#Invoca el método de mutación para algunos individuos de la población con
#cierta probabilidad.
def mutarpop( pop, pmuta ):
	for p in pop:
		if pmuta > random():
			p.mutar()


#Cruza los individuos de la población para obtener cromosomas nuevos que
#posteriormente se integrarán a la población en la siguiente generación.
def cruzarpob( pob, pcruza ):
	padres = list( pob )
	hijos = list()

	if len(padres) % 2:
		if random() > 0.5:
			padres.pop( aleatorio(0, len(padres)))
		else:
			padres.append( padres[aleatorio(0, len(padres))] )

	while padres:
		a = padres.pop(aleatorio(0,len(padres)))
		b = padres.pop(aleatorio(0,len(padres)))

		if pcruza > random() :
			hijos.extend( a.cruzar(b) )

	return hijos


#Genera la población inicial.
#Seleccionando fin-ini permutaciones aleatorias del espacio de soluciones.
def generapob( ciudades, pob):
	s     = list()
	perms = permutaciones(ciudades)
	fin   = aleatorio( pob, fact( len(ciudades) ) )
	ini   = fin - pob

	Sigma = list(rango(perms, pob))

	for sigma in Sigma:
		k = list(sigma)
		s.append(cromosoma(k))

	for k in range(2):
		mutarpop(s,1.0)

	return s


#Genera una representación como cadena de caracteres de un conjunto de
#soluciones.
def imprimepob( pob ):
	n      = int( log( len(pob),10) + 1 )
	s      = " | %" + str(n) + "d | %s | %f\n"
	edge= " +" + (n + 2) * "-" + "+" + (len(str(pob[0])) + 2) * "-" + "+\n"
	strpob = edge
	for i, p in enumerate(pob):
		strpob += s % (i+1,str(p), p.aptitud() )

	return strpob + edge



#selecciona
def selecciona(poblacion, pobtam):
	p = list(poblacion)
	p.sort()
	return p[:pobtam]



#selecciona una nueva población utilizando el método de ordenamiento exponencial.
def seleccionOE(poblacion = []):
    poblacion.sort()
    s, prom = desvestandar(poblacion)
    n = len(poblacion)
    prob = lambda r: (1-s)/(1-s**n)*(s**(r-1))
    probabilidades = map(prob, range(n))
    probacumulada  = 0
    pacumuladas    = []
    elegidos       = []
    pobtam = 20

    for probabilidad in probabilidades:
        probacumulada += probabilidad
    pacumuladas.append(probacumulada)
    print "*" *50 ,probacumulada

    for k in range(len(poblacion)):
        cota = random()
        i = 0
        while i < len(pacumuladas) and pacumuladas[i] < cota :
            i += 1
        elegidos.append( poblacion[i] )

    return elegidos[:pobtam]


#Método de selección por torneo.
def selecciont(poblacion, tampob):
	selec = list()
	for k in [1,2]:
		participantes = list(poblacion)
		if len(participantes)%2 ==1:
			if k==1:
				participantes.pop(aleatorio(0, len(participantes)))
			else:
				participantes.append(participantes[aleatorio(0, len(participantes))])
		while participantes:
			a= participantes.pop(aleatorio(0, len(participantes)))
			b= participantes.pop(aleatorio(0, len(participantes)))
			ganador= a if a<b else b
			selec.append(ganador)
	selec.sort()
	return selec[:tampob]



#Implementación de un algoritmo genético para resolver el problema del agente
#viajero.
def genetico(ciudades, pobtam, pcruza, pmuta, iteraciones ):
	poblacion = generapob(ciudades, pobtam)
	print imprimepob(poblacion)
	mejores = list()
	poblacion.sort()
	print "Poblacion ordenada"
	print imprimepob(poblacion)
	mejor = poblacion[0]
	mejores.append(mejor.copy())
	selec = selecciont(poblacion, pobtam)
	continua = True
	i = 1
	while continua and i < iteraciones:
		print i, ") comenzando iteracion"
		i+=1
		print imprimepob(selec)
		hijos = cruzarpob(selec, pcruza)
		selec.extend(hijos)
		mutarpop(selec, pmuta)
		selec = selecciont(selec, pobtam)
		selec.sort()
		mejores.append(selec[0].copy())
		if(len(mejores)>1):
			aux=list(mejores)
			aux.sort()
			n=aux.count(aux[0])
			if(len(mejores)>=10 and n>len(aux)/2):
				continua= False
	mejores.sort()

	print "Los mejores individuos en todas las iteraciones:"
	print imprimepob(mejores)
	return mejores[0]


#Método que guarda las coordenadas de las ciudades recorridas, en un archivo
#ordenadas de acuerdo al recorrido óptimo.
def guardaCoordenadas( optimo, rutaArchivo ):
	archivo   = open( rutaArchivo, "w" )
	contenido = ""
	for ciudad in optimo.getciudades():
		contenido += "%f %f\n" % (ciudad.getx(), ciudad.gety())
	archivo.write(contenido)

	archivo.close()

#Aquí modificaremos los parametros que le pasaremos a el método genetico.
#Ciudades es una lista que contiene todas las ciudades obtenidad del archivo puntos-dj38.tsp.
#pobtam es el tamaño de la población con la que iniciaremos.
#pcruza es la probabilidad de cruzamiento.
#pmuta es la probabilidad de mutación.
#iteraciones es el número de iteraciones para detener el programa.
def main():
	ciudades = parserCiudades("puntos-dj38.tsp")
	pobtam = 40
	pcruza = 0.9
	pmuta = 0.5
	iteraciones = 200
	optimo = genetico(ciudades, pobtam, pcruza, pmuta, iteraciones )
	print "Mejor solución encontrada:"
	print optimo, "-- Con un costo de", optimo.aptitud(), "unidades."

	guardaCoordenadas( optimo, "recorrido-optimo.data" )



if __name__ == "__main__":
	main()
