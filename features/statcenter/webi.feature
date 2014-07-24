Feature: WEBI Stats

    Scenario: First week of 2104
        Given there are queues with infos:
          | name | number | context     |
          | q42  | 5042   | statscenter |
        Given there is a statistic configuration "test" from "8:00" to "12:00" with queue "q42"
        Then I should have the following statistics on "q42" on "2013-12-30" on configuration "test" on axetype "week":
          |             |
          | Monday 30   |
          | Tuesday 31  |
          | Wednesday 1 |
          | Thursday 2  |
          | Friday 3    |
          | Saturday 4  |
          | Sunday 5    |
          | Total       |