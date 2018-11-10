# encoding: utf-8
import os
_basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY='a unique and long key'
TITLE='Riki' 
HISTORY_SHOW_MAX=30
PIC_BASE = '/static/content/'
CONTENT_DIR = 'C:/Users/Apekshya/Desktop/Semester-4/Software Engineering/Project/wiki_flask/GradWiki/content'
USER_DIR = 'C:/Users/Apekshya/Desktop/Semester-4/Software Engineering/Project/wiki_flask/GradWiki/user'
NUMBER_OF_HISTORY = 5
PRIVATE = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI= 'sqlite:///' + os.path.join(_basedir, 'database.db')
