Feature: Customer and Product Data Validation
In order to ensure the accuracy of customer and product data
As a data validation system
I want to validate the customer's existence, product details, and associated data in RPI's master files 

Scenario: Validate Customer and Product Details in RPI's master files

Given the system has access to RPI's master files
And the customer is "SOCiedad Comercial Valcao"

When the system validates the customer's existence in RPI's master files
Then the system should return the customer ID registered in RPI's master files

And when the system retrieves the SiteUsageID related to the customer's shipping address in RPI's master files
Then the system should return the SiteUsageID related to the customer's shipping address 

And when the system retrieves the SiteUsageID2 related to the customer's billing address in RPI's master files
Then the system should return the SiteUsageID2 related to the customer's billing address 

And when the system retrieves the TypeID related to the product's type and origin in RPI's master files
Then the system should return the TypeID related to the product's type and origin

And when the system retrieves the ItemID which is the product identifier in RPI's master files
Then the system should return the ItemID which is the product identifier 

And when the system retrieves the product's unit of measure in RPI's master files
Then the system should return the unit of measure of the product

And when the system retrieves the additional data related to product's genre, brand, class in RPI's master files
Then the system should return the genre, brand, class of the product

Given the system has all the validated data from the RPI's master files

When the user chooses to record the order
Then the system should generate a unique order number related to the data and save the order in the system

But when the user chooses to cancel the order
Then the system should not record the order and should not generate a unique order number