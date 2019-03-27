| Title          | RA_0007_containment_block_ip_on_border_firewall                                                                                                      |
|:---------------|:-----------------------------------------------------------------------------------------------------------------|
| Stage    | containment                                                            |
| Automation | None |
| Author    | Daniil Yugoslavskiy                                                          |
| Creation Date    | 31.01.2019                                            |
| References     | None                                  |
| Description    | Block ip address on border firewall.                                                               |
| Linked Response Actions | None |
| Linked Analytics |<ul><li>MS_firewall</li></ul> |


### Workflow

Block ip address on border firewall using native filtering functionality.
Warning: 
- If not all corporate hosts access internet through the border firewall, this Response Action cannot guarantee containment of threat.
- Be careful blocking IP address. Make sure it's not cloud provider or hoster. In this case you have to use blocking by URL something more specific.
