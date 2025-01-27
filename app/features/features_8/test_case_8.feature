Feature: Order Generation
In order to properly manage and track orders, our system generates unique order numbers for each order made. This process is crucial for inventory management, customer service, and financial tracking. 

Scenario: Unique Order Number Generation based on Gender Distinction

Given that the system has received an order for multiple items
And the items include both men's and women's apparel from the same brand and clothing class
When the system processes the order
Then it should generate a unique order number for the men's items
And it should generate a separate unique order number for the women's items
And both order numbers should be associated with the customer's data.

Scenario: Order number for single gender distinction

Given that the system has received an order for multiple items
And the items include only men's or women's apparel from the same brand and clothing class
When the system processes the order
Then it should generate a unique order number for the respective gender's items
And the order number should be associated with the customer's data.