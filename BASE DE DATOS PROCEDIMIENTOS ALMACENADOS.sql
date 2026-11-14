DELIMITER //
CREATE PROCEDURE sp_RegistrarCliente (
    IN p_id_cliente VARCHAR(10),
    IN p_nombre_cliente VARCHAR(50),
    IN p_correo_secundario VARCHAR(50)
)
BEGIN
    INSERT INTO Cliente (id_cliente, nombre_cliente, correo_secundario)
    VALUES (p_id_cliente, p_nombre_cliente, p_correo_secundario);
END //
CREATE PROCEDURE sp_ActualizarEstadoPieza (
    IN p_id_pieza VARCHAR(10),
    IN p_nuevo_estado VARCHAR(20)
)
BEGIN
    UPDATE Pieza 
    SET estado_conservacion = p_nuevo_estado 
    WHERE id_pieza = p_id_pieza;
END //
CREATE PROCEDURE sp_RegistrarVenta (
    IN p_id_venta VARCHAR(10),
    IN p_fecha_venta DATE,
    IN p_monto_total DECIMAL(10,2),
    IN p_id_cliente VARCHAR(10),
    IN p_id_personal VARCHAR(10)
)
BEGIN
    INSERT INTO Venta (id_venta, fecha_venta, monto_total, id_cliente, id_personal)
    VALUES (p_id_venta, p_fecha_venta, p_monto_total, p_id_cliente, p_id_personal);
END //
CREATE PROCEDURE sp_RegistrarDetalleVenta (
    IN p_id_venta VARCHAR(10),
    IN p_id_detalle_interno VARCHAR(10),
    IN p_id_pieza VARCHAR(10),
    IN p_precio_venta DECIMAL(10,2)
)
BEGIN
    INSERT INTO DetalleVenta (id_venta, id_detalle_interno, id_pieza, precio_venta)
    VALUES (p_id_venta, p_id_detalle_interno, p_id_pieza, p_precio_venta);
END //
CREATE PROCEDURE sp_ConsultarVentasPorCliente (
    IN p_id_cliente VARCHAR(10)
)
BEGIN
    SELECT 
        v.id_venta,
        v.fecha_venta,
        v.monto_total,
        p.nombre_personal AS vendedor
    FROM Venta v
    JOIN Personal p ON v.id_personal = p.id_personal
    WHERE v.id_cliente = p_id_cliente;
END //

DELIMITER ;
DELIMITER //

CREATE PROCEDURE sp_InsertarColeccion (
    IN p_id_coleccion VARCHAR(10),
    IN p_nombre VARCHAR(50),
    IN p_tematica VARCHAR(50),
    IN p_fecha_creacion DATE,
    IN p_responsable VARCHAR(50),
    IN p_estado_conservacion VARCHAR(20)
)
BEGIN
    INSERT INTO Coleccion (id_coleccion, nombre, tematica, fecha_creacion, responsable, estado_conservacion) 
    VALUES (p_id_coleccion, p_nombre, p_tematica, p_fecha_creacion, p_responsable, p_estado_conservacion);
END//

DELIMITER ;