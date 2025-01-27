Feature: CSV File Reading and Validation

As an application, I need to read CSV files, validate each record, and recover missing data from the master product record, so that the correct data can be used to generate orders.

Scenario: Reading and Validating a CSV File

Given the application is open
And I have a CSV file for reading
When I select the button to choose a file
And I select the CSV file
And I double-click to open it
Then the application should start reading and validating each record in the file

Given the application is validating each record
When there is a missing store code in the record
Then the application should automatically associate it with a DNN store

Given the application is validating each record
When there is a 'NNN' code in the model, color, and size fields
Then the validation should recover the correct model name and color corresponding to the 'NNN' code

Given the application is validating each record
When there is a missing order quantity
Then the application should mark the field as mandatory

Given the application is validating each record
When a particular field is missing data
Then the system should automatically recover the respective price and SKU from the master product record

Given the application is validating each record
When the validation is completed
And all the data has been validated 100%
Then the application should be able to generate an order for each line

Given the application is validating each record
When an error is found in a line
Then the application should mark that line as 'no'
And highlight the entire line in red