CREATE TABLE `broadcast`.`news`
(
    `headline` VARCHAR(100) NOT NULL,
    `description` VARCHAR(500) NOT NULL,
    `author_name` VARCHAR(25) NOT NULL,
    `news_category` VARCHAR(20) NOT NULL,
    PRIMARY KEY (`headline`)
);