DROP TABLE IF EXISTS `tbl_MACD`;
CREATE TABLE `tbl_MACD` (
  `SysNo` int(11) NOT NULL AUTO_INCREMENT,
  `Symbol` char(6) NOT NULL,
  `Date` datetime not null,
  `Ema5` decimal(12,6) NOT NULL,
  `Ema10` decimal(12,6) NOT NULL,
  `Ema12` decimal(12,6) NOT NULL,
  `Ema20` decimal(12,6) NOT NULL,
  `Ema26` decimal(12,6) NOT NULL,
  `Ema30` decimal(12,6) NOT NULL,
  `Ema60` bigint(20) NOT NULL,
  `Macd` bigint(20) NOT NULL,
  `Diff` bigint(20) NOT NULL,
  `Dea` bigint(20) NOT NULL,
  `MacdV` bigint(20) NOT NULL,
  `DiffV` bigint(20) NOT NULL,
  `DeaV` bigint(20) NOT NULL,
  `CreateDate` datetime DEFAULT CURRENT_TIMESTAMP,
  `LastEditDate` datetime null,
 PRIMARY KEY (`SysNo`)
) ENGINE=InnoDB AUTO_INCREMENT=7387793 DEFAULT CHARSET=utf8;