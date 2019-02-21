| Title                | Execution in Non-Executable Folder                                                                                                                                                 |
|:---------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Description          | Detects a suspicious exection from an uncommon folder                                                                                                                                           |
| ATT&amp;CK Tactic    | <ul></ul>  |
| ATT&amp;CK Technique | <ul></ul>                             |
| Data Needed          | <ul><li>[DN_0003_1_windows_sysmon_process_creation](../Data_Needed/DN_0003_1_windows_sysmon_process_creation.md)</li></ul>                                                         |
| Trigger              |  There is no Trigger for this technique yet.  |
| Severity Level       | high                                                                                                                                                 |
| False Positives      | <ul><li>Unknown</li></ul>                                                                  |
| Development Status   | experimental                                                                                                                                                |
| References           | <ul></ul>                                                          |
| Author               | Florian Roth                                                                                                                                                |


## Detection Rules

### Sigma rule

```
title: Execution in Non-Executable Folder
status: experimental
description: Detects a suspicious exection from an uncommon folder
author: Florian Roth
logsource:
    product: windows
    service: sysmon
detection:
    selection:
        EventID: 1
        Image: 
            - '*\$Recycle.bin'
            - '*\Users\All Users\*'
            - '*\Users\Default\*'
            - '*\Users\Public\*'
            - 'C:\Perflogs\*'
            - '*\config\systemprofile\*'
            - '*\Windows\Fonts\*'
            - '*\Windows\IME\*'
            - '*\Windows\addins\*'       
    condition: selection
fields:
    - CommandLine
    - ParentCommandLine
falsepositives:
    - Unknown
level: high

```





### Kibana query

```
(EventID:"1" AND Image.keyword:(*\\\\$Recycle.bin *\\\\Users\\\\All\\ Users\\* *\\\\Users\\\\Default\\* *\\\\Users\\\\Public\\* C\\:\\\\Perflogs\\* *\\\\config\\\\systemprofile\\* *\\\\Windows\\\\Fonts\\* *\\\\Windows\\\\IME\\* *\\\\Windows\\\\addins\\*))
```





### X-Pack Watcher

```
curl -s -XPUT -H \'Content-Type: application/json\' --data-binary @- localhost:9200/_xpack/watcher/watch/Execution-in-Non-Executable-Folder <<EOF\n{\n  "trigger": {\n    "schedule": {\n      "interval": "30m"\n    }\n  },\n  "input": {\n    "search": {\n      "request": {\n        "body": {\n          "size": 0,\n          "query": {\n            "query_string": {\n              "query": "(EventID:\\"1\\" AND Image.keyword:(*\\\\\\\\$Recycle.bin *\\\\\\\\Users\\\\\\\\All\\\\ Users\\\\* *\\\\\\\\Users\\\\\\\\Default\\\\* *\\\\\\\\Users\\\\\\\\Public\\\\* C\\\\:\\\\\\\\Perflogs\\\\* *\\\\\\\\config\\\\\\\\systemprofile\\\\* *\\\\\\\\Windows\\\\\\\\Fonts\\\\* *\\\\\\\\Windows\\\\\\\\IME\\\\* *\\\\\\\\Windows\\\\\\\\addins\\\\*))",\n              "analyze_wildcard": true\n            }\n          }\n        },\n        "indices": []\n      }\n    }\n  },\n  "condition": {\n    "compare": {\n      "ctx.payload.hits.total": {\n        "not_eq": 0\n      }\n    }\n  },\n  "actions": {\n    "send_email": {\n      "email": {\n        "to": null,\n        "subject": "Sigma Rule \'Execution in Non-Executable Folder\'",\n        "body": "Hits:\\n{{#ctx.payload.hits.hits}}Hit on {{_source.@timestamp}}:\\n      CommandLine = {{_source.CommandLine}}\\nParentCommandLine = {{_source.ParentCommandLine}}================================================================================\\n{{/ctx.payload.hits.hits}}",\n        "attachments": {\n          "data.json": {\n            "data": {\n              "format": "json"\n            }\n          }\n        }\n      }\n    }\n  }\n}\nEOF\n
```





### Graylog

```
(EventID:"1" AND Image:("*\\\\$Recycle.bin" "*\\\\Users\\\\All Users\\*" "*\\\\Users\\\\Default\\*" "*\\\\Users\\\\Public\\*" "C\\:\\\\Perflogs\\*" "*\\\\config\\\\systemprofile\\*" "*\\\\Windows\\\\Fonts\\*" "*\\\\Windows\\\\IME\\*" "*\\\\Windows\\\\addins\\*"))
```

