Feature: The dashboard view

  Feature: As a user I want the pages to be displayed when enter the correct url1
    Scenario: dashboard loads
     Given I am a user
      when I load the application url in the browser
      then the dashboard page is displayed

      Scenario:
    Given I am a user
    when I load the raw data url in the browser
    then the raw data page is displayed

  Scenario:
    Given I am a user
    when I load the data trend url in the browser
    then the data trend page is displayed