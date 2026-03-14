CREATE DATABASE IF NOT EXISTS pocketbot;
USE pocketbot;

DROP TABLE IF EXISTS chat_log;
DROP TABLE IF EXISTS transaction;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL
);

CREATE TABLE transaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    amount FLOAT NOT NULL,
    category VARCHAR(50),
    type VARCHAR(10),
    created DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chat_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    message TEXT,
    reply TEXT,
    created DATETIME DEFAULT CURRENT_TIMESTAMP
);
