
-- 为了测试暂时，设置为可以空值了。下面那些是测试数据
-- 重要：需要补创建时间字段

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
  PRIMARY KEY (`id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `resource`(
  `course_id` CHAR(20),
  `section_id` CHAR(10) ,
  `unit_id` CHAR(10) ,
  `unit_name` CHAR(80),
  `resource_id` CHAR(10) NOT NULL,
  `resource_type` CHAR(2) ,
  PRIMARY KEY (`resource_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
-- 补充了unit_name字段


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


CREATE TABLE IF NOT EXISTS `download_guidance`(
  `account` CHAR(20),
  `name` CHAR(20) ,
  `course_id` CHAR(20) ,
  `guidance_id` CHAR(20) ,
  `guidance_name` CHAR(40) ,
  PRIMARY KEY ( `account`,`guidance_id` )
  )ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 还需要建立一个所有辅导材料的表...
CREATE TABLE IF NOT EXISTS `guidance`(
  `id` INT NOT NULL AUTO_INCREMENT,
  `course_id` CHAR(20) ,
  `unit_id` CHAR(20) ,
  `section_id` CHAR(20) ,
  `guidance_id` CHAR(20),
  `guidance_name` CHAR(40) ,
  PRIMARY KEY ( `id` )
  )ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 作业时间表
CREATE TABLE IF NOT EXISTS `homeworkTime`(
    `account` CHAR(20),
    `name` CHAR(20) ,
    `course_id` CHAR(20) ,
    `homework_id` CHAR(10) NOT NULL,
    `submit_time` DATETIME,
    PRIMARY KEY ( `homework_id`,`account` )
  )ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- BEGIN;
-- INSERT INTO `learning_progress` (account,name,course_id,unit_id,resource_id,progress,credit) VALUES 
-- ('201630610496','黄基峰','0001','0001-01','123','0.28',5),
-- ('201630610496','黄基峰','0001','0001-01','124','0.85',10),
-- ('201630610496','黄基峰','0001','0001-01','125','0.10',3),
-- ('201630610496','黄基峰','0001','0001-01','126','0.33',5);
-- COMMIT;

-- BEGIN;
-- INSERT INTO `guidance` (course_id,guidance_id,guidance_name) VALUES
--   ('0001','888','恭喜'),
--   ('0001','6666','AC！error0！'),
--   ('0001','776655','额...'),
--   ('0002','159753','非空');
-- COMMIT;

-- BEGIN;
-- INSERT INTO `download_guidance` (account,course_id,guidance_id) VALUES 
-- ('201630610496','0001','888'),
-- ('201630610496','0001','6666'),
-- ('201630610491','0001','776655'),
-- ('201630610491','0002','159753');
-- COMMIT;

-- BEGIN;
-- INSERT INTO `download_materials` (account,materials_id,course_id,name) VALUES
-- ('201630610496','4396123','0001','养猪心得'),
-- ('201630610496','777','0001','2级抓下'),
-- ('201630610496','2800','0001','2级抓下再次出现');
-- COMMIT;

-- BEGIN;
-- INSERT INTO `discussion` (account,course_id,discussion_id,content) VALUES
-- ('201630610496','0001','dis9527','今天的风儿好喧嚣'),
-- ('2016306104961','0001','dis2795','处处好风光，除了C12-346');
-- COMMIT;
-- BEGIN;
-- INSERT INTO `discussion` (account,course_id,discussion_id,post_id,content) VALUES
-- ('201630610496','0001','dis9528','dis9527','emmm'),
-- ('201630610496','0001','dis2796','dis2795','因为我要赶紧做这个呀');
-- COMMIT;

-- BEGIN;
-- INSERT INTO `resource` (course_id,unit_name,resource_id) VALUES
-- ('0001','1+1=？','12345'),
-- ('0001','非线性偏微分方程','12346'),
-- ('0001','试一试！','12347');
-- COMMIT;

-- BEGIN;
-- INSERT INTO `materials` (course_id,materials_id) VALUES
--   ('0001','2800'),
--   ('0001','4396123'),
--   ('0002','443'),
--   ('0001','777');
-- COMMIT;