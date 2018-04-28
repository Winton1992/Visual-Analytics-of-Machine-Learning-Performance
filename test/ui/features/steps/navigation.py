from behave import *
from selenium import webdriver

@given('I am a user')
def step_impl(context):
    assert True is not False

@when('I load the application url in the browser')
def step_impl(context):
    context.browser.get(context.BASE_URL)

@when('I load the raw data url in the browser')
def step_impl(context):
    context.browser.get(context.BASE_URL+"RawData/event-flow/")

@when('I load the data trend url in the browser')
def step_impl(context):
    context.browser.get(context.BASE_URL+"RawData/data-trend/")

@then('the raw data page is displayed')
def step_impl(context):

    assert context.browser.title == 'raw-data-event-flow'

@then('the data trend page is displayed')
def step_impl(context):

    assert context.browser.title == 'raw-data-data-trend'


@then('the dashboard page is displayed')
def step_impl(context):

    assert context.browser.title == 'dashboard'
