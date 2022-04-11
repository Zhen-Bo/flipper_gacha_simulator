-- --------------------------------------------------------
-- 主機:                           207.148.101.170
-- 伺服器版本:                        10.3.31-MariaDB-0ubuntu0.20.04.1 - Ubuntu 20.04
-- 伺服器作業系統:                      debian-linux-gnu
-- HeidiSQL 版本:                  11.0.0.5919
-- --------------------------------------------------------
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
-- 傾印  資料表 flipper_gacha_simu._template_record 結構
CREATE TABLE IF NOT EXISTS `1nv_record` (
  `sim_index` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `five_count` int(11) unsigned NOT NULL DEFAULT 0,
  `four_count` int(11) unsigned NOT NULL DEFAULT 0,
  `three_count` int(11) unsigned NOT NULL DEFAULT 0,
  `seed` mediumtext NOT NULL,
  `ip` mediumtext NOT NULL,
  `time` mediumtext NOT NULL,
  PRIMARY KEY (`sim_index`) USING BTREE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 ROW_FORMAT = DYNAMIC;
-- 取消選取資料匯出。
-- 傾印  資料表 flipper_gacha_simu._template_roll 結構
CREATE TABLE IF NOT EXISTS `1nv_roll` (
  `sim_index` int(11) NOT NULL,
  `dev_id` mediumtext NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 ROW_FORMAT = DYNAMIC;
-- 取消選取資料匯出。
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;