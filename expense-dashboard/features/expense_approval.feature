Feature: Expense Approval Workflow
  Scenario: Auto-approve low value expense
    Given an expense report for $50
    When the agent processes the report
    Then the expense should be automatically approved

  Scenario: Route high value expense to human manager
    Given an expense report for $150
    When the agent processes the report
    Then the agent execution should pause
    And the session should appear in the Manager Dashboard for review
