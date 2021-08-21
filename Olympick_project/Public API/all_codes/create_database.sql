CREATE DATABASE olympick;
USE olympick;

CREATE TABLE `schedule` (
  `username` varchar(45),
  `sport` varchar(45) DEFAULT NULL,
  `event` varchar(200) DEFAULT NULL,
  `beginning` varchar(45) DEFAULT NULL,
  `end` varchar(45) DEFAULT NULL,
  `password` varchar(45)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;