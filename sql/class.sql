CREATE TABLE BOKMALclass (
  `tid` VARCHAR(255) NOT NULL,
  `class` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`tid`, `class`),
  KEY `topic` (`class`, `tid`)
);
