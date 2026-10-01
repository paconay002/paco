import math
import time

class Repuesto:
    def __init__(self, codigo_parte, nombre, categoria, marca_vehiculo, stock, precio_costo, margen_ganancia=0.30):
        self.codigo_parte = str(codigo_parte).strip().upper()
        self.nombre = nombre
        self.categoria = categoria
        self.marca_vehiculo = marca_vehiculo
        self.stock = int(stock)
        self.precio_costo = float(precio_costo)
        self.margen_ganancia = float(margen_ganancia)
        self.fecha_registro = time.strftime("%Y-%m-%d %H:%M:%S")

    def calcular_precio_venta(self):
        # Uso de math.ceil para redondear hacia arriba al centavo más cercano
        precio_bruto = self.precio_costo * (1.0 + self.margen_ganancia)
        precio_final = math.ceil(precio_bruto * 100) / 100.0
        return precio_final

    def to_dict(self):
        return {
            "codigo_parte": self.codigo_parte,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "marca_vehiculo": self.marca_vehiculo,
            "stock": self.stock,
            "precio_costo": self.precio_costo,
            "margen_ganancia": self.margen_ganancia,
            "precio_venta": self.calcular_precio_venta(),
            "fecha_registro": self.fecha_registro
        }

    @classmethod
    def from_dict(cls, data):
        rep = cls(
            data.get("codigo_parte", ""),
            data.get("nombre", ""),
            data.get("categoria", ""),
            data.get("marca_vehiculo", ""),
            data.get("stock", 0),
            data.get("precio_costo", 0.0),
            data.get("margen_ganancia", 0.30)
        )
        if "fecha_registro" in data:
            rep.fecha_registro = data["fecha_registro"]
        return rep