import sqlite3

sql_statements = """
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
"""

username = "user1"
password = "123456"
service = "printer"

# 执行修改后的 SQL 语句
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM users WHERE username = ? and password = ?",(username, password))
if not cursor.fetchall():
    print("用户名或密码错误！")
else :
    print("登录成功!")
cursor.execute("SELECT * FROM rules WHERE user = ? and service = ?",(username,service))
if not cursor.fetchall():
    print("用户未授权!")
else :
    print("访问服务成功!")
# 关闭数据库连接
conn.close()
