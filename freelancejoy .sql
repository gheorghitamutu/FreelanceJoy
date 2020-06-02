SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE DATABASE IF NOT EXISTS `freelancejoy` DEFAULT CHARACTER SET latin1 COLLATE latin1_general_ci;
USE `freelancejoy`;

DROP TABLE IF EXISTS `attachments`;
CREATE TABLE `attachments` (
  `id` int(11) NOT NULL,
  `job_id` int(11) NOT NULL,
  `link` tinytext COLLATE utf8_general_mysql500_ci NOT NULL,
  `file_name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;

INSERT INTO `attachments` (`id`, `job_id`, `link`, `file_name`, `created_at`) VALUES
(14, 0, 'https://storage.cloud.google.com/freelancejoy.appspot.com/freelance/nio/1/attachment/hel.txt', 'hel.txt', '2020-06-02 13:28:10'),
(15, 0, 'https://storage.cloud.google.com/freelancejoy.appspot.com/freelance/nio/1/attachment/el.txt', 'el.txt', '2020-06-02 13:28:10');

DROP TABLE IF EXISTS `biddings`;
CREATE TABLE `biddings` (
  `id` int(11) NOT NULL,
  `user_email` tinytext COLLATE utf8_general_mysql500_ci NOT NULL,
  `job_id` int(11) NOT NULL,
  `message` mediumtext COLLATE utf8_general_mysql500_ci NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;

DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;

INSERT INTO `categories` (`id`, `name`) VALUES
(53, 'design'),
(49, 'hello'),
(51, 'helo'),
(52, 'nice'),
(48, 'r'),
(54, 'string');

DROP TABLE IF EXISTS `jobs`;
CREATE TABLE `jobs` (
  `id` int(11) NOT NULL,
  `user_email` tinytext COLLATE utf8_general_mysql500_ci NOT NULL,
  `title` tinytext COLLATE utf8_general_mysql500_ci NOT NULL,
  `description` varchar(4000) COLLATE utf8_general_mysql500_ci NOT NULL,
  `payment` decimal(5,2) NOT NULL,
  `category_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;

INSERT INTO `jobs` (`id`, `user_email`, `title`, `description`, `payment`, `category_id`, `created_at`) VALUES
(1, 'string', 'string', 'string', '0.00', 0, '2020-06-02 16:56:35');

DROP TABLE IF EXISTS `presentation_images`;
CREATE TABLE `presentation_images` (
  `id` int(11) NOT NULL,
  `project_for_sale_id` int(11) NOT NULL,
  `name` tinytext CHARACTER SET utf8 COLLATE utf8_general_mysql500_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

DROP TABLE IF EXISTS `projects`;
CREATE TABLE `projects` (
  `id` int(11) NOT NULL,
  `job_id` int(11) NOT NULL,
  `deadline` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `freelancer_email` tinytext CHARACTER SET utf8 COLLATE utf8_general_mysql500_ci NOT NULL,
  `delivered_assets_archive_link` mediumtext CHARACTER SET utf8 COLLATE utf8_general_mysql500_ci,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

DROP TABLE IF EXISTS `projects_delivered_assets`;
CREATE TABLE `projects_delivered_assets` (
  `id` int(11) NOT NULL,
  `name` tinytext COLLATE utf8_general_mysql500_ci NOT NULL,
  `link` tinytext COLLATE utf8_general_mysql500_ci NOT NULL,
  `project_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;

DROP TABLE IF EXISTS `projects_for_sale`;
CREATE TABLE `projects_for_sale` (
  `id` int(11) NOT NULL,
  `user_email` tinytext COLLATE utf8_general_mysql500_ci NOT NULL,
  `partner_email` tinytext COLLATE utf8_general_mysql500_ci,
  `name` tinytext COLLATE utf8_general_mysql500_ci NOT NULL,
  `price` decimal(5,2) NOT NULL,
  `description` mediumtext COLLATE utf8_general_mysql500_ci NOT NULL,
  `assets_archive_link` tinytext COLLATE utf8_general_mysql500_ci NOT NULL,
  `category_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;


ALTER TABLE `attachments`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `file_name` (`file_name`);

ALTER TABLE `biddings`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

ALTER TABLE `jobs`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `presentation_images`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `projects`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `projects_for_sale`
  ADD PRIMARY KEY (`id`);


ALTER TABLE `attachments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

ALTER TABLE `biddings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=55;

ALTER TABLE `jobs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

ALTER TABLE `presentation_images`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `projects`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `projects_for_sale`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
