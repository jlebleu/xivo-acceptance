Feature: Stat

    Scenario: Generation of event "AGENTCALLBACKLOGIN"
        Given there is no agent with number "007"
        Given there is no user "User" "007"
        Given there is no "AGENTCALLBACKLOGIN" entry for agent "007"
        Given there is a user "User" "007" in context "statscenter" with number "1007"
        Given there is a agent "Agent" "007" in context "statscenter" with number "007"
        Given I log agent "007" on extension "1007"
        Given I wait 5 seconds for the calls processing
        Then i should see 1 "AGENTCALLBACKLOGIN" event for agent "007" in the queue log