Feature: Client Purchase Processing

As a QA automation expert, I ensure that the client purchase processing system works correctly. This includes automatically moving to the next input field after entering data and applying the correct discount percentage.

Scenario: Client Purchase Data Input and File Reading

Given the client purchase processing application is open
And the cursor is positioned at the first data input field

When I input client's purchase data
And press 'Enter'
Then the application should automatically move the cursor to the next data input field

When I input '15' in the discount percentage field
And press 'Enter'
Then the application should automatically move the cursor to the 'File Read' button

When I select the 'File Read' button
And select the corresponding file
Then the application should successfully read and process the file data.