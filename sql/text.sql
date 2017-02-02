CREATE TABLE BOKMALtext (
  `tid`         VARCHAR(255) NOT NULL,
  `title`       VARCHAR(255),
  `collection`  VARCHAR(255),
  `issnisbn`    VARCHAR(255),
  `wordcount`   INT(11),
  `version`     VARCHAR(255),
  `category`    VARCHAR(255),
  `publisher`   VARCHAR(255),
  `pubdate`     YEAR(4),
  `pubplace`    VARCHAR(255),
  `corpus_date` VARCHAR(255),
  `translation` VARCHAR(255),
  `startpos`    INT(11),
  `endpos`      INT(11),
  `supcat`      CHAR(2),
  PRIMARY KEY (`tid`)
);
