Feature: Mass load test
  As a user, I want to be able to generate or export the data produced by this injection 
  so I can validate that the load was successful. This feature will also allow me to close 
  the application without any issues. The backup produced by this injection test will provide 
  the same level of detail that we see in the main screen grid of the order, including the model 
  color, the generated order numbers, and the client's OC.

Scenario: Successful data injection and export
  Given I have the application open and am ready to perform an injection test
  And I have the necessary data for the mass load test
  When I initiate the mass load test
  Then the system should perform the data injection
  And the system should generate a backup of the injection test of the DBF type
  When I export the data from the injection test 
  Then the system should provide detailed information including model color, generated order numbers, and the client's OC
  And the user should be able to validate if the load was done successfully
  When I activate the saved injection test
  Then I should be able to close the application without any issues.