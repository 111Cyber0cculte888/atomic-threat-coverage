| Title                | System File Execution Location Anomaly                                                                                                                                                 |
|:---------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Description          | Detects a Windows program executable started in a suspicious folder                                                                                                                                           |
| ATT&amp;CK Tactic    | <ul><li>[TA0005: Defense Evasion](https://attack.mitre.org/tactics/TA0005)</li></ul>  |
| ATT&amp;CK Technique | <ul><li>[T1036: Masquerading](https://attack.mitre.org/techniques/T1036)</li></ul>                             |
| Data Needed          | <ul><li>[DN_0003_1_windows_sysmon_process_creation](../Data_Needed/DN_0003_1_windows_sysmon_process_creation.md)</li><li>[DN_0002_4688_windows_process_creation_with_commandline](../Data_Needed/DN_0002_4688_windows_process_creation_with_commandline.md)</li><li>[DN_0001_4688_windows_process_creation](../Data_Needed/DN_0001_4688_windows_process_creation.md)</li></ul>                                                         |
| Trigger              | <ul><li>[T1036: Masquerading](../Triggers/T1036.md)</li></ul>  |
| Severity Level       | high                                                                                                                                                 |
| False Positives      | <ul><li>Exotic software</li></ul>                                                                  |
| Development Status   | experimental                                                                                                                                                |
| References           | <ul><li>[https://twitter.com/GelosSnake/status/934900723426439170](https://twitter.com/GelosSnake/status/934900723426439170)</li></ul>                                                          |
| Author               | Florian Roth, Patrick Bareiss                                                                                                                                                |


## Detection Rules

### Sigma rule

```
title: System File Execution Location Anomaly
status: experimental
description: Detects a Windows program executable started in a suspicious folder
references:
    - https://twitter.com/GelosSnake/status/934900723426439170
author: Florian Roth, Patrick Bareiss
date: 2017/11/27
tags:
    - attack.defense_evasion
    - attack.t1036
logsource:
    category: process_creation
    product: windows
detection:
    selection:
        Image:
            - '*\svchost.exe'
            - '*\rundll32.exe'
            - '*\services.exe'
            - '*\powershell.exe'
            - '*\regsvr32.exe'
            - '*\spoolsv.exe'
            - '*\lsass.exe'
            - '*\smss.exe'
            - '*\csrss.exe'
            - '*\conhost.exe'
            - '*\wininit.exe'
            - '*\lsm.exe'
            - '*\winlogon.exe'
            - '*\explorer.exe'
            - '*\taskhost.exe' 
    filter:
        Image:
            - 'C:\Windows\System32\\*'
            - 'C:\Windows\SysWow64\\*'
    condition: selection and not filter
falsepositives:
    - Exotic software
level: high

```





### es-qs
    
```
(Image.keyword:(*\\\\svchost.exe *\\\\rundll32.exe *\\\\services.exe *\\\\powershell.exe *\\\\regsvr32.exe *\\\\spoolsv.exe *\\\\lsass.exe *\\\\smss.exe *\\\\csrss.exe *\\\\conhost.exe *\\\\wininit.exe *\\\\lsm.exe *\\\\winlogon.exe *\\\\explorer.exe *\\\\taskhost.exe) AND NOT (Image:("C\\:\\\\Windows\\\\System32\\\\*" "C\\:\\\\Windows\\\\SysWow64\\\\*")))
```


### xpack-watcher
    
```
curl -s -XPUT -H \'Content-Type: application/json\' --data-binary @- localhost:9200/_xpack/watcher/watch/System-File-Execution-Location-Anomaly <<EOF\n{\n  "trigger": {\n    "schedule": {\n      "interval": "30m"\n    }\n  },\n  "input": {\n    "search": {\n      "request": {\n        "body": {\n          "size": 0,\n          "query": {\n            "query_string": {\n              "query": "(Image.keyword:(*\\\\\\\\svchost.exe *\\\\\\\\rundll32.exe *\\\\\\\\services.exe *\\\\\\\\powershell.exe *\\\\\\\\regsvr32.exe *\\\\\\\\spoolsv.exe *\\\\\\\\lsass.exe *\\\\\\\\smss.exe *\\\\\\\\csrss.exe *\\\\\\\\conhost.exe *\\\\\\\\wininit.exe *\\\\\\\\lsm.exe *\\\\\\\\winlogon.exe *\\\\\\\\explorer.exe *\\\\\\\\taskhost.exe) AND NOT (Image:(\\"C\\\\:\\\\\\\\Windows\\\\\\\\System32\\\\\\\\*\\" \\"C\\\\:\\\\\\\\Windows\\\\\\\\SysWow64\\\\\\\\*\\")))",\n              "analyze_wildcard": true\n            }\n          }\n        },\n        "indices": []\n      }\n    }\n  },\n  "condition": {\n    "compare": {\n      "ctx.payload.hits.total": {\n        "not_eq": 0\n      }\n    }\n  },\n  "actions": {\n    "send_email": {\n      "email": {\n        "to": null,\n        "subject": "Sigma Rule \'System File Execution Location Anomaly\'",\n        "body": "Hits:\\n{{#ctx.payload.hits.hits}}{{_source}}\\n================================================================================\\n{{/ctx.payload.hits.hits}}",\n        "attachments": {\n          "data.json": {\n            "data": {\n              "format": "json"\n            }\n          }\n        }\n      }\n    }\n  }\n}\nEOF\n
```


### graylog
    
```
(Image:("*\\\\svchost.exe" "*\\\\rundll32.exe" "*\\\\services.exe" "*\\\\powershell.exe" "*\\\\regsvr32.exe" "*\\\\spoolsv.exe" "*\\\\lsass.exe" "*\\\\smss.exe" "*\\\\csrss.exe" "*\\\\conhost.exe" "*\\\\wininit.exe" "*\\\\lsm.exe" "*\\\\winlogon.exe" "*\\\\explorer.exe" "*\\\\taskhost.exe") AND NOT (Image:("C\\:\\\\Windows\\\\System32\\\\*" "C\\:\\\\Windows\\\\SysWow64\\\\*")))
```


### splunk
    
```
((Image="*\\\\svchost.exe" OR Image="*\\\\rundll32.exe" OR Image="*\\\\services.exe" OR Image="*\\\\powershell.exe" OR Image="*\\\\regsvr32.exe" OR Image="*\\\\spoolsv.exe" OR Image="*\\\\lsass.exe" OR Image="*\\\\smss.exe" OR Image="*\\\\csrss.exe" OR Image="*\\\\conhost.exe" OR Image="*\\\\wininit.exe" OR Image="*\\\\lsm.exe" OR Image="*\\\\winlogon.exe" OR Image="*\\\\explorer.exe" OR Image="*\\\\taskhost.exe") NOT ((Image="C:\\\\Windows\\\\System32\\\\*" OR Image="C:\\\\Windows\\\\SysWow64\\\\*")))
```


### logpoint
    
```
(Image IN ["*\\\\svchost.exe", "*\\\\rundll32.exe", "*\\\\services.exe", "*\\\\powershell.exe", "*\\\\regsvr32.exe", "*\\\\spoolsv.exe", "*\\\\lsass.exe", "*\\\\smss.exe", "*\\\\csrss.exe", "*\\\\conhost.exe", "*\\\\wininit.exe", "*\\\\lsm.exe", "*\\\\winlogon.exe", "*\\\\explorer.exe", "*\\\\taskhost.exe"]  -(Image IN ["C:\\\\Windows\\\\System32\\\\*", "C:\\\\Windows\\\\SysWow64\\\\*"]))
```


### grep
    
```
grep -P '^(?:.*(?=.*(?:.*.*\\svchost\\.exe|.*.*\\rundll32\\.exe|.*.*\\services\\.exe|.*.*\\powershell\\.exe|.*.*\\regsvr32\\.exe|.*.*\\spoolsv\\.exe|.*.*\\lsass\\.exe|.*.*\\smss\\.exe|.*.*\\csrss\\.exe|.*.*\\conhost\\.exe|.*.*\\wininit\\.exe|.*.*\\lsm\\.exe|.*.*\\winlogon\\.exe|.*.*\\explorer\\.exe|.*.*\\taskhost\\.exe))(?=.*(?!.*(?:.*(?=.*(?:.*C:\\Windows\\System32\\\\.*|.*C:\\Windows\\SysWow64\\\\.*))))))'
```



