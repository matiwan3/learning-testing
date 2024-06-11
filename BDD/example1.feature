Feature: Login
  As a user
  I want to be able to login to the system
  So that I can access my account

  Scenario: Successful login
    Given I am on the login page
    When I enter valid credentials
    And click on the login button
    Then I should be redirected to the dashboard

  Scenario: Invalid credentials
    Given I am on the login page
    When I enter invalid credentials
    And click on the login button
    Then I should see an error message

  Scenario: Forgot password
    Given I am on the login page
    When I click on the "Forgot password" link
    Then I should be redirected to the password recovery page