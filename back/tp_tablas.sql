USE TP_IDS;

-- TABLA DE REPORTES - Se comunica con la tabla INCIDETES y la tabla USUARIOS
CREATE TABLE reportes (
	ID_reporte INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ciudad VARCHAR(100) NOT NULL,
    localidad VARCHAR(100) NOT NULL,
    fecha_reporte DATE NOT NULL,
    horario_reporte TIME NOT NULL,
    FOREIGN KEY (ID_incidente) REFERENCES incidentes(ID_incidentes),
    FOREIGN KEY (ID_usario) REFERENCES usuarios(ID_usuario)
);

-- TABLA DE INCIDENTES - Se comunica con la tabla REPORTES
CREATE TABLE incidentes (
	ID_incidente INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    tipo_reporte VARCHAR(50) NOT NULL,
    direccion_reporte VARCHAR(100) NOT NULL,
    descripcion VARCHAR(100) NOT NULL
);

-- TABLA DE USUARIOS - Se comunica con la tabla REPORTES
CREATE TABLE usuarios (
	ID_usuario INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(20) NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    telefono VARCHAR(50) NOT NULL
);

-- QUEDA PARA HACER EL HARDCODEO DE DATOS