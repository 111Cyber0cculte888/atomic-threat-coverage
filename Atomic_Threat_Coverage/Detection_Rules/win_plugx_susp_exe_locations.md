| Title                | Executable used by PlugX in Uncommon Location                                                                                                                                                 |
|:---------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Description          | Detects the execution of an executable that is typically used by PlugX for DLL side loading started from an uncommon location                                                                                                                                           |
| ATT&amp;CK Tactic    | <ul></ul>  |
| ATT&amp;CK Technique | <ul></ul>                             |
| Data Needed          | <ul><li>[DN_0001_4688_windows_process_creation](../Data_Needed/DN_0001_4688_windows_process_creation.md)</li><li>[DN_0002_4688_windows_process_creation_with_commandline](../Data_Needed/DN_0002_4688_windows_process_creation_with_commandline.md)</li></ul>                                                         |
| Trigger              |  There is no Trigger for this technique yet.  |
| Severity Level       | high                                                                                                                                                 |
| False Positives      | <ul><li>Unknown</li></ul>                                                                  |
| Development Status   | experimental                                                                                                                                                |
| References           | <ul><li>[http://www.hexacorn.com/blog/2016/03/10/beyond-good-ol-run-key-part-36/](http://www.hexacorn.com/blog/2016/03/10/beyond-good-ol-run-key-part-36/)</li><li>[https://countuponsecurity.com/2017/06/07/threat-hunting-in-the-enterprise-with-appcompatprocessor/](https://countuponsecurity.com/2017/06/07/threat-hunting-in-the-enterprise-with-appcompatprocessor/)</li></ul>                                                          |
| Author               | Florian Roth                                                                                                                                                |
| Other Tags           | <ul><li>attack.s0013</li><li>attack.s0013</li></ul> | 

## Detection Rules

### Sigma rule

```
title: Executable used by PlugX in Uncommon Location
status: experimental
description: Detects the execution of an executable that is typically used by PlugX for DLL side loading started from an uncommon location
references:
    - 'http://www.hexacorn.com/blog/2016/03/10/beyond-good-ol-run-key-part-36/'
    - 'https://countuponsecurity.com/2017/06/07/threat-hunting-in-the-enterprise-with-appcompatprocessor/'
author: Florian Roth
date: 2017/06/12
tags:
    - attack.s0013
logsource:
    product: windows
    service: security
detection:

    # CamMute
    selection_cammute:
        EventID: 4688
        CommandLine: '*\CamMute.exe'
    filter_cammute:
        EventID: 4688
        CommandLine: '*\Lenovo\Communication Utility\*'

    # Chrome Frame Helper
    selection_chrome_frame:
        EventID: 4688
        CommandLine: '*\chrome_frame_helper.exe'
    filter_chrome_frame:
        EventID: 4688
        CommandLine: '*\Google\Chrome\application\*'    

    # Microsoft Device Emulator
    selection_devemu:
        EventID: 4688
        CommandLine: '*\dvcemumanager.exe'
    filter_devemu:
        EventID: 4688
        CommandLine: '*\Microsoft Device Emulator\*'   

    # Windows Media Player Gadget
    selection_gadget:
        EventID: 4688
        CommandLine: '*\Gadget.exe'
    filter_gadget:
        EventID: 4688
        CommandLine: '*\Windows Media Player\*'

    # HTML Help Workshop
    selection_hcc:
        EventID: 4688
        CommandLine: '*\hcc.exe'
    filter_hcc:
        EventID: 4688
        CommandLine: '*\HTML Help Workshop\*'

    # Hotkey Command Module for Intel Graphics Contollers
    selection_hkcmd:
        EventID: 4688
        CommandLine: '*\hkcmd.exe'
    filter_hkcmd:
        EventID: 4688
        CommandLine: 
            - '*\System32\*'
            - '*\SysNative\*'
            - '*\SysWowo64\*'

    # McAfee component
    selection_mc:
        EventID: 4688
        CommandLine: '*\Mc.exe'
    filter_mc:
        EventID: 4688
        CommandLine: 
            - '*\Microsoft Visual Studio*'
            - '*\Microsoft SDK*'
            - '*\Windows Kit*'

    # MsMpEng - Microsoft Malware Protection Engine
    selection_msmpeng:
        EventID: 4688
        CommandLine: '*\MsMpEng.exe'
    filter_msmpeng:
        EventID: 4688
        CommandLine: 
            - '*\Microsoft Security Client\*'
            - '*\Windows Defender\*'
            - '*\AntiMalware\*'

    # Microsoft Security Center
    selection_msseces:
        EventID: 4688
        CommandLine: '*\msseces.exe'
    filter_msseces:
        EventID: 4688
        CommandLine: '*\Microsoft Security Center\*'

    # Microsoft Office 2003 OInfo
    selection_oinfo:
        EventID: 4688
        CommandLine: '*\OInfoP11.exe'
    filter_oinfo:
        EventID: 4688
        CommandLine: '*\Common Files\Microsoft Shared\*'      

    # OLE View
    selection_oleview:
        EventID: 4688
        CommandLine: '*\OleView.exe'
    filter_oleview:
        EventID: 4688
        CommandLine: 
            - '*\Microsoft Visual Studio*'
            - '*\Microsoft SDK*'
            - '*\Windows Kit*'   
            - '*\Windows Resource Kit\*'

    # RC
    selection_rc:
        EventID: 4688
        CommandLine: '*\OleView.exe'
    filter_rc:
        EventID: 4688
        CommandLine: 
            - '*\Microsoft Visual Studio*'
            - '*\Microsoft SDK*'
            - '*\Windows Kit*'   
            - '*\Windows Resource Kit\*'
            - '*\Microsoft.NET\*'  

    condition: ( selection_cammute and not filter_cammute ) or  
                ( selection_chrome_frame and not filter_chrome_frame ) or
                ( selection_devemu and not filter_devemu ) or
                ( selection_gadget and not filter_gadget ) or 
                ( selection_hcc and not filter_hcc ) or 
                ( selection_hkcmd and not filter_hkcmd ) or 
                ( selection_mc and not filter_mc ) or
                ( selection_msmpeng and not filter_msmpeng ) or
                ( selection_msseces and not filter_msseces ) or
                ( selection_oinfo and not filter_oinfo ) or 
                ( selection_oleview and not filter_oleview ) or 
                ( selection_rc and not filter_rc ) 
falsepositives:
    - Unknown
level: high



```




### es-qs
    
```
(((((((((((((EventID:"4688" AND CommandLine.keyword:*\\\\CamMute.exe) AND NOT (EventID:"4688" AND CommandLine.keyword:*\\\\Lenovo\\\\Communication\\ Utility\\*)) OR ((EventID:"4688" AND CommandLine.keyword:*\\\\chrome_frame_helper.exe) AND NOT (EventID:"4688" AND CommandLine.keyword:*\\\\Google\\\\Chrome\\\\application\\*))) OR ((EventID:"4688" AND CommandLine.keyword:*\\\\dvcemumanager.exe) AND NOT (EventID:"4688" AND CommandLine.keyword:*\\\\Microsoft\\ Device\\ Emulator\\*))) OR ((EventID:"4688" AND CommandLine.keyword:*\\\\Gadget.exe) AND NOT (EventID:"4688" AND CommandLine.keyword:*\\\\Windows\\ Media\\ Player\\*))) OR ((EventID:"4688" AND CommandLine.keyword:*\\\\hcc.exe) AND NOT (EventID:"4688" AND CommandLine.keyword:*\\\\HTML\\ Help\\ Workshop\\*))) OR ((EventID:"4688" AND CommandLine.keyword:*\\\\hkcmd.exe) AND NOT (EventID:"4688" AND CommandLine.keyword:(*\\\\System32\\* *\\\\SysNative\\* *\\\\SysWowo64\\*)))) OR ((EventID:"4688" AND CommandLine.keyword:*\\\\Mc.exe) AND NOT (EventID:"4688" AND CommandLine.keyword:(*\\\\Microsoft\\ Visual\\ Studio* *\\\\Microsoft\\ SDK* *\\\\Windows\\ Kit*)))) OR ((EventID:"4688" AND CommandLine.keyword:*\\\\MsMpEng.exe) AND NOT (EventID:"4688" AND CommandLine.keyword:(*\\\\Microsoft\\ Security\\ Client\\* *\\\\Windows\\ Defender\\* *\\\\AntiMalware\\*)))) OR ((EventID:"4688" AND CommandLine.keyword:*\\\\msseces.exe) AND NOT (EventID:"4688" AND CommandLine.keyword:*\\\\Microsoft\\ Security\\ Center\\*))) OR ((EventID:"4688" AND CommandLine.keyword:*\\\\OInfoP11.exe) AND NOT (EventID:"4688" AND CommandLine.keyword:*\\\\Common\\ Files\\\\Microsoft\\ Shared\\*))) OR ((EventID:"4688" AND CommandLine.keyword:*\\\\OleView.exe) AND NOT (EventID:"4688" AND CommandLine.keyword:(*\\\\Microsoft\\ Visual\\ Studio* *\\\\Microsoft\\ SDK* *\\\\Windows\\ Kit* *\\\\Windows\\ Resource\\ Kit\\*)))) OR ((EventID:"4688" AND CommandLine.keyword:*\\\\OleView.exe) AND NOT (EventID:"4688" AND CommandLine.keyword:(*\\\\Microsoft\\ Visual\\ Studio* *\\\\Microsoft\\ SDK* *\\\\Windows\\ Kit* *\\\\Windows\\ Resource\\ Kit\\* *\\\\Microsoft.NET\\*))))
```


### xpack-watcher
    
```
curl -s -XPUT -H \'Content-Type: application/json\' --data-binary @- localhost:9200/_xpack/watcher/watch/Executable-used-by-PlugX-in-Uncommon-Location <<EOF\n{\n  "trigger": {\n    "schedule": {\n      "interval": "30m"\n    }\n  },\n  "input": {\n    "search": {\n      "request": {\n        "body": {\n          "size": 0,\n          "query": {\n            "query_string": {\n              "query": "(((((((((((((EventID:\\"4688\\" AND CommandLine.keyword:*\\\\\\\\CamMute.exe) AND NOT (EventID:\\"4688\\" AND CommandLine.keyword:*\\\\\\\\Lenovo\\\\\\\\Communication\\\\ Utility\\\\*)) OR ((EventID:\\"4688\\" AND CommandLine.keyword:*\\\\\\\\chrome_frame_helper.exe) AND NOT (EventID:\\"4688\\" AND CommandLine.keyword:*\\\\\\\\Google\\\\\\\\Chrome\\\\\\\\application\\\\*))) OR ((EventID:\\"4688\\" AND CommandLine.keyword:*\\\\\\\\dvcemumanager.exe) AND NOT (EventID:\\"4688\\" AND CommandLine.keyword:*\\\\\\\\Microsoft\\\\ Device\\\\ Emulator\\\\*))) OR ((EventID:\\"4688\\" AND CommandLine.keyword:*\\\\\\\\Gadget.exe) AND NOT (EventID:\\"4688\\" AND CommandLine.keyword:*\\\\\\\\Windows\\\\ Media\\\\ Player\\\\*))) OR ((EventID:\\"4688\\" AND CommandLine.keyword:*\\\\\\\\hcc.exe) AND NOT (EventID:\\"4688\\" AND CommandLine.keyword:*\\\\\\\\HTML\\\\ Help\\\\ Workshop\\\\*))) OR ((EventID:\\"4688\\" AND CommandLine.keyword:*\\\\\\\\hkcmd.exe) AND NOT (EventID:\\"4688\\" AND CommandLine.keyword:(*\\\\\\\\System32\\\\* *\\\\\\\\SysNative\\\\* *\\\\\\\\SysWowo64\\\\*)))) OR ((EventID:\\"4688\\" AND CommandLine.keyword:*\\\\\\\\Mc.exe) AND NOT (EventID:\\"4688\\" AND CommandLine.keyword:(*\\\\\\\\Microsoft\\\\ Visual\\\\ Studio* *\\\\\\\\Microsoft\\\\ SDK* *\\\\\\\\Windows\\\\ Kit*)))) OR ((EventID:\\"4688\\" AND CommandLine.keyword:*\\\\\\\\MsMpEng.exe) AND NOT (EventID:\\"4688\\" AND CommandLine.keyword:(*\\\\\\\\Microsoft\\\\ Security\\\\ Client\\\\* *\\\\\\\\Windows\\\\ Defender\\\\* *\\\\\\\\AntiMalware\\\\*)))) OR ((EventID:\\"4688\\" AND CommandLine.keyword:*\\\\\\\\msseces.exe) AND NOT (EventID:\\"4688\\" AND CommandLine.keyword:*\\\\\\\\Microsoft\\\\ Security\\\\ Center\\\\*))) OR ((EventID:\\"4688\\" AND CommandLine.keyword:*\\\\\\\\OInfoP11.exe) AND NOT (EventID:\\"4688\\" AND CommandLine.keyword:*\\\\\\\\Common\\\\ Files\\\\\\\\Microsoft\\\\ Shared\\\\*))) OR ((EventID:\\"4688\\" AND CommandLine.keyword:*\\\\\\\\OleView.exe) AND NOT (EventID:\\"4688\\" AND CommandLine.keyword:(*\\\\\\\\Microsoft\\\\ Visual\\\\ Studio* *\\\\\\\\Microsoft\\\\ SDK* *\\\\\\\\Windows\\\\ Kit* *\\\\\\\\Windows\\\\ Resource\\\\ Kit\\\\*)))) OR ((EventID:\\"4688\\" AND CommandLine.keyword:*\\\\\\\\OleView.exe) AND NOT (EventID:\\"4688\\" AND CommandLine.keyword:(*\\\\\\\\Microsoft\\\\ Visual\\\\ Studio* *\\\\\\\\Microsoft\\\\ SDK* *\\\\\\\\Windows\\\\ Kit* *\\\\\\\\Windows\\\\ Resource\\\\ Kit\\\\* *\\\\\\\\Microsoft.NET\\\\*))))",\n              "analyze_wildcard": true\n            }\n          }\n        },\n        "indices": []\n      }\n    }\n  },\n  "condition": {\n    "compare": {\n      "ctx.payload.hits.total": {\n        "not_eq": 0\n      }\n    }\n  },\n  "actions": {\n    "send_email": {\n      "email": {\n        "to": null,\n        "subject": "Sigma Rule \'Executable used by PlugX in Uncommon Location\'",\n        "body": "Hits:\\n{{#ctx.payload.hits.hits}}{{_source}}\\n================================================================================\\n{{/ctx.payload.hits.hits}}",\n        "attachments": {\n          "data.json": {\n            "data": {\n              "format": "json"\n            }\n          }\n        }\n      }\n    }\n  }\n}\nEOF\n
```


### graylog
    
```
(((((((((((((EventID:"4688" AND CommandLine:"*\\\\CamMute.exe") AND NOT (EventID:"4688" AND CommandLine:"*\\\\Lenovo\\\\Communication Utility\\*")) OR ((EventID:"4688" AND CommandLine:"*\\\\chrome_frame_helper.exe") AND NOT (EventID:"4688" AND CommandLine:"*\\\\Google\\\\Chrome\\\\application\\*"))) OR ((EventID:"4688" AND CommandLine:"*\\\\dvcemumanager.exe") AND NOT (EventID:"4688" AND CommandLine:"*\\\\Microsoft Device Emulator\\*"))) OR ((EventID:"4688" AND CommandLine:"*\\\\Gadget.exe") AND NOT (EventID:"4688" AND CommandLine:"*\\\\Windows Media Player\\*"))) OR ((EventID:"4688" AND CommandLine:"*\\\\hcc.exe") AND NOT (EventID:"4688" AND CommandLine:"*\\\\HTML Help Workshop\\*"))) OR ((EventID:"4688" AND CommandLine:"*\\\\hkcmd.exe") AND NOT (EventID:"4688" AND CommandLine:("*\\\\System32\\*" "*\\\\SysNative\\*" "*\\\\SysWowo64\\*")))) OR ((EventID:"4688" AND CommandLine:"*\\\\Mc.exe") AND NOT (EventID:"4688" AND CommandLine:("*\\\\Microsoft Visual Studio*" "*\\\\Microsoft SDK*" "*\\\\Windows Kit*")))) OR ((EventID:"4688" AND CommandLine:"*\\\\MsMpEng.exe") AND NOT (EventID:"4688" AND CommandLine:("*\\\\Microsoft Security Client\\*" "*\\\\Windows Defender\\*" "*\\\\AntiMalware\\*")))) OR ((EventID:"4688" AND CommandLine:"*\\\\msseces.exe") AND NOT (EventID:"4688" AND CommandLine:"*\\\\Microsoft Security Center\\*"))) OR ((EventID:"4688" AND CommandLine:"*\\\\OInfoP11.exe") AND NOT (EventID:"4688" AND CommandLine:"*\\\\Common Files\\\\Microsoft Shared\\*"))) OR ((EventID:"4688" AND CommandLine:"*\\\\OleView.exe") AND NOT (EventID:"4688" AND CommandLine:("*\\\\Microsoft Visual Studio*" "*\\\\Microsoft SDK*" "*\\\\Windows Kit*" "*\\\\Windows Resource Kit\\*")))) OR ((EventID:"4688" AND CommandLine:"*\\\\OleView.exe") AND NOT (EventID:"4688" AND CommandLine:("*\\\\Microsoft Visual Studio*" "*\\\\Microsoft SDK*" "*\\\\Windows Kit*" "*\\\\Windows Resource Kit\\*" "*\\\\Microsoft.NET\\*"))))
```


### splunk
    
```
(((((((((((((EventID="4688" CommandLine="*\\\\CamMute.exe") NOT (EventID="4688" CommandLine="*\\\\Lenovo\\\\Communication Utility\\*")) OR ((EventID="4688" CommandLine="*\\\\chrome_frame_helper.exe") NOT (EventID="4688" CommandLine="*\\\\Google\\\\Chrome\\\\application\\*"))) OR ((EventID="4688" CommandLine="*\\\\dvcemumanager.exe") NOT (EventID="4688" CommandLine="*\\\\Microsoft Device Emulator\\*"))) OR ((EventID="4688" CommandLine="*\\\\Gadget.exe") NOT (EventID="4688" CommandLine="*\\\\Windows Media Player\\*"))) OR ((EventID="4688" CommandLine="*\\\\hcc.exe") NOT (EventID="4688" CommandLine="*\\\\HTML Help Workshop\\*"))) OR ((EventID="4688" CommandLine="*\\\\hkcmd.exe") NOT (EventID="4688" (CommandLine="*\\\\System32\\*" OR CommandLine="*\\\\SysNative\\*" OR CommandLine="*\\\\SysWowo64\\*")))) OR ((EventID="4688" CommandLine="*\\\\Mc.exe") NOT (EventID="4688" (CommandLine="*\\\\Microsoft Visual Studio*" OR CommandLine="*\\\\Microsoft SDK*" OR CommandLine="*\\\\Windows Kit*")))) OR ((EventID="4688" CommandLine="*\\\\MsMpEng.exe") NOT (EventID="4688" (CommandLine="*\\\\Microsoft Security Client\\*" OR CommandLine="*\\\\Windows Defender\\*" OR CommandLine="*\\\\AntiMalware\\*")))) OR ((EventID="4688" CommandLine="*\\\\msseces.exe") NOT (EventID="4688" CommandLine="*\\\\Microsoft Security Center\\*"))) OR ((EventID="4688" CommandLine="*\\\\OInfoP11.exe") NOT (EventID="4688" CommandLine="*\\\\Common Files\\\\Microsoft Shared\\*"))) OR ((EventID="4688" CommandLine="*\\\\OleView.exe") NOT (EventID="4688" (CommandLine="*\\\\Microsoft Visual Studio*" OR CommandLine="*\\\\Microsoft SDK*" OR CommandLine="*\\\\Windows Kit*" OR CommandLine="*\\\\Windows Resource Kit\\*")))) OR ((EventID="4688" CommandLine="*\\\\OleView.exe") NOT (EventID="4688" (CommandLine="*\\\\Microsoft Visual Studio*" OR CommandLine="*\\\\Microsoft SDK*" OR CommandLine="*\\\\Windows Kit*" OR CommandLine="*\\\\Windows Resource Kit\\*" OR CommandLine="*\\\\Microsoft.NET\\*"))))
```


### logpoint
    
```
(((((((((((((EventID="4688" CommandLine="*\\\\CamMute.exe")  -(EventID="4688" CommandLine="*\\\\Lenovo\\\\Communication Utility\\*")) OR ((EventID="4688" CommandLine="*\\\\chrome_frame_helper.exe")  -(EventID="4688" CommandLine="*\\\\Google\\\\Chrome\\\\application\\*"))) OR ((EventID="4688" CommandLine="*\\\\dvcemumanager.exe")  -(EventID="4688" CommandLine="*\\\\Microsoft Device Emulator\\*"))) OR ((EventID="4688" CommandLine="*\\\\Gadget.exe")  -(EventID="4688" CommandLine="*\\\\Windows Media Player\\*"))) OR ((EventID="4688" CommandLine="*\\\\hcc.exe")  -(EventID="4688" CommandLine="*\\\\HTML Help Workshop\\*"))) OR ((EventID="4688" CommandLine="*\\\\hkcmd.exe")  -(EventID="4688" CommandLine IN ["*\\\\System32\\*", "*\\\\SysNative\\*", "*\\\\SysWowo64\\*"]))) OR ((EventID="4688" CommandLine="*\\\\Mc.exe")  -(EventID="4688" CommandLine IN ["*\\\\Microsoft Visual Studio*", "*\\\\Microsoft SDK*", "*\\\\Windows Kit*"]))) OR ((EventID="4688" CommandLine="*\\\\MsMpEng.exe")  -(EventID="4688" CommandLine IN ["*\\\\Microsoft Security Client\\*", "*\\\\Windows Defender\\*", "*\\\\AntiMalware\\*"]))) OR ((EventID="4688" CommandLine="*\\\\msseces.exe")  -(EventID="4688" CommandLine="*\\\\Microsoft Security Center\\*"))) OR ((EventID="4688" CommandLine="*\\\\OInfoP11.exe")  -(EventID="4688" CommandLine="*\\\\Common Files\\\\Microsoft Shared\\*"))) OR ((EventID="4688" CommandLine="*\\\\OleView.exe")  -(EventID="4688" CommandLine IN ["*\\\\Microsoft Visual Studio*", "*\\\\Microsoft SDK*", "*\\\\Windows Kit*", "*\\\\Windows Resource Kit\\*"]))) OR ((EventID="4688" CommandLine="*\\\\OleView.exe")  -(EventID="4688" CommandLine IN ["*\\\\Microsoft Visual Studio*", "*\\\\Microsoft SDK*", "*\\\\Windows Kit*", "*\\\\Windows Resource Kit\\*", "*\\\\Microsoft.NET\\*"])))
```


### grep
    
```
grep -P '^(?:.*(?:.*(?:.*(?:.*(?:.*(?:.*(?:.*(?:.*(?:.*(?:.*(?:.*(?:.*(?:.*(?:.*(?:.*(?:.*(?:.*(?:.*(?:.*(?:.*(?:.*(?:.*(?:.*(?=.*(?:.*(?=.*4688)(?=.*.*\\CamMute\\.exe)))(?=.*(?!.*(?:.*(?=.*4688)(?=.*.*\\Lenovo\\Communication Utility\\.*)))))|.*(?:.*(?=.*(?:.*(?=.*4688)(?=.*.*\\chrome_frame_helper\\.exe)))(?=.*(?!.*(?:.*(?=.*4688)(?=.*.*\\Google\\Chrome\\application\\.*)))))))|.*(?:.*(?=.*(?:.*(?=.*4688)(?=.*.*\\dvcemumanager\\.exe)))(?=.*(?!.*(?:.*(?=.*4688)(?=.*.*\\Microsoft Device Emulator\\.*)))))))|.*(?:.*(?=.*(?:.*(?=.*4688)(?=.*.*\\Gadget\\.exe)))(?=.*(?!.*(?:.*(?=.*4688)(?=.*.*\\Windows Media Player\\.*)))))))|.*(?:.*(?=.*(?:.*(?=.*4688)(?=.*.*\\hcc\\.exe)))(?=.*(?!.*(?:.*(?=.*4688)(?=.*.*\\HTML Help Workshop\\.*)))))))|.*(?:.*(?=.*(?:.*(?=.*4688)(?=.*.*\\hkcmd\\.exe)))(?=.*(?!.*(?:.*(?=.*4688)(?=.*(?:.*.*\\System32\\.*|.*.*\\SysNative\\.*|.*.*\\SysWowo64\\.*))))))))|.*(?:.*(?=.*(?:.*(?=.*4688)(?=.*.*\\Mc\\.exe)))(?=.*(?!.*(?:.*(?=.*4688)(?=.*(?:.*.*\\Microsoft Visual Studio.*|.*.*\\Microsoft SDK.*|.*.*\\Windows Kit.*))))))))|.*(?:.*(?=.*(?:.*(?=.*4688)(?=.*.*\\MsMpEng\\.exe)))(?=.*(?!.*(?:.*(?=.*4688)(?=.*(?:.*.*\\Microsoft Security Client\\.*|.*.*\\Windows Defender\\.*|.*.*\\AntiMalware\\.*))))))))|.*(?:.*(?=.*(?:.*(?=.*4688)(?=.*.*\\msseces\\.exe)))(?=.*(?!.*(?:.*(?=.*4688)(?=.*.*\\Microsoft Security Center\\.*)))))))|.*(?:.*(?=.*(?:.*(?=.*4688)(?=.*.*\\OInfoP11\\.exe)))(?=.*(?!.*(?:.*(?=.*4688)(?=.*.*\\Common Files\\Microsoft Shared\\.*)))))))|.*(?:.*(?=.*(?:.*(?=.*4688)(?=.*.*\\OleView\\.exe)))(?=.*(?!.*(?:.*(?=.*4688)(?=.*(?:.*.*\\Microsoft Visual Studio.*|.*.*\\Microsoft SDK.*|.*.*\\Windows Kit.*|.*.*\\Windows Resource Kit\\.*))))))))|.*(?:.*(?=.*(?:.*(?=.*4688)(?=.*.*\\OleView\\.exe)))(?=.*(?!.*(?:.*(?=.*4688)(?=.*(?:.*.*\\Microsoft Visual Studio.*|.*.*\\Microsoft SDK.*|.*.*\\Windows Kit.*|.*.*\\Windows Resource Kit\\.*|.*.*\\Microsoft\\.NET\\.*))))))))'
```


