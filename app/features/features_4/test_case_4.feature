Feature: Credit Validation and Order Placement

Scenario: Validating sufficient credit and placing an order at a selected branch

Given I am logged into the application
And I can see my available credit
When I decide to place an order
Then the application should automatically validate if I have sufficient credit for the order

Given the application has validated my credit
And I have sufficient credit for the order
When I proceed to select the destination branch for the order
Then the application should display a list of all my branches

Given I have multiple branches
When I choose to select the branch from the drop-down menu
Then the application should allow me to select one

Given I have chosen a branch for the order
When I proceed to input the sale conditions
And I select one
And I hit Enter
Then the application should accept the input

Given I have selected the sale conditions
When I proceed to input the order
Then I should be able to use the data from the template I am going to upload
And the application should accept the order details.