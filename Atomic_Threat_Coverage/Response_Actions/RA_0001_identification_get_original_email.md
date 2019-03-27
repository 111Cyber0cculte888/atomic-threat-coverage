| Title          | RA_0001_identification_get_original_email                                                                                                      |
|:---------------|:-----------------------------------------------------------------------------------------------------------------|
| Stage    | identification                                                            |
| Automation | None |
| Author    | Daniil Yugoslavskiy                                                          |
| Creation Date    | 31.01.2019                                            |
| References     |<ul><li>[https://www.lifewire.com/save-an-email-as-an-eml-file-in-gmail-1171956](https://www.lifewire.com/save-an-email-as-an-eml-file-in-gmail-1171956)</li><li>[https://eml.tooutlook.com/](https://eml.tooutlook.com/)</li></ul>                                  |
| Description    | Obtain original phishing email                                                               |
| Linked Response Actions | None |
| Linked Analytics | None |


### Workflow

Obtain original phishing email from on of the available/fastest options:

- Email Team/Email server: if there is such option
- Person who reported the attack (if it wasn't detected automatically or reported by victims)
- Victims: if they were reporting the attack

Ask for email in `.EML` format. Instructions: 

  1. Drug and drop email from Email client to Desktop
  2. Send to IR specialists by <email>
