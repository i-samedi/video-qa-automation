Feature: Customer Identification through RUT
In order to dispatch the right products to the right customer, the system should be able to identify customers based on their RUT (Rol Único Tributario). If the RUT is not known, a search function is provided to find the customer based on part of their social relation.

Scenario: Searching and Selecting a Customer using RUT
Given I am on the customer identification screen
And I see a field to enter the customer's RUT
When I do not know the customer's RUT
Then I should see a button with a question mark sign
And I click on the button
And I am taken to a search function
When I enter part of the customer's social relation into the search function
And I press Enter
Then I should see a list of customers that match the search pattern
And I select the appropriate customer from the list by double clicking
Then the selected customer's RUT should appear on the main screen along with their social relation
When I press Enter
Then the system should recognize and store the selected customer's RUT and social relation.