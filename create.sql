DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  PRIMARY KEY (`username`)
);

INSERT INTO `users` VALUES ('user1', '12');
INSERT INTO `users` VALUES ('user2', '12');
INSERT INTO `users` VALUES ('user3', '12');
DROP TABLE IF EXISTS `rules`;
CREATE TABLE `rules`  (
  `service` varchar(20) NOT NULL,
  `user` varchar(20) NOT NULL,
  `id` INTEGER PRIMARY KEY AUTOINCREMENT
) ;

INSERT INTO `rules` VALUES ('hardDisk', 'user3', 1);
INSERT INTO `rules` VALUES ('printer', 'user1', 2);
INSERT INTO `rules` VALUES ('printer', 'user2', 3);
INSERT INTO `rules` VALUES ('printer', 'user3', 4);
INSERT INTO `rules` VALUES ('printer', 'user4', 5);
INSERT INTO `rules` VALUES ('hardDisk', 'user4', 6);
INSERT INTO `rules` VALUES ('secret', 'user4', 7);