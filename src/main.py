#!/usr/bin/python
#-*- coding: utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import random
import string
import time
import setuptools
import tokenize
import os 
import mysql.connector as mariadb
import boto3
#https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
mariadb_connection = mariadb.connect(pool_size=3)
cursor = mariadb_connection.cursor()


def query(sql, params):
    try:
      cursor.execute(sql, params)
    except mariadb.Error as error:
      print("Error: {}".format(error))
    mariadb_connection.commit()
    print("insert")

#retrieving information
# some_name = 'Georgi'
# cursor.execute("SELECT first_name,last_name FROM employees WHERE
# first_name=%s", (some_name,))

# for first_name, last_name in cursor:
#     print("First name: {}, Last name: {}").format(first_name,last_name)

# #insert information
# try:
#     cursor.execute("INSERT INTO employees (first_name,last_name) VALUES
#     (%s,%s)", ('Maria','DB'))
# except mariadb.Error as error:
#     print("Error: {}".format(error))

# mariadb_connection.commit()
# print ("The last inserted id was: ", cursor.lastrowid)

# mariadb_connection.close()

# import pymysql
# # Connect to the database
# connection = pymysql.connect(
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)

# try:
#     with connection.cursor() as cursor:
#         # Create a new record
#         sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
#         cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

#     # connection is not autocommit by default.  So you must commit to save
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
  def get(self):
    set_header(self)
    file_name = self.get_argument("file_name")
    fileName='test/' + file_name
    bucket='kvs-for-pcu-capstone'
    client=boto3.client('rekognition')
    response = client.detect_faces(
      Image={'S3Object':{'Bucket':bucket,'Name':fileName}},
      Attributes=['ALL', ]
      )
    print('Detected labels for ' + fileName)    
    dic = dict()
    for emotion in response['FaceDetails'][0]['Emotions']:
      dic.update({emotion['Type']:str(emotion['Confidence'])})
    self.write(tornado.escape.json_encode({"result":0, "picture_result":dic}))


  def post(self):
    set_header(self)
    #print(self.request.files['file'])
    #self.write("Hello, world")
    fileinfo = self.request.files['file'][0]
    original_fname = fileinfo['filename']
    current_time = int(time.time() * 1000)
    new_file_name =  str(current_time) + "_" + original_fname
    output_file = open(dir_path + "/uploads/" + new_file_name, 'wb')
    output_file.write(fileinfo['body'])
    
    #query("INSERT INTO files (file_name) VALUES (%s)", (original_fname,))
    # Create an S3 client
    s3 = boto3.client('s3')
    
    bucket_name = 'kvs-for-pcu-capstone'

    # Uploads the given file using a managed uploader, which will split up large
    # files automatically and upload parts in parallel.
    s3.upload_file(dir_path + "/uploads/" + new_file_name, bucket_name,"test/" +  new_file_name)
    #mariadb_connection.commit()
    self.write(tornado.escape.json_encode({"result":0}))

# 통계 가져오기
class StatsHandler(tornado.web.RequestHandler):
  def get(self):
    set_header(self)
    print(self.get_current_user())
    user_idx = self.get_argument("user_idx")
    start_at = self.get_argument("start_at")
    self.write(tornado.escape.json_encode({"result":0}))

    
class SettingHandler(tornado.web.RequestHandler):
  def get(self):
    set_header(self)
    self.write("get setting")
  def put(self):
    set_header(self)
    self.write("put setting")

class TestHandler(tornado.web.RequestHandler):
  def get(self):
    set_header(self)
    cursor = mariadb_connection.cursor()
    try:
      cursor.execute("SELECT  * FROM kvs.test")
    except mariadb.Error as error :
      print("Error: {}".format(error))
    ls = list()
    for idx, a in cursor:
      ls.append({"idx":idx, "a":a})

    self.write(tornado.escape.json_encode({"result":0, "list":ls}))
  def put(self):
    set_header(self)
    self.write(tornado.escape.json_encode({"result":0}))

class PingHandler(tornado.web.RequestHandler):
  def get(self):
    set_header(self)
    self.write(tornado.escape.json_encode({"result":0}))

application = tornado.web.Application(
    [
        (r"/test", TestHandler),
        (r"/main", MainHandler),
        (r"/picture", PictureHandler),
        (r"/stats", StatsHandler),
        (r"/setting", SettingHandler),
        (r"/auth", AuthHandler),
        (r"/ping", PingHandler),
        ]
    )

if __name__ == "__main__":
  application.listen(8888)
  tornado.ioloop.IOLoop.instance().start()
