CREATE TABLE Coleccion (
    id_coleccion VARCHAR(10) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tematica VARCHAR(100) NOT NULL,
    fecha_creacion DATE NOT NULL,
    responsable VARCHAR(100) NOT NULL,
    estado_conservacion VARCHAR(50) NOT NULL
);
CREATE TABLE Cliente (
    id_cliente VARCHAR(10) PRIMARY KEY,
    nombre_cliente VARCHAR(100) NOT NULL,
    correo_secundario VARCHAR(100) NULL -- Regla de negocio opcional
);
CREATE TABLE Personal (
    id_personal VARCHAR(10) PRIMARY KEY,
    nombre_personal VARCHAR(100) NOT NULL,
    rol VARCHAR(50) NOT NULL
);
CREATE TABLE Pieza (
    id_pieza VARCHAR(10) PRIMARY KEY,
    nombre_comercial VARCHAR(100) NOT NULL,
    procedencia_geografica VARCHAR(100) NOT NULL,
    fecha_adquisicion DATE NOT NULL,
    valor_estimado DECIMAL(12, 2) NOT NULL,
    estado_conservacion VARCHAR(50) NOT NULL,
    nivel_rareza VARCHAR(50) NOT NULL,
    tipo_pieza VARCHAR(20) NOT NULL CHECK (tipo_pieza IN ('Mineral', 'Fosil', 'Gema', 'Sin Clasificar')),
    id_coleccion VARCHAR(10) NOT NULL,
    CONSTRAINT fk_pieza_coleccion FOREIGN KEY (id_coleccion) REFERENCES Coleccion(id_coleccion)
);
CREATE TABLE Mineral (
    id_pieza VARCHAR(10) PRIMARY KEY,
    sistema_cristalino VARCHAR(50),
    dureza_mohs DECIMAL(3,1),
    CONSTRAINT fk_mineral_pieza FOREIGN KEY (id_pieza) REFERENCES Pieza(id_pieza) ON DELETE CASCADE
);
CREATE TABLE Fosil (
    id_pieza VARCHAR(10) PRIMARY KEY,
    periodo_geologico VARCHAR(50),
    especie_prehistorica VARCHAR(100),
    CONSTRAINT fk_fosil_pieza FOREIGN KEY (id_pieza) REFERENCES Pieza(id_pieza) ON DELETE CASCADE
);
CREATE TABLE Gema (
    id_pieza VARCHAR(10) PRIMARY KEY,
    corte VARCHAR(50),
    quilates DECIMAL(6,2),
    pureza VARCHAR(50),
    CONSTRAINT fk_gema_pieza FOREIGN KEY (id_pieza) REFERENCES Pieza(id_pieza) ON DELETE CASCADE
);
CREATE TABLE Exposicion (
    id_exposicion VARCHAR(10) PRIMARY KEY,
    nombre_exposicion VARCHAR(100) NOT NULL,
    fecha_inicio DATE,
    fecha_fin DATE
);
CREATE TABLE ParticipacionExposicion (
    id_pieza VARCHAR(10),
    id_exposicion VARCHAR(10),
    fecha_incorporacion DATE NOT NULL,
    ubicacion VARCHAR(100) NOT NULL,
    estado_conservacion VARCHAR(50) NOT NULL,
    observaciones TEXT,
    PRIMARY KEY (id_pieza, id_exposicion),
    CONSTRAINT fk_participacion_pieza FOREIGN KEY (id_pieza) REFERENCES Pieza(id_pieza),
    CONSTRAINT fk_participacion_exposicion FOREIGN KEY (id_exposicion) REFERENCES Exposicion(id_exposicion)
);
CREATE TABLE Venta (
    id_venta VARCHAR(10) PRIMARY KEY,
    fecha_venta DATE NOT NULL,
    monto_total DECIMAL(12, 2) NOT NULL,
    id_cliente VARCHAR(10) NOT NULL,
    id_personal VARCHAR(10) NOT NULL,
    CONSTRAINT fk_venta_cliente FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
    CONSTRAINT fk_venta_gestor FOREIGN KEY (id_personal) REFERENCES Personal(id_personal)
);
CREATE TABLE DetalleVenta (
    id_venta VARCHAR(10),
    id_detalle_interno VARCHAR(10), -- Correlativo interno por venta (ej. DV01, DV02)
    id_pieza VARCHAR(10) NOT NULL,
    precio_venta DECIMAL(12, 2) NOT NULL,
    PRIMARY KEY (id_venta, id_detalle_interno),
    CONSTRAINT fk_detalle_venta FOREIGN KEY (id_venta) REFERENCES Venta(id_venta) ON DELETE CASCADE,
    CONSTRAINT fk_detalle_pieza FOREIGN KEY (id_pieza) REFERENCES Pieza(id_pieza)
);
CREATE TABLE Evaluacion (
    id_venta VARCHAR(10),
    correlativo_evaluacion INT,
    fecha_evaluacion DATE NOT NULL,
    calificacion INT CHECK (calificacion BETWEEN 1 AND 5),
    comentario TEXT,
    PRIMARY KEY (id_venta, correlativo_evaluacion),
    CONSTRAINT fk_evaluacion_venta FOREIGN KEY (id_venta) REFERENCES Venta(id_venta) ON DELETE CASCADE
);
ALTER TABLE Venta 
ADD id_pieza VARCHAR(10) NOT NULL;
ALTER TABLE Venta 
ADD CONSTRAINT fk_venta_pieza FOREIGN KEY (id_pieza) REFERENCES Pieza(id_pieza);