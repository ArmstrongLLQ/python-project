/*
Navicat MySQL Data Transfer

Source Server         : doaj
Source Server Version : 50717
Source Host           : 172.16.155.11:3306
Source Database       : doaj

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2017-09-01 16:44:35
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for doaj_data
-- ----------------------------
DROP TABLE IF EXISTS `doaj_data`;
CREATE TABLE `doaj_data` (
  `id` int(11) NOT NULL,
  `title` text,
  `title_translation` text,
  `abstract` text,
  `abstract_translation` text,
  `year` year(4) DEFAULT NULL,
  `url` text,
  `start_page` varchar(100) DEFAULT NULL,
  `end_page` varchar(100) DEFAULT NULL,
  `article_created_date` text,
  `article_last_updated` text,
  `journals_publisher` text,
  `journals_language` varchar(100) DEFAULT NULL,
  `journals_licenseId` int(11) DEFAULT NULL,
  `journals_title` text,
  `journals_country` text,
  `journals_number` text,
  `journals_volume` text,
  `journals_issns` text,
  `journals_create_date` text,
  `term` text,
  `term_code` text,
  `term_l1` text,
  `keyword` text,
  `keyword_translation` text,
  `author_name` text,
  `author_affiliation` text,
  `author_email` text,
  `identifier_type` text,
  `identifier_identifierId` text,
  `license_type` text,
  `license_title` text,
  `license_url` text,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
