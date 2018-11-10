# encoding: utf-8
import os
_basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY='a unique and long key'
TITLE='Riki' 
HISTORY_SHOW_MAX=30
PIC_BASE = '/static/content/'
CONTENT_DIR = 'C:/Users/Apekshya/Desktop/Semester-4/Software Engineering/Project/wiki_flask/GradWiki/content'
USER_DIR = 'C:/Users/Apekshya/Desktop/Semester-4/Software Engineering/Project/wiki_flask/GradWiki/user'

# This is the path to the upload directory
UPLOAD_FOLDER = 'C:/Users/Apekshya/Desktop/Semester-4/Software Engineering/Project/wiki_flask/GradWiki/uploads'
# Allowed file extensions
ALLOWED_EXTENSIONS = ['txt', 'mp3', 'mp4', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'gif', 'pdf', 'png', 'jpg', 'jpeg', 'zip']
#Content length that can be uploaded
MAX_CONTENT_LENGTH = 1024 * 1024 * 1024 #1GB
NUMBER_OF_HISTORY = 5
PRIVATE = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI= 'sqlite:///' + os.path.join(_basedir, 'database.db')
