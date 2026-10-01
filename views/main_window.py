import time
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QTableWidget, 
    QTableWidgetItem, QHeaderView, QGroupBox, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt
from models.inventario_dao import InventarioDAO
from models.repuesto import Repuesto

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión y Consulta de Repuestos")
        self.resize(1050, 720)
        
        self.dao = InventarioDAO()
        self._construir_interfaz()
        self.recargar_tabla_inventario()

    def _construir_interfaz(self):
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QVBoxLayout(widget_central)
        layout_principal.setContentsMargins(18, 18, 18, 18)
        layout_principal.setSpacing(15)

        # --- SECCIÓN: CONSULTA RÁPIDA POR CÓDIGO ---
        grupo_consulta = QGroupBox("Consulta Rápida en Mostrador")
        layout_consulta = QVBoxLayout(grupo_consulta)

        layout_barra_busqueda = QHBoxLayout()
        self.txt_codigo_busqueda = QLineEdit()
        self.txt_codigo_busqueda.setPlaceholderText("Ingrese Código de Parte (ej: BRK-102-1)...")
        self.txt_codigo_busqueda.returnPressed.connect(self.ejecutar_busqueda)

        btn_buscar = QPushButton("Buscar Repuesto")
        btn_buscar.clicked.connect(self.ejecutar_busqueda)

        layout_barra_busqueda.addWidget(self.txt_codigo_busqueda)
        layout_barra_busqueda.addWidget(btn_buscar)
        layout_consulta.addLayout(layout_barra_busqueda)

        # Tarjeta para mostrar el resultado instantáneo
        self.frame_resultado = QFrame()
        self.frame_resultado.setObjectName("tarjeta_resultado")
        layout_res = QHBoxLayout(self.frame_resultado)

        self.lbl_info_repuesto = QLabel("Ingrese un código para verificar existencias y precio.")
        self.lbl_info_repuesto.setWordWrap(True)
        
        self.lbl_precio_res = QLabel("$0.00")
        self.lbl_precio_res.setObjectName("lbl_destacado")
        self.lbl_precio_res.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.lbl_stock_res = QLabel("-")
        self.lbl_stock_res.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout_res.addWidget(self.lbl_info_repuesto, stretch=3)
        layout_res.addWidget(self.lbl_stock_res, stretch=1)
        layout_res.addWidget(self.lbl_precio_res, stretch=1)
        layout_consulta.addWidget(self.frame_resultado)

        layout_principal.addWidget(grupo_consulta)

        # --- SECCIÓN: INVENTARIO COMPLETO ---
        grupo_inventario = QGroupBox("Inventario Completo en Stock")
        layout_inv = QVBoxLayout(grupo_inventario)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(7)
        self.tabla.setHorizontalHeaderLabels([
            "Código de Parte", "Descripción", "Categoría", 
            "Vehículo", "Stock", "Precio Venta ($)", "Última Actualización"
        ])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setAlternatingRowColors(True)
        layout_inv.addWidget(self.tabla)

        # Barra inferior de controles
        layout_acciones = QHBoxLayout()
        btn_actualizar = QPushButton("Recargar Inventario")
        btn_actualizar.setObjectName("btn_secundario")
        btn_actualizar.clicked.connect(self.recargar_tabla_inventario)

        self.lbl_conteo_total = QLabel("Total productos registrados: 0")
        
        layout_acciones.addWidget(self.lbl_conteo_total)
        layout_acciones.addStretch()
        layout_acciones.addWidget(btn_actualizar)
        layout_inv.addLayout(layout_acciones)

        layout_principal.addWidget(grupo_inventario)

    def ejecutar_busqueda(self):
        codigo = self.txt_codigo_busqueda.text()
        if not codigo.strip():
            self.lbl_info_repuesto.setText("Por favor ingrese un código de parte válido.")
            self.lbl_precio_res.setText("$0.00")
            self.lbl_stock_res.setText("-")
            return

        # Medir tiempo con la librería time
        t_inicio = time.time()
        repuesto = self.dao.buscar_por_codigo(codigo)
        t_duracion = (time.time() - t_inicio) * 1000  # ms

        if repuesto:
            info_txt = (
                f"<b>Producto:</b> {repuesto.get('nombre')}<br>"
                f"<b>Vehículo:</b> {repuesto.get('marca_vehiculo')} | "
                f"<b>Categoría:</b> {repuesto.get('categoria')} | "
                f"<i>Consulta resuelta en {t_duracion:.2f} ms</i>"
            )
            self.lbl_info_repuesto.setText(info_txt)
            self.lbl_precio_res.setText(f"${repuesto.get('precio_venta', 0.0):.2f}")
            
            stock_actual = repuesto.get('stock', 0)
            if stock_actual > 0:
                self.lbl_stock_res.setObjectName("lbl_aviso_disponible")
                self.lbl_stock_res.setText(f"En Stock: {stock_actual} uds.")
            else:
                self.lbl_stock_res.setObjectName("lbl_aviso_agotado")
                self.lbl_stock_res.setText("¡SIN STOCK!")

            # Re-aplicar estilo para actualizar colores dinámicos
            self.lbl_stock_res.setStyleSheet(self.lbl_stock_res.styleSheet())
        else:
            self.lbl_info_repuesto.setText(f"El código <b>{codigo.upper()}</b> no está registrado en el inventario.")
            self.lbl_precio_res.setText("$0.00")
            self.lbl_stock_res.setObjectName("lbl_aviso_agotado")
            self.lbl_stock_res.setText("No encontrado")

    def recargar_tabla_inventario(self):
        items = self.dao.obtener_todo_el_inventario()
        self.tabla.setRowCount(0)

        for fila_idx, item in enumerate(items):
            self.tabla.insertRow(fila_idx)
            
            self.tabla.setItem(fila_idx, 0, QTableWidgetItem(str(item.get("codigo_parte", ""))))
            self.tabla.setItem(fila_idx, 1, QTableWidgetItem(str(item.get("nombre", ""))))
            self.tabla.setItem(fila_idx, 2, QTableWidgetItem(str(item.get("categoria", ""))))
            self.tabla.setItem(fila_idx, 3, QTableWidgetItem(str(item.get("marca_vehiculo", ""))))
            
            stock_item = QTableWidgetItem(str(item.get("stock", 0)))
            stock_item.setTextAlignment(Qt.AlignCenter)
            self.tabla.setItem(fila_idx, 4, stock_item)

            precio_item = QTableWidgetItem(f"${item.get('precio_venta', 0.0):.2f}")
            precio_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tabla.setItem(fila_idx, 5, precio_item)

            self.tabla.setItem(fila_idx, 6, QTableWidgetItem(str(item.get("fecha_registro", ""))))

        self.lbl_conteo_total.setText(f"Total productos registrados: {len(items)}")