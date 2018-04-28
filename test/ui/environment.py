from selenium import webdriver
from behave import *

def before_all(context):
    # call("python ../../manage.py runserver")
    # management.call_command('runserver')
    context.browser = webdriver.Chrome("./chromedriver")
    context.BASE_URL = "http://localhost:8000/"

def after_all(context):
    context.browser.quit()