-- ENREGA 3
CREATE TABLE producto(
id_producto BIGSERIAL NOT NULL PRIMARY KEY,
nombre VARCHAR(20) NOT NULL,
laboratorio VARCHAR(50) NOT NULL,
precio INTEGER NOT NULL,
formato VARCHAR(50) NOT NULL,
receta VARCHAR(15) NOT NULL);

CREATE TABLE productoXserie (
id_producto INTEGER NOT NULL,
id_serie INTEGER NOT NULL);

CREATE TABLE serie(
 id_serie BIGSERIAL NOT NULL PRIMARY KEY,
 n_serie INTEGER NOT NULL,
 lote INTEGER NOT NULL,
 fecha_vencimiento DATE NOT NULL);

CREATE TABLE cliente(
 rut_cliente VARCHAR(10) NOT NULL PRIMARY KEY,
 nombre VARCHAR(20) NOT NULL,
 apellido VARCHAR(20) NOT NULL,
 telefono INTEGER NOT NULL,
 mail VARCHAR(60) NOT NULL,
 contraseña VARCHAR(60) NOT NULL,
 id_login INTEGER NOT NULL);

CREATE TABLE direccion(
 id_direccion BIGSERIAL NOT NULL PRIMARY KEY,
 calle VARCHAR(40) NOT NULL,
 n_domicilio INTEGER NOT NULL,
 comuna VARCHAR(40) NOT NULL);

CREATE TABLE direccionXcliente(
 id_direccion INTEGER NOT NULL,
 rut_cliente VARCHAR(10) NOT NULL);

CREATE TABLE repartidor(
 rut_repartidor VARCHAR(10) NOT NULL PRIMARY KEY,
 nombre VARCHAR(20) NOT NULL,
 apellido VARCHAR(20) NOT NULL,
 telefono INTEGER NOT NULL,
 mail VARCHAR(60) NOT NULL,
 contraseña VARCHAR(60) NOT NULL,
 id_login INTEGER NOT NULL);

CREATE TABLE pedido(
 n_pedido BIGSERIAL NOT NULL PRIMARY KEY,
 rut_repartidor VARCHAR(10) NOT NULL,
 valor_total INTEGER NOT NULL,
 estado VARCHAR(20) NOT NULL);

CREATE TABLE pedidoXcliente(
 n_pedido BIGSERIAL NOT NULL,
 rut_cliente VARCHAR(10) NOT NULL);

CREATE TABLE detalle(
 id_detalle BIGSERIAL NOT NULL PRIMARY KEY,
 rut_cliente INTEGER NOT NULL,
 cantidad INTEGER NOT NULL,
 fecha DATE NOT NULL);

 CREATE TABLE pedidoXdetalle(
 n_pedido INTEGER NOT NULL,
 id_detalle INTEGER NOT NULL);

-- ENREGA 4

SET password_encryption = 'scram-sha-256';


CREATE ROLE administrador WITH LOGIN PASSWORD 'admin';
CREATE ROLE usuario LOGIN PASSWORD 'user';
CREATE ROLE repartidor LOGIN PASSWORD 'rep';

ALTER SCHEMA public RENAME TO home;
CREATE SCHEMA development;

ALTER USER usuario SET search_path TO home,public;
ALTER USER repartidor SET search_path TO home,public;

GRANT CONNECT ON DATABASE farmacia TO administrador;
GRANT CONNECT ON DATABASE farmacia TO usuario;
GRANT CONNECT ON DATABASE farmacia TO repartidor;

REVOKE ALL ON DATABASE farmacia FROM administrador;
REVOKE ALL ON DATABASE farmacia FROM usuario;
REVOKE ALL ON DATABASE farmacia FROM repartidor;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA home TO administrador;

GRANT SELECT ON ALL TABLES IN SCHEMA home TO usuario;
GRANT INSERT, UPDATE, DELETE ON TABLE pedido TO usuario;
GRANT USAGE ON sequence pedido_n_pedido_seq TO usuario;
GRANT INSERT, UPDATE ON TABLE cliente TO usuario;
GRANT INSERT, UPDATE ON TABLE direccion TO usuario;
GRANT USAGE ON sequence pedidoxcliente_n_pedido_seq TO administrador;

GRANT SELECT, INSERT ON TABLE repartidor TO repartidor;
GRANT SELECT, UPDATE ON TABLE pedido TO repartidor;
GRANT SELECT ON TABLE producto TO repartidor;

SET search_path TO home;