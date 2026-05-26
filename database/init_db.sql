CREATE DATABASE universidad;
USE universidad;

CREATE TABLE docente (
    id_docente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL 
);

CREATE TABLE programa_academico (
    id_programa INT AUTO_INCREMENT PRIMARY KEY,
    nombre_programa VARCHAR(100) NOT NULL,
    total_semestres INT NOT NULL
);

CREATE TABLE estudiante (
    id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    documento VARCHAR(20) UNIQUE NOT NULL,
    id_programa INT NOT NULL,
    semestre_actual INT NOT NULL,
    estado VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_programa) REFERENCES programa_academico(id_programa)
);

CREATE TABLE asignatura (
    id_asignatura INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    creditos INT NOT NULL,
    id_docente INT NOT NULL,
    FOREIGN KEY (id_docente) REFERENCES docente(id_docente)
);

CREATE TABLE matricula (
    id_matricula INT AUTO_INCREMENT PRIMARY KEY,
    id_estudiante INT NOT NULL,
    id_asignatura INT NOT NULL,
    periodo_academico VARCHAR(20) NOT NULL,
    nota_final DECIMAL(3,1),
    porcentaje_asistencia DECIMAL(5,2),
    FOREIGN KEY (id_estudiante) REFERENCES estudiante(id_estudiante),
    FOREIGN KEY (id_asignatura) REFERENCES asignatura(id_asignatura)
);

CREATE TABLE alerta (
    id_alerta INT AUTO_INCREMENT PRIMARY KEY,
    id_estudiante INT NOT NULL,
    nivel_riesgo VARCHAR(20) NOT NULL,
    fecha_generacion DATE NOT NULL,
    estado VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_estudiante) REFERENCES estudiante(id_estudiante)
);
CREATE TABLE usuario (

    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(255),
    rol VARCHAR(50)

);