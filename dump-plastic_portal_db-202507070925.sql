-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: plastic-portal-db.czw0aqcke793.eu-north-1.rds.amazonaws.com    Database: plastic_portal_db
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '';

--
-- Table structure for table `exchange_rates`
--

DROP TABLE IF EXISTS `exchange_rates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exchange_rates` (
  `id` int NOT NULL AUTO_INCREMENT,
  `currency` varchar(10) NOT NULL,
  `rate` decimal(10,4) NOT NULL,
  `last_updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `currency` (`currency`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exchange_rates`
--

LOCK TABLES `exchange_rates` WRITE;
/*!40000 ALTER TABLE `exchange_rates` DISABLE KEYS */;
INSERT INTO `exchange_rates` VALUES (1,'USD',1.0800,'2025-03-28 14:45:27'),(2,'CNY',7.8670,'2025-03-28 14:34:24');
/*!40000 ALTER TABLE `exchange_rates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logs`
--

DROP TABLE IF EXISTS `logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `activity` text,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs`
--

LOCK TABLES `logs` WRITE;
/*!40000 ALTER TABLE `logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `materials`
--

DROP TABLE IF EXISTS `materials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `materials` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `cost_per_unit` decimal(10,2) NOT NULL,
  `unit` varchar(50) NOT NULL,
  `thickness` decimal(5,2) DEFAULT NULL,
  `width` decimal(10,2) DEFAULT NULL,
  `length` decimal(10,2) DEFAULT NULL,
  `currency` varchar(10) DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  `brand_id` int DEFAULT NULL,
  `quantity` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_material_category` (`category_id`),
  KEY `fk_material_brand` (`brand_id`),
  CONSTRAINT `fk_material_brand` FOREIGN KEY (`brand_id`) REFERENCES `product_brands` (`id`),
  CONSTRAINT `fk_material_category` FOREIGN KEY (`category_id`) REFERENCES `product_categories` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materials`
--

LOCK TABLES `materials` WRITE;
/*!40000 ALTER TABLE `materials` DISABLE KEYS */;
INSERT INTO `materials` VALUES (11,'TGP HC5000',49.81,'nr',1.02,406.40,203.20,'USD',6,6,1),(12,'TSP 900 adesivo 7 mils',3.34,'nr',0.18,304.80,304.80,'USD',2,6,1),(13,'TC900S adesivo 9 mils',1.31,'nr',0.23,300.00,300.00,'USD',2,7,1),(14,'TSP 1600 adesivo 5 mils',6.30,'nr',0.13,304.80,304.80,'USD',2,6,1),(15,'UTP100 adesivo',3.91,'nr',1.00,200.00,400.00,'USD',6,7,1),(16,'TSP 3500 dry 15 mils',101.89,'nr',0.38,304.80,304.80,'USD',2,6,0),(17,'TSP 3500 adesivo 15 mils',216.78,'nr',0.38,304.80,304.80,'USD',2,6,0);
/*!40000 ALTER TABLE `materials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_brands`
--

DROP TABLE IF EXISTS `product_brands`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_brands` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_brands`
--

LOCK TABLES `product_brands` WRITE;
/*!40000 ALTER TABLE `product_brands` DISABLE KEYS */;
INSERT INTO `product_brands` VALUES (7,'AOK'),(6,'Henkel');
/*!40000 ALTER TABLE `product_brands` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_categories`
--

DROP TABLE IF EXISTS `product_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_categories`
--

LOCK TABLES `product_categories` WRITE;
/*!40000 ALTER TABLE `product_categories` DISABLE KEYS */;
INSERT INTO `product_categories` VALUES (6,'Gap Pad'),(2,'Sil Pad');
/*!40000 ALTER TABLE `product_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productions`
--

DROP TABLE IF EXISTS `productions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `setup_cost` decimal(10,2) NOT NULL,
  `cutting_cost_per_sheet` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productions`
--

LOCK TABLES `productions` WRITE;
/*!40000 ALTER TABLE `productions` DISABLE KEYS */;
INSERT INTO `productions` VALUES (1,'Taglio passante a fustella testa piana',20.00,4.00),(2,'Mezzo taglio a fustella testa piana',20.00,4.00),(3,'Taglio passante a plotter',40.00,7.00),(4,'Mezzo taglio a plotter',40.00,7.00),(5,'Mezzo taglio a rotativa',60.00,12.00),(7,'Lavorazione a tornio',30.00,1.00);
/*!40000 ALTER TABLE `productions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quotes`
--

DROP TABLE IF EXISTS `quotes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quotes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `material_id` int NOT NULL,
  `production_id` int NOT NULL,
  `quantity_requested` int NOT NULL,
  `drawing_path` varchar(255) DEFAULT NULL,
  `order_multiple` int DEFAULT NULL,
  `cost_per_element` decimal(10,4) DEFAULT NULL,
  `selling_price` decimal(10,4) DEFAULT NULL,
  `quote_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `expiry_date` date DEFAULT NULL,
  `currency` varchar(10) DEFAULT 'EUR',
  `exchange_rate` decimal(10,4) DEFAULT NULL,
  `element_dimensions_x` decimal(10,2) DEFAULT NULL,
  `element_dimensions_y` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `material_id` (`material_id`),
  KEY `production_id` (`production_id`),
  CONSTRAINT `quotes_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `quotes_ibfk_2` FOREIGN KEY (`material_id`) REFERENCES `materials` (`id`),
  CONSTRAINT `quotes_ibfk_3` FOREIGN KEY (`production_id`) REFERENCES `productions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quotes`
--

LOCK TABLES `quotes` WRITE;
/*!40000 ALTER TABLE `quotes` DISABLE KEYS */;
/*!40000 ALTER TABLE `quotes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `settings`
--

DROP TABLE IF EXISTS `settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `settings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `value` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `settings`
--

LOCK TABLES `settings` WRITE;
/*!40000 ALTER TABLE `settings` DISABLE KEYS */;
INSERT INTO `settings` VALUES (1,'profit_margin','0.5'),(2,'plotter_setup_cost','40'),(3,'plotter_cutting_cost','7'),(4,'fustella_tooling_cost','400'),(5,'fustella_setup_cost','20'),(6,'fustella_cutting_cost','4'),(7,'useless_margin','5');
/*!40000 ALTER TABLE `settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(50) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (3,'gori@weltelectronic.it','scrypt:32768:8:1$3bHu5xiVYnOgKsyI$6be6561ed7fe55954aaa44eb67e887276ad607f4e9e6d315f30520a4d8a9bb4260fbaa49a9f2c95469123d1178001d72cf7fe9191f06ed25963b299eb2b9d8a0','admin','2025-03-25 18:31:23'),(4,'stegori@tiscali.it','scrypt:32768:8:1$eA3iksJDMQ92NRcq$62cfb9c9d005536f4540b1f70f5ca15e1b80cb5547259660eb3716cd4d18eb2eeef982ece891f855307d024830385be2dfdaa68d9eb6d74eb13a7dd7a841399b','user','2025-03-26 08:52:44'),(5,'giusti@weltelectronic.it','scrypt:32768:8:1$tkvHwJO5T23SEN5l$69b7cc43b1559a3038ea9261b08b741279133f6ed9279da94be9b89ad884ada9c77de8fb2232e25db9cc2291e88a62d37a6cac983692eb6ffc36762059b4fdf2','user','2025-03-28 14:48:48'),(6,'test_user@weltelectronic.it','scrypt:32768:8:1$Gf2CGRJJc5tlQEQn$4919bb5fea49d3383f156e8787ff7841d15e11b20f17c32c5a09f945749f597681f89c511112702340858231edc01d4bc8b7f5a4b07a7566c28ef0f8ac762c65','user','2025-03-31 05:52:30');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'plastic_portal_db'
--
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-07  9:25:37
