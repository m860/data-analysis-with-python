use stock;
SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for tbl_StockList
-- ----------------------------
DROP TABLE IF EXISTS `tbl_Symbols`;
CREATE TABLE `tbl_Symbols` (
  `SysNo` int(11) NOT NULL AUTO_INCREMENT,
  `Symbol` char(6) NOT NULL,
  `ExchangeCode` char(2) not null,
  `CreateDate` datetime not null default now(),
  `LastEditDate` datetime null,
  PRIMARY KEY (`SysNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

