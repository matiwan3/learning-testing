Feature: Login Functionality

    Scenario Outline: User Login
        Given the user is on the login page
        When they enter "<username>" and "<password>"
        Then they should be logged in successfully

        Examples:
            | username | password |
            | user1    | pass123  |
            | user2    | pass456  |
            | user3    | pass789  |
            