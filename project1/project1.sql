-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema project1
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `project1` ;

-- -----------------------------------------------------
-- Schema project1
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `project1` DEFAULT CHARACTER SET utf8 ;
USE `project1` ;

-- -----------------------------------------------------
-- Table `project1`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project1`.`users` ;

CREATE TABLE IF NOT EXISTS `project1`.`users` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `firstName` VARCHAR(45) NULL,
  `lastName` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `username` VARCHAR(45) NULL,
  `password` VARCHAR(85) NULL,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `project1`.`posts`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project1`.`posts` ;

CREATE TABLE IF NOT EXISTS `project1`.`posts` (
  `post_id` INT NOT NULL AUTO_INCREMENT,
  `content` VARCHAR(80) NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`post_id`),
  INDEX `fk_posts_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_posts_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `project1`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `project1`.`likes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project1`.`likes` ;

CREATE TABLE IF NOT EXISTS `project1`.`likes` (
  `post_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`post_id`, `user_id`),
  INDEX `fk_posts_has_users_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_posts_has_users_posts1_idx` (`post_id` ASC) VISIBLE,
  CONSTRAINT `fk_posts_has_users_posts1`
    FOREIGN KEY (`post_id`)
    REFERENCES `project1`.`posts` (`post_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_posts_has_users_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `project1`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `project1`.`comments`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project1`.`comments` ;

CREATE TABLE IF NOT EXISTS `project1`.`comments` (
  `post_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `content` VARCHAR(45) NULL,
  PRIMARY KEY (`post_id`, `user_id`),
  INDEX `fk_posts_has_users_users2_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_posts_has_users_posts2_idx` (`post_id` ASC) VISIBLE,
  CONSTRAINT `fk_posts_has_users_posts2`
    FOREIGN KEY (`post_id`)
    REFERENCES `project1`.`posts` (`post_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_posts_has_users_users2`
    FOREIGN KEY (`user_id`)
    REFERENCES `project1`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `project1`.`followed_user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project1`.`followed_user` ;

CREATE TABLE IF NOT EXISTS `project1`.`followed_user` (
  `user_id` INT NOT NULL,
  `user_id1` INT NOT NULL,
  PRIMARY KEY (`user_id`, `user_id1`),
  INDEX `fk_users_has_users_users2_idx` (`user_id1` ASC) VISIBLE,
  INDEX `fk_users_has_users_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_users_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `project1`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_users_users2`
    FOREIGN KEY (`user_id1`)
    REFERENCES `project1`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
