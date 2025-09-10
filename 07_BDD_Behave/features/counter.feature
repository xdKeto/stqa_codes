Feature: Hit Counter

As a website visitor
I want to be able to click a button to make the counter go up
So that I can see how many times I have clicked the button

Scenario: The counter goes up when the button is clicked
    Given the counter is reset
    When the "Hit" button is clicked
    Then the counter shows value "1"
    When the "Hit" button is clicked
    Then the counter shows value "2"