| Title                | Reconnaissance Activity                                                                                                                                                 |
|:---------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Description          | Detects activity as "net user administrator /domain" and "net group domain admins /domain"                                                                                                                                           |
| ATT&amp;CK Tactic    | <ul><li>[TA0007: Discovery](https://attack.mitre.org/tactics/TA0007)</li></ul>  |
| ATT&amp;CK Technique | <ul><li>[T1087: Account Discovery](https://attack.mitre.org/techniques/T1087)</li><li>[T1069: Permission Groups Discovery](https://attack.mitre.org/techniques/T1069)</li></ul>                             |
| Data Needed          | <ul><li>[DN_0030_4662_operation_was_performed_on_an_object](../Data_Needed/DN_0030_4662_operation_was_performed_on_an_object.md)</li><li>[DN_0029_4661_handle_to_an_object_was_requested](../Data_Needed/DN_0029_4661_handle_to_an_object_was_requested.md)</li></ul>                                                         |
| Trigger              | <ul><li>[T1087: Account Discovery](../Triggers/T1087.md)</li><li>[T1069: Permission Groups Discovery](../Triggers/T1069.md)</li></ul>  |
| Severity Level       | high                                                                                                                                                 |
| False Positives      | <ul><li>Administrator activity</li><li>Penetration tests</li></ul>                                                                  |
| Development Status   | experimental                                                                                                                                                |
| References           | <ul><li>[https://findingbad.blogspot.de/2017/01/hunting-what-does-it-look-like.html](https://findingbad.blogspot.de/2017/01/hunting-what-does-it-look-like.html)</li></ul>                                                          |
| Author               | Florian Roth (rule), Jack Croock (method)                                                                                                                                                |
| Other Tags           | <ul><li>attack.s0039</li><li>attack.s0039</li></ul> | 

## Detection Rules

### Sigma rule

```
title: Reconnaissance Activity
status: experimental
description: 'Detects activity as "net user administrator /domain" and "net group domain admins /domain"'
references:
    - https://findingbad.blogspot.de/2017/01/hunting-what-does-it-look-like.html
author: Florian Roth (rule), Jack Croock (method)
tags:
    - attack.discovery
    - attack.t1087
    - attack.t1069
    - attack.s0039
logsource:
    product: windows
    service: security
    definition: The volume of Event ID 4661 is high on Domain Controllers and therefore "Audit SAM" and "Audit Kernel Object" advanced audit policy settings are not configured in the recommandations for server systems
detection:
    selection:
        - EventID: 4661
          ObjectType: 'SAM_USER'
          ObjectName: 'S-1-5-21-*-500'
          AccessMask: '0x2d'
        - EventID: 4661
          ObjectType: 'SAM_GROUP'
          ObjectName: 'S-1-5-21-*-512'
          AccessMask: '0x2d'
    condition: selection
falsepositives:
    - Administrator activity
    - Penetration tests
level: high

```





### Kibana query

```
(EventID:"4661" AND AccessMask:"0x2d" AND ((ObjectType:"SAM_USER" AND ObjectName.keyword:S\\-1\\-5\\-21\\-*\\-500) OR (ObjectType:"SAM_GROUP" AND ObjectName.keyword:S\\-1\\-5\\-21\\-*\\-512)))
```





### X-Pack Watcher

```
curl -s -XPUT -H \'Content-Type: application/json\' --data-binary @- localhost:9200/_xpack/watcher/watch/Reconnaissance-Activity <<EOF\n{\n  "trigger": {\n    "schedule": {\n      "interval": "30m"\n    }\n  },\n  "input": {\n    "search": {\n      "request": {\n        "body": {\n          "size": 0,\n          "query": {\n            "query_string": {\n              "query": "(EventID:\\"4661\\" AND AccessMask:\\"0x2d\\" AND ((ObjectType:\\"SAM_USER\\" AND ObjectName.keyword:S\\\\-1\\\\-5\\\\-21\\\\-*\\\\-500) OR (ObjectType:\\"SAM_GROUP\\" AND ObjectName.keyword:S\\\\-1\\\\-5\\\\-21\\\\-*\\\\-512)))",\n              "analyze_wildcard": true\n            }\n          }\n        },\n        "indices": []\n      }\n    }\n  },\n  "condition": {\n    "compare": {\n      "ctx.payload.hits.total": {\n        "not_eq": 0\n      }\n    }\n  },\n  "actions": {\n    "send_email": {\n      "email": {\n        "to": null,\n        "subject": "Sigma Rule \'Reconnaissance Activity\'",\n        "body": "Hits:\\n{{#ctx.payload.hits.hits}}{{_source}}\\n================================================================================\\n{{/ctx.payload.hits.hits}}",\n        "attachments": {\n          "data.json": {\n            "data": {\n              "format": "json"\n            }\n          }\n        }\n      }\n    }\n  }\n}\nEOF\n
```





### Graylog

```
(EventID:"4661" AND AccessMask:"0x2d" AND ((ObjectType:"SAM_USER" AND ObjectName:"S\\-1\\-5\\-21\\-*\\-500") OR (ObjectType:"SAM_GROUP" AND ObjectName:"S\\-1\\-5\\-21\\-*\\-512")))
```

