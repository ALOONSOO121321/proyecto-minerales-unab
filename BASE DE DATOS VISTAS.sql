CREATE VIEW Vista_DetallePiezas AS
SELECT 
    p.id_pieza,
    p.nombre_comercial,
    p.tipo_pieza,
    p.procedencia_geografica,
    p.fecha_adquisicion,
    p.valor_estimado,
    p.estado_conservacion,
    p.nivel_rareza,
    c.nombre AS nombre_coleccion,
    m.sistema_cristalino,
    m.dureza_mohs,
    f.periodo_geologico,
    f.especie_prehistorica,
    g.corte,
    g.quilates,
    g.pureza
FROM Pieza p
LEFT JOIN Coleccion c ON p.id_coleccion = c.id_coleccion
LEFT JOIN Mineral m ON p.id_pieza = m.id_pieza
LEFT JOIN Fosil f ON p.id_pieza = f.id_pieza
LEFT JOIN Gema g ON p.id_pieza = g.id_pieza;
CREATE VIEW Vista_ResumenVentas AS
SELECT 
    v.id_venta,
    v.fecha_venta,
    c.nombre_cliente,
    c.correo_secundario,
    p.nombre_personal AS vendedor,
    p.rol AS rol_vendedor,
    v.monto_total
FROM Venta v
JOIN Cliente c ON v.id_cliente = c.id_cliente
JOIN Personal p ON v.id_personal = p.id_personal;
CREATE VIEW Vista_ExposicionesPiezas AS
SELECT 
    e.id_exposicion,
    e.nombre_exposicion,
    e.fecha_inicio,
    e.fecha_fin,
    pe.id_pieza,
    p.nombre_comercial,
    pe.ubicacion,
    pe.estado_conservacion AS estado_en_expo,
    pe.observaciones
FROM ParticipacionExposicion pe
JOIN Exposicion e ON pe.id_exposicion = e.id_exposicion
JOIN Pieza p ON pe.id_pieza = p.id_pieza;
CREATE VIEW Vista_PromedioEvaluaciones AS
SELECT 
    v.id_venta,
    v.fecha_venta,
    c.nombre_cliente,
    COUNT(ev.correlativo_evaluacion) AS total_evaluaciones,
    ROUND(AVG(ev.calificacion), 2) AS calificacion_promedio
FROM Venta v
JOIN Cliente c ON v.id_cliente = c.id_cliente
LEFT JOIN Evaluacion ev ON v.id_venta = ev.id_venta
GROUP BY v.id_venta, v.fecha_venta, c.nombre_cliente;
CREATE VIEW Vista_DetalleVentasCompleto AS
SELECT 
    dv.id_venta, 
    dv.id_detalle_interno, 
    p.id_pieza, 
    p.nombre_comercial, 
    p.tipo_pieza, 
    dv.precio_venta
FROM DetalleVenta dv
JOIN Pieza p ON dv.id_pieza = p.id_pieza;
CREATE VIEW Vista_ColeccionesResumen AS
SELECT 
    c.id_coleccion, 
    c.nombre, 
    c.tematica, 
    c.responsable,
    COUNT(p.id_pieza) AS total_piezas,
    SUM(p.valor_estimado) AS valor_total_coleccion
FROM Coleccion c
LEFT JOIN Pieza p ON c.id_coleccion = p.id_coleccion
GROUP BY c.id_coleccion, c.nombre, c.tematica, c.responsable;