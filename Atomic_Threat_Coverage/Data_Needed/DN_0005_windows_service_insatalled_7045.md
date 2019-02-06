| Title          | DN_0005_windows_service_insatalled_7045                                                                                                      |
|:---------------|:-----------------------------------------------------------------------------------------------------------------|
| Description    | A service was installed in the system.
                                                                                                |
| Logging Policy | <ul><li>[None](../Logging_Policies/None.md)</li></ul> |
| References     | <ul><li>[None](None)</li></ul>                                  |
| Platform       | Windows    																																															  |
| Type           | Windows Log        																																															  |
| Channel        | System     																																															  |
| Provider       | Service Control Manager    																																															  |
| Fields         | <ul><li>EventID</li><li>ProcessID</li><li>ThreadID</li><li>ServiceName</li><li>ImagePath</li><li>ServiceFileName</li><li>ServiceType</li><li>StartType</li><li>AccountName</li><li>UserSid</li><li>Computer</li></ul>                                               |


## Log Samples

### Raw Log

```
- <Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">
  - <System>
    <Provider Name="Service Control Manager" Guid="{555908d1-a6d7-4695-8e1e-26931d2012f4}" EventSourceName="Service Control Manager" /> 
    <EventID Qualifiers="16384">7045</EventID> 
    <Version>0</Version> 
    <Level>4</Level> 
    <Task>0</Task> 
    <Opcode>0</Opcode> 
    <Keywords>0x8080000000000000</Keywords> 
    <TimeCreated SystemTime="2017-07-02T15:48:56.256752900Z" /> 
    <EventRecordID>762</EventRecordID> 
    <Correlation /> 
    <Execution ProcessID="568" ThreadID="1792" /> 
    <Channel>System</Channel> 
    <Computer>DESKTOP</Computer> 
    <Security UserID="S-1-5-21-2073602604-586167410-2329295167-1001" /> 
    </System>
  - <EventData>
    <Data Name="ServiceName">sshd</Data> 
    <Data Name="ImagePath">C:\Program Files\OpenSSH\sshd.exe</Data> 
    <Data Name="ServiceType">user mode service</Data> 
    <Data Name="StartType">demand start</Data> 
    <Data Name="AccountName">LocalSystem</Data> 
  </EventData>
</Event>

```




