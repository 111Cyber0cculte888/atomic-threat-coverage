| Title                | Suspicious Rundll32 Activity                                                                                                                                                 |
|:---------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Description          | Detects suspicious process related to rundll32 based on arguments                                                                                                                                           |
| ATT&amp;CK Tactic    | <ul><li>[TA0005: Defense Evasion](https://attack.mitre.org/tactics/TA0005)</li><li>[TA0002: Execution](https://attack.mitre.org/tactics/TA0002)</li></ul>  |
| ATT&amp;CK Technique | <ul><li>[T1085: Rundll32](https://attack.mitre.org/techniques/T1085)</li></ul>                             |
| Data Needed          | <ul><li>[DN_0001_4688_windows_process_creation](../Data_Needed/DN_0001_4688_windows_process_creation.md)</li><li>[DN_0003_1_windows_sysmon_process_creation](../Data_Needed/DN_0003_1_windows_sysmon_process_creation.md)</li><li>[DN_0002_4688_windows_process_creation_with_commandline](../Data_Needed/DN_0002_4688_windows_process_creation_with_commandline.md)</li></ul>                                                         |
| Trigger              | <ul><li>[T1085: Rundll32](../Triggers/T1085.md)</li></ul>  |
| Severity Level       |                                                                                                                                                  |
| False Positives      | <ul><li>False positives depend on scripts and administrative tools used in the monitored environment</li></ul>                                                                  |
| Development Status   | experimental                                                                                                                                                |
| References           | <ul><li>[http://www.hexacorn.com/blog/2017/05/01/running-programs-via-proxy-jumping-on-a-edr-bypass-trampoline/](http://www.hexacorn.com/blog/2017/05/01/running-programs-via-proxy-jumping-on-a-edr-bypass-trampoline/)</li><li>[https://twitter.com/Hexacorn/status/885258886428725250](https://twitter.com/Hexacorn/status/885258886428725250)</li><li>[https://gist.github.com/ryhanson/227229866af52e2d963cf941af135a52](https://gist.github.com/ryhanson/227229866af52e2d963cf941af135a52)</li></ul>                                                          |
| Author               | juju4                                                                                                                                                |


## Detection Rules

### Sigma rule

```
action: global
title: Suspicious Rundll32 Activity
description: Detects suspicious process related to rundll32 based on arguments
status: experimental
references:
    - http://www.hexacorn.com/blog/2017/05/01/running-programs-via-proxy-jumping-on-a-edr-bypass-trampoline/
    - https://twitter.com/Hexacorn/status/885258886428725250
    - https://gist.github.com/ryhanson/227229866af52e2d963cf941af135a52
tags:
    - attack.defense_evasion
    - attack.execution
    - attack.t1085
author: juju4
detection:
    selection:
        CommandLine:
            # match with or without rundll32.exe to try to catch evasion
            - '*\rundll32.exe* url.dll,*OpenURL *'
            - '*\rundll32.exe* url.dll,*OpenURLA *'
            - '*\rundll32.exe* url.dll,*FileProtocolHandler *'
            - '*\rundll32.exe* zipfldr.dll,*RouteTheCall *'
            - '*\rundll32.exe* Shell32.dll,*Control_RunDLL *'
            - '*\rundll32.exe javascript:*'
            - '* url.dll,*OpenURL *'
            - '* url.dll,*OpenURLA *'
            - '* url.dll,*FileProtocolHandler *'
            - '* zipfldr.dll,*RouteTheCall *'
            - '* Shell32.dll,*Control_RunDLL *'
            - '* javascript:*'
            - '*.RegisterXLL*'
    condition: selection
falsepositives:
    - False positives depend on scripts and administrative tools used in the monitored environment
---
# Windows Audit Log
logsource:
    product: windows
    service: security
    definition: 'Requirements: Audit Policy : Detailed Tracking > Audit Process creation, Group Policy : Administrative Templates\System\Audit Process Creation'
detection:
    selection:
        EventID: 4688
---
# Sysmon
logsource:
    product: windows
    service: sysmon
detection:
    selection:
        EventID: 1
level: medium

```




### esqs
    
```
(EventID:"4688" AND CommandLine.keyword:(*\\\\rundll32.exe*\\ url.dll,*OpenURL\\ * *\\\\rundll32.exe*\\ url.dll,*OpenURLA\\ * *\\\\rundll32.exe*\\ url.dll,*FileProtocolHandler\\ * *\\\\rundll32.exe*\\ zipfldr.dll,*RouteTheCall\\ * *\\\\rundll32.exe*\\ Shell32.dll,*Control_RunDLL\\ * *\\\\rundll32.exe\\ javascript\\:* *\\ url.dll,*OpenURL\\ * *\\ url.dll,*OpenURLA\\ * *\\ url.dll,*FileProtocolHandler\\ * *\\ zipfldr.dll,*RouteTheCall\\ * *\\ Shell32.dll,*Control_RunDLL\\ * *\\ javascript\\:* *.RegisterXLL*))\n(EventID:"1" AND CommandLine.keyword:(*\\\\rundll32.exe*\\ url.dll,*OpenURL\\ * *\\\\rundll32.exe*\\ url.dll,*OpenURLA\\ * *\\\\rundll32.exe*\\ url.dll,*FileProtocolHandler\\ * *\\\\rundll32.exe*\\ zipfldr.dll,*RouteTheCall\\ * *\\\\rundll32.exe*\\ Shell32.dll,*Control_RunDLL\\ * *\\\\rundll32.exe\\ javascript\\:* *\\ url.dll,*OpenURL\\ * *\\ url.dll,*OpenURLA\\ * *\\ url.dll,*FileProtocolHandler\\ * *\\ zipfldr.dll,*RouteTheCall\\ * *\\ Shell32.dll,*Control_RunDLL\\ * *\\ javascript\\:* *.RegisterXLL*))
```


### xpackwatcher
    
```
curl -s -XPUT -H \'Content-Type: application/json\' --data-binary @- localhost:9200/_xpack/watcher/watch/Suspicious-Rundll32-Activity <<EOF\n{\n  "trigger": {\n    "schedule": {\n      "interval": "30m"\n    }\n  },\n  "input": {\n    "search": {\n      "request": {\n        "body": {\n          "size": 0,\n          "query": {\n            "query_string": {\n              "query": "(EventID:\\"4688\\" AND CommandLine.keyword:(*\\\\\\\\rundll32.exe*\\\\ url.dll,*OpenURL\\\\ * *\\\\\\\\rundll32.exe*\\\\ url.dll,*OpenURLA\\\\ * *\\\\\\\\rundll32.exe*\\\\ url.dll,*FileProtocolHandler\\\\ * *\\\\\\\\rundll32.exe*\\\\ zipfldr.dll,*RouteTheCall\\\\ * *\\\\\\\\rundll32.exe*\\\\ Shell32.dll,*Control_RunDLL\\\\ * *\\\\\\\\rundll32.exe\\\\ javascript\\\\:* *\\\\ url.dll,*OpenURL\\\\ * *\\\\ url.dll,*OpenURLA\\\\ * *\\\\ url.dll,*FileProtocolHandler\\\\ * *\\\\ zipfldr.dll,*RouteTheCall\\\\ * *\\\\ Shell32.dll,*Control_RunDLL\\\\ * *\\\\ javascript\\\\:* *.RegisterXLL*))",\n              "analyze_wildcard": true\n            }\n          }\n        },\n        "indices": []\n      }\n    }\n  },\n  "condition": {\n    "compare": {\n      "ctx.payload.hits.total": {\n        "not_eq": 0\n      }\n    }\n  },\n  "actions": {\n    "send_email": {\n      "email": {\n        "to": null,\n        "subject": "Sigma Rule \'Suspicious Rundll32 Activity\'",\n        "body": "Hits:\\n{{#ctx.payload.hits.hits}}{{_source}}\\n================================================================================\\n{{/ctx.payload.hits.hits}}",\n        "attachments": {\n          "data.json": {\n            "data": {\n              "format": "json"\n            }\n          }\n        }\n      }\n    }\n  }\n}\nEOF\ncurl -s -XPUT -H \'Content-Type: application/json\' --data-binary @- localhost:9200/_xpack/watcher/watch/Suspicious-Rundll32-Activity-2 <<EOF\n{\n  "trigger": {\n    "schedule": {\n      "interval": "30m"\n    }\n  },\n  "input": {\n    "search": {\n      "request": {\n        "body": {\n          "size": 0,\n          "query": {\n            "query_string": {\n              "query": "(EventID:\\"1\\" AND CommandLine.keyword:(*\\\\\\\\rundll32.exe*\\\\ url.dll,*OpenURL\\\\ * *\\\\\\\\rundll32.exe*\\\\ url.dll,*OpenURLA\\\\ * *\\\\\\\\rundll32.exe*\\\\ url.dll,*FileProtocolHandler\\\\ * *\\\\\\\\rundll32.exe*\\\\ zipfldr.dll,*RouteTheCall\\\\ * *\\\\\\\\rundll32.exe*\\\\ Shell32.dll,*Control_RunDLL\\\\ * *\\\\\\\\rundll32.exe\\\\ javascript\\\\:* *\\\\ url.dll,*OpenURL\\\\ * *\\\\ url.dll,*OpenURLA\\\\ * *\\\\ url.dll,*FileProtocolHandler\\\\ * *\\\\ zipfldr.dll,*RouteTheCall\\\\ * *\\\\ Shell32.dll,*Control_RunDLL\\\\ * *\\\\ javascript\\\\:* *.RegisterXLL*))",\n              "analyze_wildcard": true\n            }\n          }\n        },\n        "indices": []\n      }\n    }\n  },\n  "condition": {\n    "compare": {\n      "ctx.payload.hits.total": {\n        "not_eq": 0\n      }\n    }\n  },\n  "actions": {\n    "send_email": {\n      "email": {\n        "to": null,\n        "subject": "Sigma Rule \'Suspicious Rundll32 Activity\'",\n        "body": "Hits:\\n{{#ctx.payload.hits.hits}}{{_source}}\\n================================================================================\\n{{/ctx.payload.hits.hits}}",\n        "attachments": {\n          "data.json": {\n            "data": {\n              "format": "json"\n            }\n          }\n        }\n      }\n    }\n  }\n}\nEOF\n
```


### graylog
    
```
(EventID:"4688" AND CommandLine:("*\\\\rundll32.exe* url.dll,*OpenURL *" "*\\\\rundll32.exe* url.dll,*OpenURLA *" "*\\\\rundll32.exe* url.dll,*FileProtocolHandler *" "*\\\\rundll32.exe* zipfldr.dll,*RouteTheCall *" "*\\\\rundll32.exe* Shell32.dll,*Control_RunDLL *" "*\\\\rundll32.exe javascript\\:*" "* url.dll,*OpenURL *" "* url.dll,*OpenURLA *" "* url.dll,*FileProtocolHandler *" "* zipfldr.dll,*RouteTheCall *" "* Shell32.dll,*Control_RunDLL *" "* javascript\\:*" "*.RegisterXLL*"))\n(EventID:"1" AND CommandLine:("*\\\\rundll32.exe* url.dll,*OpenURL *" "*\\\\rundll32.exe* url.dll,*OpenURLA *" "*\\\\rundll32.exe* url.dll,*FileProtocolHandler *" "*\\\\rundll32.exe* zipfldr.dll,*RouteTheCall *" "*\\\\rundll32.exe* Shell32.dll,*Control_RunDLL *" "*\\\\rundll32.exe javascript\\:*" "* url.dll,*OpenURL *" "* url.dll,*OpenURLA *" "* url.dll,*FileProtocolHandler *" "* zipfldr.dll,*RouteTheCall *" "* Shell32.dll,*Control_RunDLL *" "* javascript\\:*" "*.RegisterXLL*"))
```


### splunk
    
```
(EventID="4688" (CommandLine="*\\\\rundll32.exe* url.dll,*OpenURL *" OR CommandLine="*\\\\rundll32.exe* url.dll,*OpenURLA *" OR CommandLine="*\\\\rundll32.exe* url.dll,*FileProtocolHandler *" OR CommandLine="*\\\\rundll32.exe* zipfldr.dll,*RouteTheCall *" OR CommandLine="*\\\\rundll32.exe* Shell32.dll,*Control_RunDLL *" OR CommandLine="*\\\\rundll32.exe javascript:*" OR CommandLine="* url.dll,*OpenURL *" OR CommandLine="* url.dll,*OpenURLA *" OR CommandLine="* url.dll,*FileProtocolHandler *" OR CommandLine="* zipfldr.dll,*RouteTheCall *" OR CommandLine="* Shell32.dll,*Control_RunDLL *" OR CommandLine="* javascript:*" OR CommandLine="*.RegisterXLL*"))\n(EventID="1" (CommandLine="*\\\\rundll32.exe* url.dll,*OpenURL *" OR CommandLine="*\\\\rundll32.exe* url.dll,*OpenURLA *" OR CommandLine="*\\\\rundll32.exe* url.dll,*FileProtocolHandler *" OR CommandLine="*\\\\rundll32.exe* zipfldr.dll,*RouteTheCall *" OR CommandLine="*\\\\rundll32.exe* Shell32.dll,*Control_RunDLL *" OR CommandLine="*\\\\rundll32.exe javascript:*" OR CommandLine="* url.dll,*OpenURL *" OR CommandLine="* url.dll,*OpenURLA *" OR CommandLine="* url.dll,*FileProtocolHandler *" OR CommandLine="* zipfldr.dll,*RouteTheCall *" OR CommandLine="* Shell32.dll,*Control_RunDLL *" OR CommandLine="* javascript:*" OR CommandLine="*.RegisterXLL*"))
```


### logpoint
    
```
(EventID="4688" CommandLine IN ["*\\\\rundll32.exe* url.dll,*OpenURL *", "*\\\\rundll32.exe* url.dll,*OpenURLA *", "*\\\\rundll32.exe* url.dll,*FileProtocolHandler *", "*\\\\rundll32.exe* zipfldr.dll,*RouteTheCall *", "*\\\\rundll32.exe* Shell32.dll,*Control_RunDLL *", "*\\\\rundll32.exe javascript:*", "* url.dll,*OpenURL *", "* url.dll,*OpenURLA *", "* url.dll,*FileProtocolHandler *", "* zipfldr.dll,*RouteTheCall *", "* Shell32.dll,*Control_RunDLL *", "* javascript:*", "*.RegisterXLL*"])\n(EventID="1" CommandLine IN ["*\\\\rundll32.exe* url.dll,*OpenURL *", "*\\\\rundll32.exe* url.dll,*OpenURLA *", "*\\\\rundll32.exe* url.dll,*FileProtocolHandler *", "*\\\\rundll32.exe* zipfldr.dll,*RouteTheCall *", "*\\\\rundll32.exe* Shell32.dll,*Control_RunDLL *", "*\\\\rundll32.exe javascript:*", "* url.dll,*OpenURL *", "* url.dll,*OpenURLA *", "* url.dll,*FileProtocolHandler *", "* zipfldr.dll,*RouteTheCall *", "* Shell32.dll,*Control_RunDLL *", "* javascript:*", "*.RegisterXLL*"])
```


### grep
    
```
grep -P '^(?:.*(?=.*4688)(?=.*(?:.*.*\\rundll32\\.exe.* url\\.dll,.*OpenURL .*|.*.*\\rundll32\\.exe.* url\\.dll,.*OpenURLA .*|.*.*\\rundll32\\.exe.* url\\.dll,.*FileProtocolHandler .*|.*.*\\rundll32\\.exe.* zipfldr\\.dll,.*RouteTheCall .*|.*.*\\rundll32\\.exe.* Shell32\\.dll,.*Control_RunDLL .*|.*.*\\rundll32\\.exe javascript:.*|.*.* url\\.dll,.*OpenURL .*|.*.* url\\.dll,.*OpenURLA .*|.*.* url\\.dll,.*FileProtocolHandler .*|.*.* zipfldr\\.dll,.*RouteTheCall .*|.*.* Shell32\\.dll,.*Control_RunDLL .*|.*.* javascript:.*|.*.*\\.RegisterXLL.*)))'\ngrep -P '^(?:.*(?=.*1)(?=.*(?:.*.*\\rundll32\\.exe.* url\\.dll,.*OpenURL .*|.*.*\\rundll32\\.exe.* url\\.dll,.*OpenURLA .*|.*.*\\rundll32\\.exe.* url\\.dll,.*FileProtocolHandler .*|.*.*\\rundll32\\.exe.* zipfldr\\.dll,.*RouteTheCall .*|.*.*\\rundll32\\.exe.* Shell32\\.dll,.*Control_RunDLL .*|.*.*\\rundll32\\.exe javascript:.*|.*.* url\\.dll,.*OpenURL .*|.*.* url\\.dll,.*OpenURLA .*|.*.* url\\.dll,.*FileProtocolHandler .*|.*.* zipfldr\\.dll,.*RouteTheCall .*|.*.* Shell32\\.dll,.*Control_RunDLL .*|.*.* javascript:.*|.*.*\\.RegisterXLL.*)))'
```


