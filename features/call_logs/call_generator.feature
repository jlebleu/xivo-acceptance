Feature: Call Log Generation

    Scenario: Generation of answered internal call
        Given there are no calls
        Given I have the following CEL entries:
            | eventtype    | eventtime                  | cid_name      | cid_num | exten | context | uniqueid     | linkedid     | userfield |
            | CHAN_START   | 2013-01-01 08:46:20.118025 | Bob Marley    | 1002    | 1001  | default | 1375994780.1 | 1375994780.1 |           |
            | APP_START    | 2013-01-01 08:46:20.156126 | Bob Marley    | 1002    | s     | user    | 1375994780.1 | 1375994780.1 |           |
            | CHAN_START   | 2013-01-01 08:46:20.156385 | Alice Aglisse | 1001    | s     | default | 1375994780.2 | 1375994780.1 |           |
            | ANSWER       | 2013-01-01 08:46:23.005457 | Alice Aglisse | 1001    | s     | default | 1375994780.2 | 1375994780.1 |           |
            | ANSWER       | 2013-01-01 08:46:23.005613 | Bob Marley    | 1002    | s     | user    | 1375994780.1 | 1375994780.1 |           |
            | BRIDGE_START | 2013-01-01 08:46:23.005632 | Bob Marley    | 1002    | s     | user    | 1375994780.1 | 1375994780.1 |           |
            | BRIDGE_END   | 2013-01-01 08:46:26.848705 | Bob Marley    | 1002    | s     | user    | 1375994780.1 | 1375994780.1 |           |
            | HANGUP       | 2013-01-01 08:46:26.849811 | Alice Aglisse | 1001    |       | user    | 1375994780.2 | 1375994780.1 |           |
            | CHAN_END     | 2013-01-01 08:46:26.84983  | Alice Aglisse | 1001    |       | user    | 1375994780.2 | 1375994780.1 |           |
            | HANGUP       | 2013-01-01 08:46:26.860098 | Bob Marley    | 1002    | s     | user    | 1375994780.1 | 1375994780.1 |           |
            | CHAN_END     | 2013-01-01 08:46:26.860247 | Bob Marley    | 1002    | s     | user    | 1375994780.1 | 1375994780.1 |           |
            | LINKEDID_END | 2013-01-01 08:46:26.860254 | Bob Marley    | 1002    | s     | user    | 1375994780.1 | 1375994780.1 |           |
        When I generate call logs
        Then I should have the following call logs:
            | date                       | source_name | source_exten | destination_exten |       duration | user_field |
            | 2013-01-01 08:46:20.118025 | Bob Marley  |         1002 |              1001 | 0:00:03.854485 |            |

    Scenario: Generation of non-answered internal call
        Given there are no calls
        Given I have the following CEL entries:
            | eventtype    | eventtime                  | cid_name      | cid_num | exten | context | uniqueid     | linkedid     | userfield |
            | CHAN_START   | 2013-01-01 08:46:31.981    | Bob Marley    | 1002    | 1001  | default | 1375994791.3 | 1375994791.3 |           |
            | APP_START    | 2013-01-01 08:46:32.016612 | Bob Marley    | 1002    | s     | user    | 1375994791.3 | 1375994791.3 |           |
            | CHAN_START   | 2013-01-01 08:46:32.016872 | Alice Aglisse | 1001    | s     | default | 1375994792.4 | 1375994791.3 |           |
            | HANGUP       | 2013-01-01 08:46:36.327564 | Alice Aglisse | 1001    | s     | default | 1375994792.4 | 1375994791.3 |           |
            | CHAN_END     | 2013-01-01 08:46:36.32762  | Alice Aglisse | 1001    | s     | default | 1375994792.4 | 1375994791.3 |           |
            | HANGUP       | 2013-01-01 08:46:36.327692 | Bob Marley    | 1002    | s     | user    | 1375994791.3 | 1375994791.3 |           |
            | CHAN_END     | 2013-01-01 08:46:36.327704 | Bob Marley    | 1002    | s     | user    | 1375994791.3 | 1375994791.3 |           |
            | LINKEDID_END | 2013-01-01 08:46:36.327708 | Bob Marley    | 1002    | s     | user    | 1375994791.3 | 1375994791.3 |           |
        When I generate call logs
        Then I should have the following call logs:
            | date                    | source_name | source_exten | destination_exten | duration | user_field |
            | 2013-01-01 08:46:31.981 | Bob Marley  | 1002         | 1001              | 0        |            |

    Scenario: Generation of answered incoming call
        Given there are no calls
        Given I have the following CEL entries:
            | eventtype    | eventtime                  | cid_name   | cid_num    | exten | context     | uniqueid      | linkedid      | userfield |
            | CHAN_START   | 2013-01-01 11:02:38.0 | 612345678  | 612345678  | 1002  | from-extern | 1376060558.17 | 1376060558.17 |           |
            | APP_START    | 2013-01-01 11:02:38.0 |            | 0612345678 | s     | user        | 1376060558.17 | 1376060558.17 |           |
            | CHAN_START   | 2013-01-01 11:02:38.0 | Bob Marley | 1002       | s     | default     | 1376060558.18 | 1376060558.17 |           |
            | ANSWER       | 2013-01-01 11:02:42.0 | Bob Marley | 1002       | s     | default     | 1376060558.18 | 1376060558.17 |           |
            | ANSWER       | 2013-01-01 11:02:42.0 |            | 0612345678 | s     | user        | 1376060558.17 | 1376060558.17 |           |
            | BRIDGE_START | 2013-01-01 11:02:42.0 |            | 0612345678 | s     | user        | 1376060558.17 | 1376060558.17 |           |
            | BRIDGE_END   | 2013-01-01 11:02:45.0 |            | 0612345678 | s     | user        | 1376060558.17 | 1376060558.17 |           |
            | HANGUP       | 2013-01-01 11:02:45.0 | Bob Marley | 1002       |       | user        | 1376060558.18 | 1376060558.17 |           |
            | CHAN_END     | 2013-01-01 11:02:45.0 | Bob Marley | 1002       |       | user        | 1376060558.18 | 1376060558.17 |           |
            | HANGUP       | 2013-01-01 11:02:45.0 |            | 0612345678 | s     | user        | 1376060558.17 | 1376060558.17 |           |
            | CHAN_END     | 2013-01-01 11:02:45.0 |            | 0612345678 | s     | user        | 1376060558.17 | 1376060558.17 |           |
            | LINKEDID_END | 2013-01-01 11:02:45.0 |            | 0612345678 | s     | user        | 1376060558.17 | 1376060558.17 |           |
        When I generate call logs
        Then I should have the following call logs:
            | date                  | source_name | source_exten | destination_exten |  duration | user_field |
            | 2013-01-01 11:02:38.0 |   612345678 |    612345678 |              1002 | 0:00:03.0 |            |

    Scenario: Generation of answered outgoing call
        Given there are no calls
        Given I have the following CEL entries:
            | eventtype    | eventtime             | cid_name   | cid_num | exten      | context     | uniqueid      | linkedid      | userfield |
            | CHAN_START   | 2013-01-01 11:03:47.0 | Bob Marley | 1002    | 4185550155 | default     | 1376060627.21 | 1376060627.21 |           |
            | APP_START    | 2013-01-01 11:03:47.0 | Bob Marley | 1002    | dial       | outcall     | 1376060627.21 | 1376060627.21 |           |
            | CHAN_START   | 2013-01-01 11:03:47.0 |            |         | s          | from-extern | 1376060627.22 | 1376060627.21 |           |
            | ANSWER       | 2013-01-01 11:03:51.0 |            | dial    | dial       | from-extern | 1376060627.22 | 1376060627.21 |           |
            | ANSWER       | 2013-01-01 11:03:51.0 | Bob Marley | 1002    | dial       | outcall     | 1376060627.21 | 1376060627.21 |           |
            | BRIDGE_START | 2013-01-01 11:03:51.0 | Bob Marley | 1002    | dial       | outcall     | 1376060627.21 | 1376060627.21 |           |
            | BRIDGE_END   | 2013-01-01 11:03:54.0 | Bob Marley | 1002    | dial       | outcall     | 1376060627.21 | 1376060627.21 |           |
            | HANGUP       | 2013-01-01 11:03:54.0 |            | dial    |            | outcall     | 1376060627.22 | 1376060627.21 |           |
            | CHAN_END     | 2013-01-01 11:03:54.0 |            | dial    |            | outcall     | 1376060627.22 | 1376060627.21 |           |
            | HANGUP       | 2013-01-01 11:03:54.0 | Bob Marley | 1002    | dial       | outcall     | 1376060627.21 | 1376060627.21 |           |
            | CHAN_END     | 2013-01-01 11:03:54.0 | Bob Marley | 1002    | dial       | outcall     | 1376060627.21 | 1376060627.21 |           |
            | LINKEDID_END | 2013-01-01 11:03:54.0 | Bob Marley | 1002    | dial       | outcall     | 1376060627.21 | 1376060627.21 |           |
            | CHAN_START   | 2013-01-01 11:20:08.0 | Bob Marley | 1002    | 4185550155 | default     | 1376068808.35 | 1376068808.35 |           |
            | APP_START    | 2013-01-01 11:20:08.0 | Bob Marley | 1002    | dial       | outcall     | 1376068808.35 | 1376068808.35 | 00548AB33 |
            | CHAN_START   | 2013-01-01 11:20:08.0 |            |         | s          | from-extern | 1376068808.36 | 1376068808.35 |           |
            | ANSWER       | 2013-01-01 11:20:10.0 |            | dial    | dial       | from-extern | 1376068808.36 | 1376068808.35 |           |
            | ANSWER       | 2013-01-01 11:20:10.0 | Bob Marley | 1002    | dial       | outcall     | 1376068808.35 | 1376068808.35 | 00548AB33 |
            | BRIDGE_START | 2013-01-01 11:20:10.0 | Bob Marley | 1002    | dial       | outcall     | 1376068808.35 | 1376068808.35 | 00548AB33 |
            | BRIDGE_END   | 2013-01-01 11:20:13.0 | Bob Marley | 1002    | dial       | outcall     | 1376068808.35 | 1376068808.35 | 00548AB33 |
            | HANGUP       | 2013-01-01 11:20:13.0 |            | dial    |            | outcall     | 1376068808.36 | 1376068808.35 |           |
            | CHAN_END     | 2013-01-01 11:20:13.0 |            | dial    |            | outcall     | 1376068808.36 | 1376068808.35 |           |
            | HANGUP       | 2013-01-01 11:20:13.0 | Bob Marley | 1002    | dial       | outcall     | 1376068808.35 | 1376068808.35 | 00548AB33 |
            | CHAN_END     | 2013-01-01 11:20:13.0 | Bob Marley | 1002    | dial       | outcall     | 1376068808.35 | 1376068808.35 | 00548AB33 |
            | LINKEDID_END | 2013-01-01 11:20:13.0 | Bob Marley | 1002    | dial       | outcall     | 1376068808.35 | 1376068808.35 | 00548AB33 |
        When I generate call logs
        Then I should have the following call logs:
            | date                  | source_name | source_exten | destination_exten | duration  | user_field |
            | 2013-01-01 11:03:47.0 | Bob Marley  | 1002         | 4185550155        | 0:00:03.0 |            |
            | 2013-01-01 11:20:08.0 | Bob Marley  | 1002         | 4185550155        | 0:00:03.0 | 00548AB33  |