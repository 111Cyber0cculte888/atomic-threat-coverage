| Title          | DN_0007_windows_sysmon_sysmon_service_state_changed_4                                                                                                      |
|:---------------|:-----------------------------------------------------------------------------------------------------------------|
| Description    | Sysmon service changed status
                                                                                                |
| Logging Policy | <ul><li>[None](../Logging_Policies/None.md)</li></ul> |
| References     | <ul><li>[https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx?eventid=90004](https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx?eventid=90004)</li><li>[https://github.com/Cyb3rWard0g/OSSEM/blob/master/data_dictionaries/windows/sysmon/event-4.md](https://github.com/Cyb3rWard0g/OSSEM/blob/master/data_dictionaries/windows/sysmon/event-4.md)</li></ul>                                  |
| Platform       | Windows    																																															  |
| Type           | Windows Log        																																															  |
| Channel        | Microsoft-Windows-Sysmon/Operational     																																															  |
| Provider       | Microsoft-Windows-Sysmon    																																															  |
| Fields         | <ul><li>EventID</li><li>Computer</li><li>UtcTime</li><li>State</li></ul>                                               |


## Log Samples

### Raw Log

```
- <Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">
- <System>
      <Provider Name="Microsoft-Windows-Sysmon" Guid="{5770385F-C22A-43E0-BF4C-06F5698FFBD9}" />
      <EventID>4</EventID>
      <Version>3</Version>
      <Level>4</Level>
      <Task>4</Task>
      <Opcode>0</Opcode>
      <Keywords>0x8000000000000000</Keywords>
      <TimeCreated SystemTime="2017-04-28T22:52:20.883759300Z" />
      <EventRecordID>16761</EventRecordID>
      <Correlation />
      <Execution ProcessID="3216" ThreadID="3220" />
      <Channel>Microsoft-Windows-Sysmon/Operational</Channel>
      <Computer>rfsH.lab.local</Computer>
      <Security UserID="S-1-5-18" />
  </System>
- <EventData>
      <Data Name="UtcTime">2017-04-28 22:52:20.883</Data>
      <Data Name="State">Stopped</Data>
      <Data Name="Version">6.01</Data>
      <Data Name="SchemaVersion">3.30</Data>
  </EventData>
  </Event>

```




