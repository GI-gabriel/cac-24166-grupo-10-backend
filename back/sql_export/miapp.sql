-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 25-06-2024 a las 22:28:16
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `miapp`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `brokers`
--

CREATE TABLE `brokers` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `mail` varchar(255) NOT NULL,
  `telefono` varchar(255) NOT NULL,
  `url_foto` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `brokers`
--

INSERT INTO `brokers` (`id`, `nombre`, `mail`, `telefono`, `url_foto`) VALUES
(1, 'John Doe', 'john.doe@example.com', '123-456-7890', './static/img/brokers/m1.jpg'),
(2, 'Jane Smith', 'jane.smith@example.com', '987-654-3210', './static/img/brokers/f1.jpg'),
(3, 'Alice Johnson', 'alice.johnson@example.com', '555-123-4567', './static/img/brokers/f2.jpg'),
(4, 'Bob Brown', 'bob.brown@example.com', '555-987-6543', './static/img/brokers/m2.jpg'),
(5, 'Carol White', 'carol.white@example.com', '555-555-5555', './static/img/brokers/f3.jpg'),
(6, 'David Black', 'david.black@example.com', '555-444-3333', './static/img/brokers/m3.jpg'),
(7, 'Eva Green', 'eva.green@example.com', '555-222-1111', './static/img/brokers/f4.jpg'),
(8, 'Frank Blue', 'frank.blue@example.com', '555-666-7777', './static/img/brokers/m4.jpg'),
(9, 'Grace Yellow', 'grace.yellow@example.com', '555-888-9999', './static/img/brokers/f5.jpg'),
(10, 'Hank Red', 'hank.red@example.com', '555-000-1111', './static/img/brokers/m5.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `propiedades`
--

CREATE TABLE `propiedades` (
  `id` int(11) NOT NULL,
  `descrip_corta` varchar(255) NOT NULL,
  `descrip_larga` varchar(2048) NOT NULL,
  `direccion` varchar(255) NOT NULL,
  `nota` varchar(255) NOT NULL,
  `url_foto_1` varchar(255) NOT NULL,
  `url_foto_2` varchar(255) NOT NULL,
  `url_foto_3` varchar(255) NOT NULL,
  `url_maps` varchar(255) NOT NULL,
  `id_broker` int(11) DEFAULT NULL,
  `precio` decimal(10,2) NOT NULL,
  `superf` int(11) DEFAULT NULL,
  `superf_tot` int(11) DEFAULT NULL,
  `baños` int(11) DEFAULT NULL,
  `dormitorios` int(11) DEFAULT NULL,
  `cocheras` int(11) DEFAULT NULL,
  `basicos` varchar(1024) NOT NULL,
  `servicios` varchar(1024) NOT NULL,
  `amenities` varchar(1024) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `brokers`
--
ALTER TABLE `brokers`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `propiedades`
--
ALTER TABLE `propiedades`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `brokers`
--
ALTER TABLE `brokers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `propiedades`
--
ALTER TABLE `propiedades`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
