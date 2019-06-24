| Title                | RDP Sensitive Settings Changed                                                                                                                                                 |
|:---------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Description          | Detects changes to RDP terminal service sensitive settings                                                                                                                                           |
| ATT&amp;CK Tactic    | <ul><li>[TA0005: Defense Evasion](https://attack.mitre.org/tactics/TA0005)</li></ul>  |
| ATT&amp;CK Technique | <ul></ul>                             |
| Data Needed          | <ul><li>[DN_0017_13_windows_sysmon_RegistryEvent](../Data_Needed/DN_0017_13_windows_sysmon_RegistryEvent.md)</li></ul>                                                         |
| Trigger              |  There is no Trigger for this technique yet.  |
| Severity Level       | high                                                                                                                                                 |
| False Positives      | <ul><li>unknown</li></ul>                                                                  |
| Development Status   |                                                                                                                                                 |
| References           | <ul><li>[https://blog.menasec.net/2019/02/threat-hunting-rdp-hijacking-via.html](https://blog.menasec.net/2019/02/threat-hunting-rdp-hijacking-via.html)</li></ul>                                                          |
| Author               | Samir Bousseaden                                                                                                                                                |


## Detection Rules

### Sigma rule

```
title: RDP Sensitive Settings Changed
description: Detects changes to RDP terminal service sensitive settings
references:
    - https://blog.menasec.net/2019/02/threat-hunting-rdp-hijacking-via.html
date: 2019/04/03
author: Samir Bousseaden
logsource:
   product: windows
   service: sysmon
detection:
    selection_reg:
        EventID: 13 
        TargetObject: 
            - '*\services\TermService\Parameters\ServiceDll*'
            - '*\Control\Terminal Server\fSingleSessionPerUser*'
            - '*\Control\Terminal Server\fDenyTSConnections*'
    condition: selection_reg
tags:
    - attack.defense_evasion
falsepositives:
    - unknown
level: high

```





### es-qs
    
```
(EventID:"13" AND TargetObject.keyword:(*\\\\services\\\\TermService\\\\Parameters\\\\ServiceDll* *\\\\Control\\\\Terminal\\ Server\\\\fSingleSessionPerUser* *\\\\Control\\\\Terminal\\ Server\\\\fDenyTSConnections*))
```


### xpack-watcher
    
```
curl -s -XPUT -H \'Content-Type: application/json\' --data-binary @- localhost:9200/_watcher/watch/RDP-Sensitive-Settings-Changed <<EOF\n{\n  "metadata": {\n    "title": "RDP Sensitive Settings Changed",\n    "description": "Detects changes to RDP terminal service sensitive settings",\n    "tags": [\n      "attack.defense_evasion"\n    ]\n  },\n  "trigger": {\n    "schedule": {\n      "interval": "30m"\n    }\n  },\n  "input": {\n    "search": {\n      "request": {\n        "body": {\n          "size": 0,\n          "query": {\n            "query_string": {\n              "query": "(EventID:\\"13\\" AND TargetObject.keyword:(*\\\\\\\\services\\\\\\\\TermService\\\\\\\\Parameters\\\\\\\\ServiceDll* *\\\\\\\\Control\\\\\\\\Terminal\\\\ Server\\\\\\\\fSingleSessionPerUser* *\\\\\\\\Control\\\\\\\\Terminal\\\\ Server\\\\\\\\fDenyTSConnections*))",\n              "analyze_wildcard": true\n            }\n          }\n        },\n        "indices": []\n      }\n    }\n  },\n  "condition": {\n    "compare": {\n      "ctx.payload.hits.total": {\n        "not_eq": 0\n      }\n    }\n  },\n  "actions": {\n    "send_email": {\n      "email": {\n        "to": null,\n        "subject": "Sigma Rule \'RDP Sensitive Settings Changed\'",\n        "body": "Hits:\\n{{#ctx.payload.hits.hits}}{{_source}}\\n================================================================================\\n{{/ctx.payload.hits.hits}}",\n        "attachments": {\n          "data.json": {\n            "data": {\n              "format": "json"\n            }\n          }\n        }\n      }\n    }\n  }\n}\nEOF\n
```


### graylog
    
```
(EventID:"13" AND TargetObject:("*\\\\services\\\\TermService\\\\Parameters\\\\ServiceDll*" "*\\\\Control\\\\Terminal Server\\\\fSingleSessionPerUser*" "*\\\\Control\\\\Terminal Server\\\\fDenyTSConnections*"))
```


### splunk
    
```
(EventID="13" (TargetObject="*\\\\services\\\\TermService\\\\Parameters\\\\ServiceDll*" OR TargetObject="*\\\\Control\\\\Terminal Server\\\\fSingleSessionPerUser*" OR TargetObject="*\\\\Control\\\\Terminal Server\\\\fDenyTSConnections*"))
```


### logpoint
    
```
(EventID="13" TargetObject IN ["*\\\\services\\\\TermService\\\\Parameters\\\\ServiceDll*", "*\\\\Control\\\\Terminal Server\\\\fSingleSessionPerUser*", "*\\\\Control\\\\Terminal Server\\\\fDenyTSConnections*"])
```


### grep
    
```
grep -P '^(?:.*(?=.*13)(?=.*(?:.*.*\\services\\TermService\\Parameters\\ServiceDll.*|.*.*\\Control\\Terminal Server\\fSingleSessionPerUser.*|.*.*\\Control\\Terminal Server\\fDenyTSConnections.*)))'
```



