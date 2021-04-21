CREATE TABLE `broadcast`.`users`
(
    `username` VARCHAR(20) NOT NULL,
    `email`    VARCHAR(50) NOT NULL,
    `password` VARCHAR(20) NOT NULL,
    PRIMARY KEY (`email`)
);