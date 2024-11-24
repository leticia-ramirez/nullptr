CREATE DATABASE TP_IDS;
USE TP_IDS;

-- TABLA DE INCIDENTES - Se comunica con la tabla REPORTES
CREATE TABLE incidentes (
	ID_incidente INT NOT NULL AUTO_INCREMENT,
    tipo_reporte VARCHAR(50) NOT NULL,
    direccion_reporte VARCHAR(100) NOT NULL,
    descripcion VARCHAR(1000) NOT NULL,
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
    provincia VARCHAR(100) NOT NULL,
    departamento VARCHAR(100) NOT NULL,
    localidad VARCHAR(100) NOT NULL,
    fecha_reporte DATE NOT NULL,
    horario_reporte TIME NOT NULL,
    ID_incidente INT,
    ID_usuario INT,
    PRIMARY KEY (ID_reporte),
    FOREIGN KEY (ID_incidente) REFERENCES incidentes(ID_incidente),
    FOREIGN KEY (ID_usuario) REFERENCES usuarios(ID_usuario)
);


-- HARDCODEO DE DATOS - USUARIOS
INSERT INTO usuarios(nombre_usuario, nombre, apellido, email,telefono)
VALUES('lore142', 'Lorena', 'Sanz', 'lorena1@gmail.com', '1134512345');

INSERT INTO usuarios(nombre_usuario, nombre, apellido, email,telefono)
VALUES('mari42l', 'Mariela Raina', 'Marciel', 'mari@hotmail.com', '1131425365');

INSERT INTO usuarios(nombre_usuario, nombre, apellido, email,telefono)
VALUES('bola23', 'Martin', 'Ramiro', 'ramiro@gmail.com', '1132456734');

INSERT INTO usuarios(nombre_usuario, nombre, apellido, email,telefono)
VALUES('boba132', 'Cintia', 'Villaverde', 'villaverde@gmail.com', '1132433254');

INSERT INTO usuarios(nombre_usuario, nombre, apellido, email,telefono)
VALUES('loal13', 'Maria', 'Cantilla', 'maria@gmail.com', '1132124356');

INSERT INTO usuarios(nombre_usuario, nombre, apellido, email,telefono)
VALUES('poll231', 'Iban', 'Vallejos', 'vallejos@hotmail.com', '1143658743');

INSERT INTO usuarios(nombre_usuario, nombre, apellido, email,telefono)
VALUES('buz0', 'Camila', 'Cantino', 'camilacantino@gmail.com', '1143235476');

INSERT INTO usuarios(nombre_usuario, nombre, apellido, email,telefono)
VALUES('holo12', 'Lucas', 'Mancilla', 'mancillalucas@gmail.com', '1132423532');

INSERT INTO usuarios(nombre_usuario, nombre, apellido, email,telefono)
VALUES('koa12', 'Maria', 'Morena', 'morena12@gmail.com', '1143214335');

INSERT INTO usuarios(nombre_usuario, nombre, apellido, email,telefono)
VALUES('pyla53', 'Geraldine', 'Amaro', 'geraldinea@gmail.com', '1143562352');
INSERT INTO usuarios(nombre_usuario, nombre, apellido, email,telefono)
VALUES('lhg45', 'Lizbet', 'Montenegro', 'montenegro45@gmail.com', '1142132435');

INSERT INTO usuarios(nombre_usuario, nombre, apellido, email,telefono)
VALUES('kho43', 'Camilo', 'Roda', 'rodacamilo@gmail.com', '1143235264');

INSERT INTO usuarios(nombre_usuario, nombre, apellido, email,telefono)
VALUES('luz134', 'Luz', 'Bermejo', 'bermejo@hotmail.com', '1124433523');

INSERT INTO usuarios(nombre_usuario, nombre, apellido, email,telefono)
VALUES('luna655', 'Luna', 'Mancila', 'lunam@hotmail.com', '1143524336');

INSERT INTO usuarios(nombre_usuario, nombre, apellido, email,telefono)
VALUES('Mia345', 'Maricielo', 'Camargo', 'camargomaricielo@hotmail.com', '1141324153');

INSERT INTO usuarios(nombre_usuario, nombre, apellido, email,telefono)
VALUES('paks12', 'Priscila', 'Guzman', 'guzmanpriscila@hotmail.com', '1132132143');


-- HARDCODEO DE DATOS - INCIDENTES
INSERT INTO incidentes (tipo_reporte, direccion_reporte, descripcion)
VALUES ('Robo', 'Paseo Colon 850', 'Robo de Apuntes');

INSERT INTO incidentes (tipo_reporte, direccion_reporte, descripcion)
VALUES ('Secuestro', 'Av. Juan de Garay 125', 'Secuestro de vacaciones');

INSERT INTO incidentes (tipo_reporte, direccion_reporte, descripcion)
VALUES ('Asesinato', 'Paseo Colon 750', 'Asesinato de neuronas');

INSERT INTO incidentes (tipo_reporte, direccion_reporte, descripcion)
VALUES ('Asesinato', 'Av. Brasil 800', 'Asesinato de neuronas');


-- HARDCODEO DE DATOS - REPORTES
INSERT INTO reportes (provincia, departamento, localidad, fecha_reporte, horario_reporte, ID_incidente, ID_usuario)
VALUES ('Ciuadad Autonoma de Buenos Aires', 'Comuna 1', 'San Telmo', '2024-04-12', '03:15', 1, 1);

INSERT INTO reportes (provincia, departamento, localidad, fecha_reporte, horario_reporte, ID_incidente, ID_usuario)
VALUES ('Ciuadad Autonoma de Buenos Aires', 'Comuna 1', 'San Telmo', '2022-03-27', '12:15', 2, 1);

INSERT INTO reportes (provincia, departamento, localidad, fecha_reporte, horario_reporte, ID_incidente, ID_usuario)
VALUES ('Ciuadad Autonoma de Buenos Aires', 'Comuna 1', 'San Telmo', '2021-01-27', '04:15', 3, 1);

INSERT INTO reportes (provincia, departamento, localidad, fecha_reporte, horario_reporte, ID_incidente, ID_usuario)
VALUES ('Ciuadad Autonoma de Buenos Aires', 'Comuna 1', 'San Telmo', '2021-01-30', '06:44', 4, 1);
