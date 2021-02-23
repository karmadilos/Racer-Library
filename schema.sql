CREATE DATABASE libraryuser;
USE libraryuser;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `passwd` text NOT NULL,
  PRIMARY KEY (`id`)
);