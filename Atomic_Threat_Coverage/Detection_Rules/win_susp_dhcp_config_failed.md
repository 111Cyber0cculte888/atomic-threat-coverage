| Title                | DHCP Server Error Failed Loading the CallOut DLL                                                                                                                                                 |
|:---------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Description          | This rule detects a DHCP server error in which a specified Callout DLL (in registry) could not be loaded                                                                                                                                           |
| ATT&amp;CK Tactic    | <ul></ul>  |
| ATT&amp;CK Technique | <ul></ul>                             |
| Data Needed          | <ul></ul>                                                         |
| Trigger              |  There is no Trigger for this technique yet.  |
| Severity Level       | critical                                                                                                                                                 |
| False Positives      | <ul><li>Unknown</li></ul>                                                                  |
| Development Status   | experimental                                                                                                                                                |
| References           | <ul><li>[https://blog.3or.de/mimilib-dhcp-server-callout-dll-injection.html](https://blog.3or.de/mimilib-dhcp-server-callout-dll-injection.html)</li><li>[https://technet.microsoft.com/en-us/library/cc726884(v=ws.10).aspx](https://technet.microsoft.com/en-us/library/cc726884(v=ws.10).aspx)</li><li>[https://msdn.microsoft.com/de-de/library/windows/desktop/aa363389(v=vs.85).aspx](https://msdn.microsoft.com/de-de/library/windows/desktop/aa363389(v=vs.85).aspx)</li></ul>                                                          |
| Author               | Dimitrios Slamaris                                                                                                                                                |


## Detection Rules

### Sigma rule

```
title: DHCP Server Error Failed Loading the CallOut DLL
description: This rule detects a DHCP server error in which a specified Callout DLL (in registry) could not be loaded
status: experimental
references:
    - https://blog.3or.de/mimilib-dhcp-server-callout-dll-injection.html
    - https://technet.microsoft.com/en-us/library/cc726884(v=ws.10).aspx
    - https://msdn.microsoft.com/de-de/library/windows/desktop/aa363389(v=vs.85).aspx
date: 2017/05/15
author: Dimitrios Slamaris
logsource:
    product: windows
    service: system
detection:
    selection:
          EventID: 
            - 1031
            - 1032
            - 1034
    condition: selection
falsepositives: 
    - Unknown
level: critical

```





### Kibana query

```
EventID:("1031" "1032" "1034")
```





### X-Pack Watcher

```
curl -s -XPUT -H \'Content-Type: application/json\' --data-binary @- localhost:9200/_xpack/watcher/watch/DHCP-Server-Error-Failed-Loading-the-CallOut-DLL <<EOF\n{\n  "trigger": {\n    "schedule": {\n      "interval": "30m"\n    }\n  },\n  "input": {\n    "search": {\n      "request": {\n        "body": {\n          "size": 0,\n          "query": {\n            "query_string": {\n              "query": "EventID:(\\"1031\\" \\"1032\\" \\"1034\\")",\n              "analyze_wildcard": true\n            }\n          }\n        },\n        "indices": []\n      }\n    }\n  },\n  "condition": {\n    "compare": {\n      "ctx.payload.hits.total": {\n        "not_eq": 0\n      }\n    }\n  },\n  "actions": {\n    "send_email": {\n      "email": {\n        "to": null,\n        "subject": "Sigma Rule \'DHCP Server Error Failed Loading the CallOut DLL\'",\n        "body": "Hits:\\n{{#ctx.payload.hits.hits}}{{_source}}\\n================================================================================\\n{{/ctx.payload.hits.hits}}",\n        "attachments": {\n          "data.json": {\n            "data": {\n              "format": "json"\n            }\n          }\n        }\n      }\n    }\n  }\n}\nEOF\n
```





### Graylog

```
EventID:("1031" "1032" "1034")
```





### Splunk

```
(EventID="1031" OR EventID="1032" OR EventID="1034")
```





### Logpoint

```
EventID IN ["1031", "1032", "1034"]
```





### Grep

```
grep -P '^(?:.*1031|.*1032|.*1034)'
```





### Fieldlist

```
EventID
```

