DROP TABLE IF EXISTS `tbl_Prices`;
CREATE TABLE `tbl_Prices` (
  `SysNo` int(11) NOT NULL AUTO_INCREMENT,
  `Symbol` char(6) NOT NULL,
  `Open` decimal(12,6) NOT NULL,
  `High` decimal(12,6) NOT NULL,
  `Low` decimal(12,6) NOT NULL,
  `Close` decimal(12,6) NOT NULL,
  `Volume` bigint(20) NOT NULL,
  `AdjClose` decimal(12,6) NULL,
  `Date` date DEFAULT NULL,
  `Amount` decimal(20,6) DEFAULT NULL,
  `CreateDate` datetime DEFAULT CURRENT_TIMESTAMP,
  `LastEditDate` datetime null,
 PRIMARY KEY (`SysNo`)
) ENGINE=InnoDB AUTO_INCREMENT=7387793 DEFAULT CHARSET=utf8;