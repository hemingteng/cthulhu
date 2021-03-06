#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       inicio.py
#       
#       Copyright 2012 Danny Enrique Vasconez <dannyvasconeze@gmail.com>
#                      Daniel Engiberto Granda Guitierrez <degranda87@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import pygtk
pygtk.require("2.0")
import gtk
from time import sleep
import os
import sys
from pysvg.structure import *
from pysvg.core import *
from pysvg.text import *
from pysvg.shape import *
from cliente_lib import *
#from sender import *
from renderizado import renderizado as mapa
#from AriaPy import *
"""\package inicio
   \brief programa que utiliza la libreria cliente_lib
   \details Programa que utiliza el XML de gtk+ y la libreria cliente_lib para comunicarse con el servidor de la plataforma movil utilizando una interfaz grafica
   \authors   Danny Vasconez
   \authors   Daniel Granda
   \version   0.0.3
   \date      2012
   \pre       Tener funcionando el servidor
   \bug       Nada
   \warning   uso inapropiado puede hacer que la aplicacion falle
   
"""
class prueba_adqui(object):
	"""
	\class inicio.prueba_adqui
	\brief es la clase encargada del entorno grafico y enlace con cliente_lib 
	"""
	def __init__(self,dimensiones,nombre_archivo,dimensiones_robot):
		"""
		\brief para cargar el XML de gtk+ y sus senales
		\param self no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la definicion de una clase
		\return self
		"""
		self.aument=0
		builder = gtk.Builder() #El archivo de glade debe estar en gtkbuilder
		builder.add_from_file("glade/GUI.glade") #Carga el archivo glade
		builder.connect_signals(self) #Toma todas las senales de glade
		self.teleoper = builder.get_object("map") #Ventana principal
		self.boton = builder.get_object("button1")
		self.area=builder.get_object("mapa")
		self.teleoper.show()
		#Inicializa cliente d-bus
		#self.client_dbus = DBusClient()
		#
		#Inicializar visor
		#self.client_dbus.visor()
		#
		#imnicio opencv
		self.imagen=mapa(dimensiones,nombre_archivo,dimensiones_robot)
		self.nombre_archivo=nombre_archivo
		self.imagen.cargar()
		#
		self.a=cliente_lib();
		#self.a.ip="192.168.1.102"
		self.cliente=self.a.cliente_inicio()
		#self.a.cliente_apaga(self.cliente)
		try:
			self.cliente=self.a.envio_consulta_fisica(self.cliente,"pose")
			#valor_x,valor_y,valor_t=self.a.devuelve_valors()
			valor_x=self.a.x
			valor_y=self.a.y
			ArUtil.sleep(100) #cambiar estos comandos por temporisadores de python
			#sleep(0.1)
			self.cliente=self.a.envio_consulta_fisica(self.cliente,"updateNumbers")
			self.valores_f=self.a.devuelve_valorf()
			mi_x=self.valores_f[1]
			mi_y=self.valores_f[2]
			mi_th=self.valores_f[3]
			#print valor_x
			#print valor_y
			print len(valor_x)
			self.generador_mapa(valor_x,valor_y,mi_x,mi_y,mi_th)
		except:
			print "Fallo inicio"
			pass
	def izq_clicked(self, widget, data=None):
		try:
			print "presiono izquierda"
			TransRatio,RotRatio,LatRatio = [0,90,90]
			self.cliente=self.a.envio_ratioDrive(self.cliente,TransRatio,RotRatio,LatRatio) #fijar los valores para mover
			ArUtil.sleep(100)
			#sleep(0.1)
			self.cliente=self.a.envio_consulta_fisica(self.cliente,"pose")
			#valor_x,valor_y,valor_t=self.a.devuelve_valors()
			valor_x=self.a.x
			valor_y=self.a.y
			self.cliente=self.a.envio_consulta_fisica(self.cliente,"updateNumbers")
			self.valores_f=self.a.devuelve_valorf()
			mi_x=self.valores_f[1]
			mi_y=self.valores_f[2]
			mi_th=self.valores_f[3]
			#print self.valores_f
			#print valor_x
			#print valor_y
			print len(valor_x)
			self.generador_mapa(valor_x,valor_y,mi_x,mi_y,mi_th)
		except:
			print "Fallo init"
			pass
	def der_clicked(self, widget, data=None):
		try:
			print "presiono derecha"
			TransRatio,RotRatio,LatRatio = [0,-90,-90]
			self.cliente=self.a.envio_ratioDrive(self.cliente,TransRatio,RotRatio,LatRatio) #fijar los valores para mover
			ArUtil.sleep(100)
			#sleep(0.1)
			self.cliente=self.a.envio_consulta_fisica(self.cliente,"pose")
			#valor_x,valor_y,valor_t=self.a.devuelve_valors()
			valor_x=self.a.x
			valor_y=self.a.y
			self.cliente=self.a.envio_consulta_fisica(self.cliente,"updateNumbers")
			self.valores_f=self.a.devuelve_valorf()
			mi_x=self.valores_f[1]
			mi_y=self.valores_f[2]
			mi_th=self.valores_f[3]
			#print self.valores_f
			#print valor_x
			#print valor_y
			print len(valor_x)
			self.generador_mapa(valor_x,valor_y,mi_x,mi_y,mi_th)
		except:
			print "Fallo"
			pass
	def arriba_clicked(self, widget, data=None):
		try:
			print "Presiono arriba"
			TransRatio,RotRatio,LatRatio = [50,0,0]
			self.cliente=self.a.envio_ratioDrive(self.cliente,TransRatio,RotRatio,LatRatio) #fijar los valores para mover
			ArUtil.sleep(100)
			#sleep(0.1)
			self.cliente=self.a.envio_consulta_fisica(self.cliente,"pose")
			#valor_x,valor_y,valor_t=self.a.devuelve_valors()
			valor_x=self.a.x
			valor_y=self.a.y
			self.cliente=self.a.envio_consulta_fisica(self.cliente,"updateNumbers")
			self.valores_f=self.a.devuelve_valorf()
			mi_x=self.valores_f[1]
			mi_y=self.valores_f[2]
			mi_th=self.valores_f[3]
			#print self.valores_f
			#print valor_x
			#print valor_y
			print len(valor_x)
			self.generador_mapa(valor_x,valor_y,mi_x,mi_y,mi_th)
		except:
			print "Fallo"
			pass
	def abajo_clicked(self, widget, data=None):
		try:
			print "Presiono abajo"
			TransRatio,RotRatio,LatRatio = [-50,0,0]
			self.cliente=self.a.envio_ratioDrive(self.cliente,TransRatio,RotRatio,LatRatio) #fijar los valores para mover
			ArUtil.sleep(100)
			#sleep(0.1)
			self.cliente=self.a.envio_consulta_fisica(self.cliente,"pose")
			#valor_x,valor_y,valor_t=self.a.devuelve_valors()
			valor_x=self.a.x
			valor_y=self.a.y
			self.cliente=self.a.envio_consulta_fisica(self.cliente,"updateNumbers")
			self.valores_f=self.a.devuelve_valorf()
			mi_x=self.valores_f[1]
			mi_y=self.valores_f[2]
			mi_th=self.valores_f[3]
			#print self.valores_f
			#print valor_x
			#print valor_y
			print len(valor_x)
			self.generador_mapa(valor_x,valor_y,mi_x,mi_y,mi_th)
		except:
			print "Fallo"
			pass
	def parar_clicked(self, widget, data=None):
		try:
			print "Presiono alto"
			self.cliente.requestOnce("stop") #parada de emergencia
			ArUtil.sleep(100)
			#sleep(0.1)
			self.cliente=self.a.envio_consulta_fisica(self.cliente,"pose")
			#valor_x,valor_y,valor_t=self.a.devuelve_valors()
			valor_x=self.a.x
			valor_y=self.a.y
			self.cliente=self.a.envio_consulta_fisica(self.cliente,"updateNumbers")
			self.valores_f=self.a.devuelve_valorf()
			mi_x=self.valores_f[1]
			mi_y=self.valores_f[2]
			mi_th=self.valores_f[3]
			#print self.valores_f
			#print valor_x
			#print valor_y
			print len(valor_x)
			self.generador_mapa(valor_x,valor_y,mi_x,mi_y,mi_th)
		except:
			print "Fallo"
			pass
	def button1_clicked(self, widget, data=None):
		try:
			self.cliente=self.a.envio_consulta_fisica(self.cliente,"pose")
			ArUtil.sleep(100)
			#sleep(0.1)
			#valor_x,valor_y,valor_t=self.a.devuelve_valors()
			valor_x=self.a.x
			valor_y=self.a.y
			self.cliente=self.a.envio_consulta_fisica(self.cliente,"updateNumbers")
			self.valores_f=self.a.devuelve_valorf()
			mi_x=self.valores_f[1]
			mi_y=self.valores_f[2]
			mi_th=self.valores_f[3]
			#print self.valores_f
			#print valor_x
			#print valor_y
			print len(valor_x)
			self.generador_mapa(valor_x,valor_y,mi_x,mi_y,mi_th)
		except:
			print "Fallo paro"
			pass

	def generador_mapa(self,valor_x,valor_y,mi_x,mi_y,mi_th):
		try:
			print valor_x
			if (len(valor_x)>0):
				for a in range(len(valor_x)): #SIP en c. 
					self.imagen.anadir_punto((valor_x['x%d' % a]/100+300,valor_y['y%d' % a]/100+200),radio=2)
			self.imagen.crear_imagen()
			self.imagen.rotacion_y_posicion_robot(mi_x/100+300,mi_y/100+200,mi_th)
			self.area.set_from_file(self.nombre_archivo)
		except:
			print "Fallo mapa"
			pass
	
	def on_maps_destroy(self, widget, data=None):
		print self.a.cliente_apaga(self.cliente)
		gtk.main_quit()
	
def main():
	"""
	\brief El encargado al momento de ejcutar la aplicacion de instanciar el objeto prueba_teleoperacion
	"""
	if os.name=="posix": #verifica que sea un entorno Linux
		dimensiones=(600,400)
		nombre_archivo="filenamea.jpg"
		dimensiones_robot=(13,13)
		app = prueba_adqui(dimensiones,nombre_archivo,dimensiones_robot) #instancia el objeto GUI con las senales enlazadas
		gtk.main() #levanta el motor GTK para poder visualizar
  

if __name__ == '__main__':
	main()


