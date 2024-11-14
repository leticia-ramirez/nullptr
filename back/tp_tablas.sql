USE TP_IDS;

-- TABLA DE INCIDENTES - Se comunica con la tabla REPORTES
CREATE TABLE incidentes (
	ID_incidente INT NOT NULL AUTO_INCREMENT,
    tipo_reporte VARCHAR(50) NOT NULL,
    direccion_reporte VARCHAR(100) NOT NULL,
    descripcion VARCHAR(100) NOT NULL,
	PRIMARY KEY (ID_incidente)
);

-- TABLA DE USUARIOS - Se comunica con la tabla REPORTES
CREATE TABLE usuarios (
	ID_usuario INT NOT NULL AUTO_INCREMENT,
    nombre_usuario VARCHAR(20) NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    telefono VARCHAR(50) NOT NULL,
    PRIMARY KEY (ID_usuario)
);

-- TABLA DE REPORTES - Se comunica con la tabla INCIDETES y la tabla USUARIOS
CREATE TABLE reportes (
	ID_reporte INT NOT NULL AUTO_INCREMENT,
    ciudad VARCHAR(100) NOT NULL,
    localidad VARCHAR(100) NOT NULL,
    fecha_reporte DATE NOT NULL,
    horario_reporte TIME NOT NULL,
    ID_incidente INT,
    ID_usuario INT,
    PRIMARY KEY (ID_reporte),
    FOREIGN KEY (ID_incidente) REFERENCES incidentes(ID_incidente),
    FOREIGN KEY (ID_usario) REFERENCES usuarios(ID_usuario)
);


-- QUEDA PARA HACER EL HARDCODEO DE DATOS