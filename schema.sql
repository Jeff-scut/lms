
-- 为了测试暂时，设置为可以空值了。下面那些是测试数据

CREATE TABLE IF NOT EXISTS `learning_progress`(
  `id` INT NOT NULL AUTO_INCREMENT,
  `account` CHAR(20) NOT NULL,
  `name` CHAR(20) ,
  `course_id` CHAR(20) ,
  `section_id` CHAR(10) ,
  `unit_id` CHAR(10),
  `resource_id` CHAR(10) ,
  `resource_type` CHAR(2) ,
  `progress` CHAR(5) ,
  `credit` INT ,
  PRIMARY KEY ( `account`,`id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `resource`(
  `course_id` CHAR(20),
  `section_id` CHAR(10) ,
  `unit_id` CHAR(10) ,
  `resource_id` CHAR(10) NOT NULL,
  `resource_type` CHAR(2) ,
  PRIMARY KEY (`resource_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `download_materials`(
  `account` CHAR(20) NOT NULL,
  `name` CHAR(20) ,
  `course_id` CHAR(20),
  `materials_id` CHAR(10) NOT NULL,
  `materials_name` CHAR(50),
  PRIMARY KEY (`account`,`materials_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;



CREATE TABLE IF NOT EXISTS `materials`(
  `course_id` CHAR(20) ,
  `materials_id` CHAR(10) NOT NULL,
  `materials_name` CHAR(50),
  PRIMARY KEY ( `materials_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;



CREATE TABLE IF NOT EXISTS `discussion`(
  `id` INT NOT NULL AUTO_INCREMENT,
  `account` CHAR(20) ,
  `name` CHAR(20) ,
  `course_id` CHAR(20) ,
  `discussion_id` CHAR(10) ,
  `post_id` CHAR(10),
  `content` TEXT,
  PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `guidance`(
  `id` INT NOT NULL AUTO_INCREMENT,
  `account` CHAR(20),
  `name` CHAR(20) ,
  `course_id` CHAR(20) ,
  `unit_id` CHAR(20) ,
  `section_id` CHAR(20) ,
  `guidance_name` CHAR(40) ,
  PRIMARY KEY ( `id` )
  )ENGINE=InnoDB DEFAULT CHARSET=utf8;

BEGIN;
INSERT INTO `learning_progress` VALUES ('201630610496','黄基峰','0001','0001-01','0001-01-01','123','0','0.28',5),
('201630610496','黄基峰','0001','0001-01','0001-01-01','124','0','0.85',10),
('201630610496','黄基峰','0001','0001-01','0001-01-01','125','0','0.10',3),
('201630610496','黄基峰','0001','0001-01','0001-01-01','126','0','0.33',5);
COMMIT;

BEGIN;
INSERT INTO `guidance` (account,section_id) VALUES ('201630610496','66678'),
('201630610496','123321'),
('201630610491','211'),
('201630610491','958');
COMMIT;

BEGIN;
INSERT INTO `download_materials` (account,materials_id,course_id,name) VALUES
('201630610496','4396123','0001','养猪心得'),
('201630610496','777','0001','2级抓下'),
('201630610496','2800','0001','2级抓下再次出现');
COMMIT;

BEGIN;
INSERT INTO `discussion` (account,course_id,discussion_id,content) VALUES
('201630610496','0001','dis9527','今天的风儿好喧嚣'),
('2016306104961','0001','dis2795','处处好风光，除了C12-346');
COMMIT;
BEGIN;
INSERT INTO `discussion` (account,course_id,discussion_id,post_id,content) VALUES
('201630610496','0001','dis9528','dis9527','emmm'),
('201630610496','0001','dis2796','dis2795','因为我要赶紧做这个呀');
COMMIT;