-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: localhost    Database: sonuresults
-- ------------------------------------------------------
-- Server version	8.0.32

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
-- Table structure for table `a_register`
--

DROP TABLE IF EXISTS `a_register`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `a_register` (
  `user` varchar(30) NOT NULL,
  `email` varchar(30) DEFAULT NULL,
  `password` varchar(10) DEFAULT NULL,
  `ccode` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `a_register`
--

LOCK TABLES `a_register` WRITE;
/*!40000 ALTER TABLE `a_register` DISABLE KEYS */;
INSERT INTO `a_register` VALUES ('daya','abduljasmin733@gmail.com','hhh','admin@123'),('eswar','eswar@codegnan.com','2001','admin@123'),('kkkk','mounikamurikipudi333@gmail.com','kkk','admin@123'),('sonu','dayasagar333@gmail.com','ggg','admin@333');
/*!40000 ALTER TABLE `a_register` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `addstu`
--

DROP TABLE IF EXISTS `addstu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `addstu` (
  `studentid` varchar(10) NOT NULL,
  `studentname` varchar(30) DEFAULT NULL,
  `section` varchar(20) DEFAULT NULL,
  `mobile` bigint NOT NULL,
  `Address` varchar(50) DEFAULT NULL,
  `Department` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`studentid`),
  UNIQUE KEY `mobile` (`mobile`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `addstu`
--

LOCK TABLES `addstu` WRITE;
/*!40000 ALTER TABLE `addstu` DISABLE KEYS */;
INSERT INTO `addstu` VALUES ('197208','Eswar','B.Sc M.S.Ds',9177806313,'vij','it'),('201','mouni','B.Sc M.S.Ds',3333,'vij','computer');
/*!40000 ALTER TABLE `addstu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `addsub`
--

DROP TABLE IF EXISTS `addsub`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `addsub` (
  `courseid` varchar(20) NOT NULL,
  `coursetitle` varchar(20) DEFAULT NULL,
  `maxmarks` bigint DEFAULT NULL,
  PRIMARY KEY (`courseid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `addsub`
--

LOCK TABLES `addsub` WRITE;
/*!40000 ALTER TABLE `addsub` DISABLE KEYS */;
INSERT INTO `addsub` VALUES ('BBA0T3','telugu',75),('BCAE01','Theory',75),('BCAOO1','telugu Theory',80),('MATT35','Group Theory',75);
/*!40000 ALTER TABLE `addsub` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contactus`
--

DROP TABLE IF EXISTS `contactus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contactus` (
  `name` varchar(30) DEFAULT NULL,
  `emailid` varchar(40) DEFAULT NULL,
  `message` tinytext,
  `date` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contactus`
--

LOCK TABLES `contactus` WRITE;
/*!40000 ALTER TABLE `contactus` DISABLE KEYS */;
INSERT INTO `contactus` VALUES ('sonu','dayasagar333@gmail.com','Please bring more placements','2023-04-30 15:28:24'),('eswar','eswar@codegnan.com','Please provide better cafeteria','2023-04-30 15:32:19');
/*!40000 ALTER TABLE `contactus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `internalresults`
--

DROP TABLE IF EXISTS `internalresults`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `internalresults` (
  `studentid` varchar(10) NOT NULL,
  `courseid` varchar(20) NOT NULL,
  `Internal1` enum('Internal1') DEFAULT NULL,
  `Internal2` enum('Internal2') DEFAULT NULL,
  `internalmarks2` smallint DEFAULT NULL,
  `internalmarks1` smallint DEFAULT NULL,
  `section` enum('BCA','B.Sc M.S.Ds','BBA','BBA BA','BA','BSC MPCs','B.Sc C.A.M.E','B.Sc M.S.Cs') DEFAULT NULL,
  PRIMARY KEY (`studentid`,`courseid`),
  KEY `courseid` (`courseid`),
  CONSTRAINT `internalresults_ibfk_1` FOREIGN KEY (`studentid`) REFERENCES `addstu` (`studentid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `internalresults`
--

LOCK TABLES `internalresults` WRITE;
/*!40000 ALTER TABLE `internalresults` DISABLE KEYS */;
INSERT INTO `internalresults` VALUES ('197208','BCAOO1','Internal1','Internal2',10,10,'BCA'),('201','BBA0T3','Internal1','Internal2',10,10,'BCA'),('201','BCAOO1','Internal1','Internal2',20,30,'B.Sc M.S.Ds');
/*!40000 ALTER TABLE `internalresults` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `semresults`
--

DROP TABLE IF EXISTS `semresults`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `semresults` (
  `studentid` varchar(10) NOT NULL,
  `courseid` varchar(20) NOT NULL,
  `Semister` enum('sem1','sem2','sem3','sem4','sem5','sem6') DEFAULT NULL,
  `Semmarks` int DEFAULT NULL,
  `section` enum('BCA','B.Sc M.S.Ds','BBA','BBA BA','BA','BSC MPCs','B.Sc C.A.M.E','B.Sc M.S.Cs') DEFAULT NULL,
  PRIMARY KEY (`studentid`,`courseid`),
  KEY `courseid` (`courseid`),
  CONSTRAINT `semresults_ibfk_1` FOREIGN KEY (`studentid`) REFERENCES `addstu` (`studentid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `semresults`
--

LOCK TABLES `semresults` WRITE;
/*!40000 ALTER TABLE `semresults` DISABLE KEYS */;
INSERT INTO `semresults` VALUES ('197208','BCAE01','sem1',70,'BCA'),('197208','BCAOO1','sem3',45,'BCA'),('201','BBA0T3','sem1',70,'BCA'),('201','BCAOO1','sem1',50,'B.Sc M.S.Ds');
/*!40000 ALTER TABLE `semresults` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-18 15:32:47
