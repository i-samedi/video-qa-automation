Feature: Order Type and Dispatch Origin Selection

Scenario: Default and custom selection of order type and dispatch origin

Given the user is on the order page
And the order type options are displayed on the left
And 'Normal' order type is selected by default
And the dispatch origin is shown where the user can dispatch the merchandise from
And the default dispatch origin is set to 'SDFORCE'
When the user presses 'Enter'
Then the cursor should respond automatically
And the dispatch origin drop-down menu should be displayed
When the user clicks on the dispatch origin drop-down menu
Then the user should be able to select any warehouse for the dispatch without any issue
When the user selects a warehouse from the drop-down menu
And the user presses 'Enter'
Then the selected warehouse should be set as the dispatch origin
And the cursor should respond automatically
And the page should reflect the new dispatch origin.