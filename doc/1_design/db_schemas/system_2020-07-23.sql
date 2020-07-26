# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.5.5-10.4.12-MariaDB)
# Database: system
# Generation Time: 2020-07-23 14:22:07 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table msss_session
# ------------------------------------------------------------

DROP TABLE IF EXISTS `msss_session`;

CREATE TABLE `msss_session` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` varchar(45) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `init_time` datetime NOT NULL DEFAULT current_timestamp(),
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `status` int(4) NOT NULL DEFAULT 0 COMMENT '0: Created;\n1: Started;\n2: Crashed;\n3: UserCanceled;\n4: Finished;',
  `note` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `instance_id_UNIQUE` (`instance_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table msss_session_input
# ------------------------------------------------------------

DROP TABLE IF EXISTS `msss_session_input`;

CREATE TABLE `msss_session_input` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `index` int(11) NOT NULL DEFAULT 0,
  `fk_session_id` int(11) NOT NULL,
  `note` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX (`index`, `fk_session_id`),
  CONSTRAINT `ss_input_fk_session_id_2_session` FOREIGN KEY (`fk_session_id`) REFERENCES `msss_session` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table msss_session_input_value
# ------------------------------------------------------------

DROP TABLE IF EXISTS `msss_session_input_value`;

CREATE TABLE `msss_session_input_value` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fk_session_input_id` int(11) NOT NULL,
  `key` varchar(64) NOT NULL,
  `index` int(11) NOT NULL,
  `data_type` int(11) NOT NULL,
  `v1` varchar(64) DEFAULT NULL,
  `v2` varchar(64) DEFAULT NULL,
  `v3` varchar(512) DEFAULT NULL COMMENT 'Put json config/list here.',
  PRIMARY KEY (`id`),
  KEY `ss_pv_fk_session_input_id_2_session_input_idx` (`fk_session_input_id`),
  CONSTRAINT `ss_pv_fk_session_input_id_2_session_input` FOREIGN KEY (`fk_session_input_id`) REFERENCES `msss_session_input` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table msss_session_parameter
# ------------------------------------------------------------

DROP TABLE IF EXISTS `msss_session_parameter`;

CREATE TABLE `msss_session_parameter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `index` int(11) NOT NULL DEFAULT 0,
  `fk_session_id` int(11) NOT NULL,
  `note` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX (`index`, `fk_session_id`),
  CONSTRAINT `ss_parameter_fk_session_id_2_session` FOREIGN KEY (`fk_session_id`) REFERENCES `msss_session` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table msss_session_parameter_value
# ------------------------------------------------------------

DROP TABLE IF EXISTS `msss_session_parameter_value`;

CREATE TABLE `msss_session_parameter_value` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fk_session_parameter_id` int(11) NOT NULL,
  `key` varchar(64) NOT NULL,
  `index` int(11) NOT NULL,
  `data_type` int(11) NOT NULL,
  `v1` varchar(64) DEFAULT NULL,
  `v2` varchar(64) DEFAULT NULL,
  `v3` varchar(512) DEFAULT NULL COMMENT 'Put json config/list here.',
  PRIMARY KEY (`id`),
  KEY `ss_pv_fk_session_parameter_id_2_session_parameter_idx` (`fk_session_parameter_id`),
  CONSTRAINT `ss_pv_fk_session_parameter_id_2_session_parameter` FOREIGN KEY (`fk_session_parameter_id`) REFERENCES `msss_session_parameter` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table msss_session_output
# ------------------------------------------------------------

DROP TABLE IF EXISTS `msss_session_output`;

CREATE TABLE `msss_session_output` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `index` int(11) NOT NULL DEFAULT 0,
  `fk_session_id` int(11) NOT NULL,
  `note` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX (`index`, `fk_session_id`),
  CONSTRAINT `ss_output_fk_session_id_2_session` FOREIGN KEY (`fk_session_id`) REFERENCES `msss_session` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table msss_session_output_value
# ------------------------------------------------------------

DROP TABLE IF EXISTS `msss_session_output_value`;

CREATE TABLE `msss_session_output_value` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fk_session_output_id` int(11) NOT NULL,
  `key` varchar(64) NOT NULL,
  `index` int(11) NOT NULL,
  `data_type` int(11) NOT NULL,
  `v1` varchar(64) DEFAULT NULL,
  `v2` varchar(64) DEFAULT NULL,
  `v3` varchar(512) DEFAULT NULL COMMENT 'Put json config/list here.',
  PRIMARY KEY (`id`),
  KEY `ss_pv_fk_session_output_id_2_session_output_idx` (`fk_session_output_id`),
  CONSTRAINT `ss_pv_fk_session_output_id_2_session_output` FOREIGN KEY (`fk_session_output_id`) REFERENCES `msss_session_output` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
