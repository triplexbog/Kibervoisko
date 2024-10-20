-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3308
-- Время создания: Окт 20 2024 г., 11:35
-- Версия сервера: 8.0.30
-- Версия PHP: 8.0.22

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `Mail_DNR`
--

-- --------------------------------------------------------

--
-- Структура таблицы `services`
--

CREATE TABLE `services` (
  `id` int NOT NULL,
  `name` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Дамп данных таблицы `services`
--

INSERT INTO `services` (`id`, `name`) VALUES
(1, 'Почтовые отправления'),
(2, 'Почтовые переводы'),
(3, 'Платежи'),
(4, 'Стартовые пакеты мобильных операторов');

-- --------------------------------------------------------

--
-- Структура таблицы `talon`
--

CREATE TABLE `talon` (
  `talon_number` int NOT NULL,
  `date_talon` datetime NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `servicesid` int NOT NULL,
  `completed` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Дамп данных таблицы `talon`
--

INSERT INTO `talon` (`talon_number`, `date_talon`, `phone_number`, `servicesid`, `completed`) VALUES
(2, '2024-10-20 09:06:21', '', 1, 0),
(3, '2024-10-20 09:06:43', '', 3, 0),
(4, '2024-10-20 09:22:39', '', 4, 0),
(5, '2024-10-20 09:22:50', '', 4, 0),
(6, '2024-10-20 09:25:10', '', 4, 0),
(7, '2024-10-20 09:26:00', '', 4, 0),
(8, '2024-10-20 09:26:28', '', 4, 0),
(9, '2024-10-20 09:27:36', '', 4, 0),
(10, '2024-10-20 09:40:23', '1006702079', 1, 0),
(11, '2024-10-20 09:40:56', '1006702079', 1, 0),
(12, '2024-10-23 10:00:00', '+380713488047', 4, 0),
(13, '2024-10-23 13:00:00', '+380713488047', 2, 0),
(14, '2024-10-23 13:30:00', '+380713488047', 2, 0),
(15, '2024-10-28 14:15:00', '+380713488047', 1, 0),
(16, '2024-10-24 17:45:00', '+380713488047', 4, 0),
(17, '2024-10-20 10:09:41', '', 2, 0),
(18, '2024-10-20 10:11:33', '', 4, 0),
(19, '2024-10-20 11:31:18', '', 2, 0),
(20, '2024-10-24 14:45:00', '+380713488047', 3, 0);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `services`
--
ALTER TABLE `services`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `talon`
--
ALTER TABLE `talon`
  ADD PRIMARY KEY (`talon_number`),
  ADD KEY `fk_services` (`servicesid`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `services`
--
ALTER TABLE `services`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT для таблицы `talon`
--
ALTER TABLE `talon`
  MODIFY `talon_number` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `talon`
--
ALTER TABLE `talon`
  ADD CONSTRAINT `fk_services` FOREIGN KEY (`servicesid`) REFERENCES `services` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
