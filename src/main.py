import tornado.httpserver, tornado.ioloop, tornado.options, tornado.web, os.path, random, string, time, setuptools, tokenize
import os 
import mysql.connector as mariadb
#https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
mariadb_connection = mariadb.connect(pool_name = "abc",user='kvs', password='pcu_kvs', database='kvs_test', pool_size=3)
cursor = mariadb_connection.cursor()

#retrieving information
# some_name = 'Georgi'
# cursor.execute("SELECT first_name,last_name FROM employees WHERE first_name=%s", (some_name,))

# for first_name, last_name in cursor:
#     print("First name: {}, Last name: {}").format(first_name,last_name)

# #insert information
# try:
#     cursor.execute("INSERT INTO employees (first_name,last_name) VALUES (%s,%s)", ('Maria','DB'))
# except mariadb.Error as error:
#     print("Error: {}".format(error))

# mariadb_connection.commit()
# print ("The last inserted id was: ", cursor.lastrowid)

# mariadb_connection.close()

# import pymysql
# # Connect to the database
# connection = pymysql.connect(host='localhost',
#                              user='kvs',
#                              password='pcu_kvs',
#                              db='kvs_test',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)

# try:
#     with connection.cursor() as cursor:
#         # Create a new record
#         sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
#         cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

#     # connection is not autocommit by default. So you must commit to save
#     # your changes.
#     connection.commit()

#     with connection.cursor() as cursor:
#         # Read a single record
#         sql = "SELECT * FROM `users` WHERE `email`=%s"
#         cursor.execute(sql, ('webmaster@python.org',))
#         result = cursor.fetchone()
#         print(result)
# finally:
#     connection.close()


dir_path = os.path.dirname(os.path.realpath(__file__))

print(dir_path)
def set_header(self):
	self.set_header("Content-Type", "application/json")

def publish_fcm(Message,Target):
	1
	
class AuthHandler(tornado.web.RequestHandler):
	def post(self):
		body_data = tornado.escape.json_decode(self.request.body)
		print(body_data)
		id = body_data.get("id")
		password = body_data.get("password")
		self.write(tornado.escape.json_encode({"result":0}))

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		set_header(self)
		self.write(tornado.escape.json_encode({"result":0}))
				
	def post(self):
		set_header(self)
		self.write(tornado.escape.json_encode({"result":0}))

# 사진 전송
class PictureHandler(tornado.web.RequestHandler):
	def post(self):
		set_header(self)
		#print(self.request.files['file'])
		#self.write("Hello, world")
		fileinfo = self.request.files['file'][0]
		original_fname = fileinfo['filename']
		current_time = int(time.time()*1000)
		output_file = open(dir_path + "/uploads/" + str(current_time) + "_" + original_fname, 'wb')
		output_file.write(fileinfo['body'])
		try:
			cursor.execute("INSERT INTO files (file_name) VALUES (%s)", (original_fname,))
		except mariadb.Error as error:
			print("Error: {}".format(error))
		print("insert")
		mariadb_connection.commit()
		self.write(tornado.escape.json_encode({"result":0}))
		
# 통계 가져오기
class StatsHandler(tornado.web.RequestHandler):
	def get(self):
		set_header(self)
		print(self.get_current_user())
		user_idx = self.get_argument("user_idx")
		start_at = self.get_argument("start_at")
		self.write("{\"result\":\"0\"}")
				
class SettingHandler(tornado.web.RequestHandler):
	def get(self):
		set_header(self)
		self.write("get setting")
	def put(self):
		set_header(self)
		self.write("put setting")

application = tornado.web.Application([
	(r"/main", MainHandler),
	(r"/picture", PictureHandler),
	(r"/stats", StatsHandler),
	(r"/setting", SettingHandler),
	(r"/auth", AuthHandler),
])

if __name__ == "__main__":
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()