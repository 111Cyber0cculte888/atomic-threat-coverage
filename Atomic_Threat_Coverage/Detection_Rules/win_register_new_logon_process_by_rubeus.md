| Title                | Register new logon process by Rubeus                                                                                                                                                 |
|:---------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Description          | Detects potential use of Rubeus via registered new trusted logon process                                                                                                                                           |
| ATT&amp;CK Tactic    |  <ul><li>[TA0008: Lateral Movement](https://attack.mitre.org/tactics/TA0008)</li><li>[TA0004: Privilege Escalation](https://attack.mitre.org/tactics/TA0004)</li></ul>  |
| ATT&amp;CK Technique | <ul><li>[T1208: Kerberoasting](https://attack.mitre.org/techniques/T1208)</li></ul>  |
| Data Needed          |  There is no documented Data Needed for this Detection Rule yet  |
| Enrichment           |  Data for this Detection Rule doesn't require any Enrichments.  |
| Trigger              | <ul><li>[T1208: Kerberoasting](../Triggers/T1208.md)</li></ul>  |
| Severity Level       | high |
| False Positives      | <ul><li>Unkown</li></ul>  |
| Development Status   | experimental |
| References           | <ul><li>[https://posts.specterops.io/hunting-in-active-directory-unconstrained-delegation-forests-trusts-71f2b33688e1](https://posts.specterops.io/hunting-in-active-directory-unconstrained-delegation-forests-trusts-71f2b33688e1)</li></ul>  |
| Author               | Roberto Rodriguez (source), Ilyas Ochkov (rule), oscd.community |


## Detection Rules

### Sigma rule

```
title: Register new logon process by Rubeus
id: 12e6d621-194f-4f59-90cc-1959e21e69f7
description: Detects potential use of Rubeus via registered new trusted logon process
status: experimental
references:
    - https://posts.specterops.io/hunting-in-active-directory-unconstrained-delegation-forests-trusts-71f2b33688e1
tags:
    - attack.lateral_movement
    - attack.privilege_escalation
    - attack.t1208
author: Roberto Rodriguez (source), Ilyas Ochkov (rule), oscd.community
date: 2019/10/24
logsource:
    product: windows
    service: security
    definition: Ubnormal logon process name 'User32LogonProcesss' - with three 's' at the end
detection:
    selection:
        - EventID: 4611
          LogonProcessName: 'User32LogonProcesss'
    condition: selection
falsepositives:
    - Unkown
level: high

```





### es-qs
    
```
(EventID:"4611" AND LogonProcessName:"User32LogonProcesss")
```


### xpack-watcher
    
```
curl -s -XPUT -H \'Content-Type: application/json\' --data-binary @- localhost:9200/_watcher/watch/Register-new-logon-process-by-Rubeus <<EOF\n{\n  "metadata": {\n    "title": "Register new logon process by Rubeus",\n    "description": "Detects potential use of Rubeus via registered new trusted logon process",\n    "tags": [\n      "attack.lateral_movement",\n      "attack.privilege_escalation",\n      "attack.t1208"\n    ],\n    "query": "(EventID:\\"4611\\" AND LogonProcessName:\\"User32LogonProcesss\\")"\n  },\n  "trigger": {\n    "schedule": {\n      "interval": "30m"\n    }\n  },\n  "input": {\n    "search": {\n      "request": {\n        "body": {\n          "size": 0,\n          "query": {\n            "bool": {\n              "must": [\n                {\n                  "query_string": {\n                    "query": "(EventID:\\"4611\\" AND LogonProcessName:\\"User32LogonProcesss\\")",\n                    "analyze_wildcard": true\n                  }\n                }\n              ],\n              "filter": {\n                "range": {\n                  "timestamp": {\n                    "gte": "now-30m/m"\n                  }\n                }\n              }\n            }\n          }\n        },\n        "indices": []\n      }\n    }\n  },\n  "condition": {\n    "compare": {\n      "ctx.payload.hits.total": {\n        "not_eq": 0\n      }\n    }\n  },\n  "actions": {\n    "send_email": {\n      "email": {\n        "to": "root@localhost",\n        "subject": "Sigma Rule \'Register new logon process by Rubeus\'",\n        "body": "Hits:\\n{{#ctx.payload.hits.hits}}{{_source}}\\n================================================================================\\n{{/ctx.payload.hits.hits}}",\n        "attachments": {\n          "data.json": {\n            "data": {\n              "format": "json"\n            }\n          }\n        }\n      }\n    }\n  }\n}\nEOF\n
```


### graylog
    
```
(EventID:"4611" AND LogonProcessName:"User32LogonProcesss")
```


### splunk
    
```
(EventID="4611" LogonProcessName="User32LogonProcesss")
```


### logpoint
    
```
(event_source="Microsoft-Windows-Security-Auditing" event_id="4611" logon_process="User32LogonProcesss")
```


### grep
    
```
grep -P '^(?:.*(?=.*4611)(?=.*User32LogonProcesss))'
```



