DROP TABLE IF EXISTS `tbl_Mean`;
CREATE TABLE `tbl_Mean` (
  `SysNo` int(11) NOT NULL AUTO_INCREMENT,
  `Symbol` char(6) NOT NULL,
  `Date` datetime not null,
  `Ma5` decimal(12,6) NOT NULL,
  `Ma10` decimal(12,6) NOT NULL,
  `Ma20` decimal(12,6) NOT NULL,
  `Ma30` decimal(12,6) NOT NULL,
  `Ma60` bigint(20) NOT NULL,
  `CreateDate` datetime DEFAULT CURRENT_TIMESTAMP,
  `LastEditDate` datetime null,
 PRIMARY KEY (`SysNo`)
) ENGINE=InnoDB AUTO_INCREMENT=7387793 DEFAULT CHARSET=utf8;