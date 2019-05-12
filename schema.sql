
-- 为了测试暂时，设置为可以空值了。下面那些是测试数据

-- 资源表，即每个教学元素对应的pdf/视频
CREATE TABLE IF NOT EXISTS `resource`(
  `id` INT NOT NULL AUTO_INCREMENT,
  `course_id` CHAR(20),
  `section_id` CHAR(10) ,
  `unit_id` CHAR(20) ,
  `unit_name` CHAR(80),
  `resource_id` CHAR(10) NOT NULL,
  `resource_type` CHAR(2) ,
  PRIMARY KEY (`id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
-- 这个是可以更换的，所以需要注意添加update操作.而且可以既放视频又放pdf
-- BEGIN;
--   INSERT INTO `resource` (course_id,unit_id,unit_name,resource_id) VALUES
--   ('0001','d1j','1+1=？','12345'),
--   ('0001','d2j','非线性偏微分方程','12346'),
--   ('0001','d3j','试一试！','12347');
-- COMMIT;

-- 课程资源库中的可供下载的学习材料
CREATE TABLE IF NOT EXISTS `materials`(
  `id` INT NOT NULL AUTO_INCREMENT,
  `course_id` CHAR(20) ,
  `materials_id` CHAR(10) NOT NULL,
  `materials_name` CHAR(50),
  PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
-- BEGIN;
--   INSERT INTO `materials` (course_id,materials_id) VALUES
--     ('0001','2800'),
--     ('0001','4396123'),
--     ('0002','443'),
--     ('0001','777');
-- COMMIT;

-- 老师在某个教学元素中提供的辅导材料
CREATE TABLE IF NOT EXISTS `guidance`(
  `id` INT NOT NULL AUTO_INCREMENT,
  `course_id` CHAR(20) ,
  `unit_id` CHAR(20) ,
  `section_id` CHAR(20) ,
  `guidance_id` CHAR(20),
  `guidance_name` CHAR(40) ,
  PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
-- BEGIN;
--   INSERT INTO `guidance` (course_id,guidance_id,guidance_name) VALUES
--   ('0001','888','恭喜'),
--   ('0001','6666','AC！error0！'),
--   ('0001','776655','额...'),
--   ('0002','159753','非空');
-- COMMIT;

-- 作业提交时间的表
CREATE TABLE IF NOT EXISTS `homeworkTime`(
  `account` CHAR(20),
  `name` CHAR(20) ,
  `course_id` CHAR(20) ,
  `homework_id` CHAR(10) NOT NULL,
  `submit_time` DATETIME,
  PRIMARY KEY ( `homework_id`,`account` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
-- 这样设置主键就限制了一个人对一份作业不能多次提交

-- 讨论参与情况
CREATE TABLE IF NOT EXISTS `discussion`(
  `id` INT NOT NULL AUTO_INCREMENT,
  `account` CHAR(20) ,
  `name` CHAR(20) ,
  `course_id` CHAR(20) ,
  `discussion_id` CHAR(10) ,
  `post_id` CHAR(10),
  `content` TEXT,
  `create_time` DATETIME,
  PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
-- BEGIN;
--   INSERT INTO `discussion` (account,course_id,discussion_id,post_id,content) VALUES
--   ('201630610496','0001','dis9527','NULL','今天的风儿好喧嚣'),
--   ('2016306104961','0001','dis2795','NULL','处处好风光，除了C12-346'),
--   ('201630610496','0001','dis9528','dis9527','emmm'),
--   ('201630610496','0001','dis2796','dis2795','因为我要赶紧做这个呀');
-- COMMIT;

-- 学习进度记录表
CREATE TABLE IF NOT EXISTS `learning_progress`(
  `id` INT NOT NULL AUTO_INCREMENT,
  `account` CHAR(20) NOT NULL,
  `name` CHAR(20) ,
  `course_id` CHAR(20) ,
  `unit_id` CHAR(20),
  `resource_id` CHAR(10) ,
  `resource_type` CHAR(2) ,
  `cur_time` CHAR(20),
  `duration` CHAR(20),
  `progress` CHAR(20) ,
  `credit` CHAR(20) ,
  `create_time` DATETIME,
  PRIMARY KEY (`id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
-- BEGIN;
--   INSERT INTO `learning_progress` (account,name,course_id,unit_id,resource_id,progress,credit,create_time) 
--   VALUES 
--   ('201630610496','黄基峰','0001','d1j','12345','0.28',5,'2019-05-09 14:44:23'),
--   ('201630610496','黄基峰','0001','d2j','12346','0.85',10,'2019-05-09 14:44:23'),
--   ('201630610496','黄基峰','0001','d3j','12347','0.10',3,'2019-05-09 14:44:23');
-- COMMIT;

-- 资源库下载情况
CREATE TABLE IF NOT EXISTS `download_materials`(
  `id` INT NOT NULL AUTO_INCREMENT,
  `account` CHAR(20) NOT NULL,
  `name` CHAR(20) ,
  `course_id` CHAR(20),
  `materials_id` CHAR(10) NOT NULL,
  `materials_name` CHAR(50),
  `create_time` DATETIME,
  PRIMARY KEY (`id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
-- BEGIN;
--   INSERT INTO `download_materials` (account,course_id,materials_id,materials_name) VALUES
--   ('201630610496','0001','4396123','养猪心得'),
--   ('201630610496','0001','777','2级抓下'),
--   ('201630610496','0001','2800','2级抓下再次出现');
-- COMMIT;

-- 辅导资料下载情况
CREATE TABLE IF NOT EXISTS `download_guidance`(
  `account` CHAR(20),
  `name` CHAR(20) ,
  `course_id` CHAR(20) ,
  `unit_id` CHAR(20),
  `guidance_id` CHAR(20) ,
  `guidance_name` CHAR(40) ,
  `create_time` DATETIME,
  PRIMARY KEY ( `account`,`guidance_id` )
  )ENGINE=InnoDB DEFAULT CHARSET=utf8;
-- BEGIN;
--   INSERT INTO `download_guidance` (account,course_id,guidance_id) VALUES 
--   ('201630610496','0001','888'),
--   ('201630610496','0001','6666'),
--   ('201630610491','0001','776655'),
--   ('201630610491','0002','159753');
-- COMMIT;
