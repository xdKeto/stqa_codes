Feature: Search Pets by ID

As a pet shop customer
I need to be able to find a pet by its ID
So that I can see all of its information

Background:
    Given the following pets
        | name   | category | available | gender  | birthday   |
        | Fido   | dog      | True      | MALE    | 2019-11-18 |
        | Kitty  | cat      | True      | FEMALE  | 2020-08-13 |
        | Leo    | lion     | False     | MALE    | 2021-04-01 |

Scenario: Search for a pet by ID and populate the form
    Given I am on the "Home Page"
    When I set the "Pet ID" to "1"
    And I click the "Search" button
    Then I should see the message "Success"
    And the "Name" field should contain "Fido"
    And the "Category" field should contain "dog"
    And the "Available" checkbox should be checked
    And the "Gender" select should contain "MALE"
    And the "Birthday" field should contain "2019-11-18"
