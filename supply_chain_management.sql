CREATE TABLE `employees` (
  `name` char(255) DEFAULT NULL,
  `pending_work` int DEFAULT NULL,
  `completed_work` int DEFAULT NULL,
  `username` char(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) 

CREATE TABLE `factories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `raw_material` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) 

INSERT INTO `factories` VALUES (1,'Factory1','steel'),(2,'Factory2','plastic');

CREATE TABLE `producer` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `productA_quantity` int NOT NULL DEFAULT '0',
  `productB_quantity` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) 

CREATE TABLE `user_credentials` (
  `username` char(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) 


CREATE TABLE `warehouse` (
  `id` int DEFAULT NULL,
  `product_id` int DEFAULT NULL,
  `product_name` char(255) DEFAULT NULL,
  `price` int DEFAULT NULL,
  `quantity` int DEFAULT NULL
)

INSERT INTO `warehouse` VALUES (1,1,'productA',20,110),(1,2,'productB',10,200),(2,1,'productA',15,130),(2,2,'productB',7,80);
