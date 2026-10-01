import json
import os
import random
import time
import math
from models.repuesto import Repuesto

class InventarioDAO:
    def __init__(self, filepath="data/inventario.json"):
        self.filepath = filepath
        self.datos = {}  # Estructura anidada: { "categoria": { "marca": [ {repuesto_dict}, ... ] } }
        self._inicializar_directorio()
        self.cargar_datos()

    def _inicializar_directorio(self):
        directorio = os.path.dirname(self.filepath)
        if directorio != "" and not os.path.exists(directorio):
            os.makedirs(directorio)

    def cargar_datos(self):
        if not os.path.exists(self.filepath):
            self.generar_datos_demo()
            return

        try:
            with open(self.filepath, 'r', encoding='utf-8') as file:
                self.datos = json.load(file)
        except Exception:
            self.datos = {}
            self.guardar_datos()

    def guardar_datos(self):
        with open(self.filepath, 'w', encoding='utf-8') as file:
            json.dump(self.datos, file, indent=4, ensure_ascii=False)

    def registrar_repuesto(self, repuesto: Repuesto):
        cat = repuesto.categoria
        marca = repuesto.marca_vehiculo
        
        # Inserción con condicionales anidados
        if cat not in self.datos:
            self.datos[cat] = {}
            if marca not in self.datos[cat]:
                self.datos[cat][marca] = []
        else:
            if marca not in self.datos[cat]:
                self.datos[cat][marca] = []

        # Comprobar si ya existe mediante bucles anidados
        actualizado = False
        for c_key, marcas_dict in self.datos.items():
            for m_key, lista_items in marcas_dict.items():
                for item in lista_items:
                    if item.get("codigo_parte") == repuesto.codigo_parte:
                        item["stock"] = repuesto.stock
                        item["precio_costo"] = repuesto.precio_costo
                        item["precio_venta"] = repuesto.calcular_precio_venta()
                        actualizado = True
                        break
        
        if not actualizado:
            self.datos[cat][marca].append(repuesto.to_dict())

        self.guardar_datos()

    def buscar_por_codigo(self, codigo_parte):
        codigo_limpio = str(codigo_parte).strip().upper()
        # Búsqueda mediante bucles y condicionales anidados
        for cat, marcas in self.datos.items():
            for marca, repuestos in marcas.items():
                i = 0
                while i < len(repuestos):
                    rep = repuestos[i]
                    if rep.get("codigo_parte") == codigo_limpio:
                        if rep.get("stock", 0) > 0:
                            rep["estado_stock"] = "Disponible"
                        else:
                            rep["estado_stock"] = "Agotado"
                        return rep
                    i += 1
        return None

    def obtener_todo_el_inventario(self):
        lista_completa = []
        for cat, marcas in self.datos.items():
            for marca, repuestos in marcas.items():
                for item in repuestos:
                    lista_completa.append(item)
        return lista_completa

    def generar_datos_demo(self):
        categorias = ["Frenos", "Suspension", "Motor", "Electrico"]
        marcas = ["Toyota", "Ford", "Chevrolet", "Jeep"]
        prefijos = ["BRK", "SUS", "ENG", "ELC"]

        self.datos = {}
        for idx, cat in enumerate(categorias):
            self.datos[cat] = {}
            for marca in marcas:
                self.datos[cat][marca] = []
                # Generar repuestos aleatorios
                for correlativo in range(1, 3):
                    cod = f"{prefijos[idx]}-{random.randint(100, 999)}-{correlativo}"
                    costo = round(random.uniform(15.0, 180.0), 2)
                    stock_qty = random.randint(0, 15)
                    nombre = f"Repuesto {cat} {marca} Mod-{correlativo}"
                    
                    rep = Repuesto(
                        codigo_parte=cod,
                        nombre=nombre,
                        categoria=cat,
                        marca_vehiculo=marca,
                        stock=stock_qty,
                        precio_costo=costo
                    )
                    self.datos[cat][marca].append(rep.to_dict())

        self.guardar_datos()