Feature: User
    In order to get a user
    I have to create a user

    Scenario Outline: Add a user with first name and last name and remove it
        Given I login as root with password superpass at http://192.168.32.51/
        When I create a user John Willis
        Then user John Willis is displayed in the list
        When user John Willis is removed
        Then user John Willis is not displayed in the list