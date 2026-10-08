QCSS_STYLES = """
QMainWindow, QDialog {
    background-color: #121417;
}

QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #E0E0E0;
    font-size: 13px;
}

/* Paneles y Contenedores */
QGroupBox {
    border: 1px solid #2B303A;
    border-radius: 8px;
    margin-top: 15px;
    font-weight: bold;
    color: #00ADB5;
    padding-top: 15px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 10px;
    background-color: #121417;
}

/* Entradas de texto, Listas y SpinBoxes */
QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
    background-color: #1E2229;
    border: 1px solid #363C48;
    border-radius: 6px;
    padding: 8px 12px;
    color: #FFFFFF;
    selection-background-color: #00ADB5;
}

QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
    border: 1px solid #00ADB5;
    background-color: #242932;
}

QComboBox::drop-down {
    border: none;
}

QComboBox QAbstractItemView {
    background-color: #1E2229;
    color: #FFFFFF;
    selection-background-color: #00ADB5;
}

/* Botones */
QPushButton {
    background-color: #00ADB5;
    color: #0E1013;
    font-weight: bold;
    border-radius: 6px;
    padding: 9px 18px;
    border: none;
}

QPushButton:hover {
    background-color: #00D1DC;
}

QPushButton:pressed {
    background-color: #00878E;
}

QPushButton#btn_secundario {
    background-color: #2B303A;
    color: #E0E0E0;
}

QPushButton#btn_secundario:hover {
    background-color: #39404E;
}

/* Tablas */
QTableWidget {
    background-color: #1A1D24;
    alternate-background-color: #1E2229; /* ESTA ES LA LÍNEA NUEVA PARA ARREGLAR LAS FILAS BLANCAS */
    border: 1px solid #2B303A;
    border-radius: 6px;
    gridline-color: #262B35;
    selection-background-color: #234E52;
    selection-color: #FFFFFF;
}

QHeaderView::section {
    background-color: #242933;
    color: #A0AAB8;
    padding: 8px;
    font-weight: bold;
    border: none;
    border-bottom: 2px solid #00ADB5;
}

QTableCornerButton::section {
    background-color: #242933;
    border: none;
}

/* Tarjeta de Resumen / Resultado */
QFrame#tarjeta_resultado {
    background-color: #1A1D24;
    border: 1px solid #2B303A;
    border-radius: 8px;
    padding: 12px;
}

QLabel#lbl_destacado {
    font-size: 20px;
    font-weight: bold;
    color: #00ADB5;
}

QLabel#lbl_aviso_agotado {
    font-size: 16px;
    font-weight: bold;
    color: #FF5370;
}

QLabel#lbl_aviso_disponible {
    font-size: 16px;
    font-weight: bold;
    color: #C3E88D;
}
"""