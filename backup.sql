-- MySQL dump 10.13  Distrib 9.3.0, for macos15.4 (arm64)
--
-- Host: localhost    Database: work_logs
-- ------------------------------------------------------
-- Server version	8.0.42

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

--
-- Table structure for table `cutting_logs`
--

DROP TABLE IF EXISTS `cutting_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cutting_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `line` varchar(10) DEFAULT NULL,
  `job_number` varchar(50) DEFAULT NULL,
  `qty` int DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cutting_logs`
--

LOCK TABLES `cutting_logs` WRITE;
/*!40000 ALTER TABLE `cutting_logs` DISABLE KEYS */;
INSERT INTO `cutting_logs` VALUES (1,'Line 1','999999',1000,'2025-06-01 10:51:49');
/*!40000 ALTER TABLE `cutting_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_tracker`
--

DROP TABLE IF EXISTS `order_tracker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_tracker` (
  `job_number` varchar(50) NOT NULL,
  `my_date` date DEFAULT NULL,
  `num_lines` int DEFAULT NULL,
  PRIMARY KEY (`job_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_tracker`
--

LOCK TABLES `order_tracker` WRITE;
/*!40000 ALTER TABLE `order_tracker` DISABLE KEYS */;
INSERT INTO `order_tracker` VALUES ('999999','2025-06-02',3);
/*!40000 ALTER TABLE `order_tracker` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pack_logs`
--

DROP TABLE IF EXISTS `pack_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pack_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `line` varchar(10) DEFAULT NULL,
  `job_number` varchar(50) DEFAULT NULL,
  `qty` int DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pack_logs`
--

LOCK TABLES `pack_logs` WRITE;
/*!40000 ALTER TABLE `pack_logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `pack_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `polish_logs`
--

DROP TABLE IF EXISTS `polish_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `polish_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `line` varchar(10) DEFAULT NULL,
  `job_number` varchar(50) DEFAULT NULL,
  `qty` int DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `polish_logs`
--

LOCK TABLES `polish_logs` WRITE;
/*!40000 ALTER TABLE `polish_logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `polish_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prep_logs`
--

DROP TABLE IF EXISTS `prep_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prep_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `line` varchar(10) DEFAULT NULL,
  `job_number` varchar(50) DEFAULT NULL,
  `qty` int DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prep_logs`
--

LOCK TABLES `prep_logs` WRITE;
/*!40000 ALTER TABLE `prep_logs` DISABLE KEYS */;
INSERT INTO `prep_logs` VALUES (1,'Line 1','999999',1000,'2025-06-01 10:51:32');
/*!40000 ALTER TABLE `prep_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scope_logs`
--

DROP TABLE IF EXISTS `scope_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `scope_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `line` varchar(10) DEFAULT NULL,
  `job_number` varchar(50) DEFAULT NULL,
  `qty` int DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scope_logs`
--

LOCK TABLES `scope_logs` WRITE;
/*!40000 ALTER TABLE `scope_logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `scope_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `term_logs`
--

DROP TABLE IF EXISTS `term_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `term_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `line` varchar(10) DEFAULT NULL,
  `job_number` varchar(50) DEFAULT NULL,
  `qty` int DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `term_logs`
--

LOCK TABLES `term_logs` WRITE;
/*!40000 ALTER TABLE `term_logs` DISABLE KEYS */;
INSERT INTO `term_logs` VALUES (1,'Line 1','999999',500,'2025-06-01 10:50:46'),(2,'Line 2','999999',500,'2025-06-01 10:51:10');
/*!40000 ALTER TABLE `term_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test_logs`
--

DROP TABLE IF EXISTS `test_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `line` varchar(10) DEFAULT NULL,
  `job_number` varchar(50) DEFAULT NULL,
  `qty` int DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test_logs`
--

LOCK TABLES `test_logs` WRITE;
/*!40000 ALTER TABLE `test_logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `test_logs` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-01 14:35:47
