CREATE TABLE BOKMALauthor (
  `a_id`          INT(11) NOT NULL AUTO_INCREMENT,
  `firstname`     VARCHAR(100),
  `lastname`      VARCHAR(100),
  `type`          VARCHAR(10),
  `sex`           CHAR(1),
  `geogr`         VARCHAR(10),
  `born`          YEAR(4),
  `tid`           VARCHAR(255),
  `name`          VARCHAR(100),
  `in_collection` TINYINT(4),
  PRIMARY KEY (`a_id`)
);
