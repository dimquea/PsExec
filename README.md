# PsExec integrations
Home Assistant integrations that allow you to run command on remote Windows PC, for example hibernate, that can't do **net rpc**.

## Main info
Component create and run service on remote PC, that execute command. On end of execution service will delete.
More info [here](https://pypi.org/project/pypsexec/).

## Config
The user must be an administarator.
If on remote PC turned on UAC, you need to do one change in registry.
Find key:
```
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System
```
change value of **LocalAccountTokenFilterPolicy** to **dword:00000001**

`configuration.yaml`:

    psexec:

`scripts.yaml` template:

```yaml
script:
  name_of_your_script:
    sequence:
      - service: psexec.exec
        data:
          encrypt: false
          host: 192.168.1.10 # ip of your PC
          username: user # user name
          password: password # password for user
          command: cmd.exe /c echo Hello World > c:\out.txt # this command create out.txt on root of C:\
```

## Example scenario
You can wake and hibernate your PC remotely. You will this and [Wake on Lan](https://www.home-assistant.io/integrations/wake_on_lan/) integration.
In `scripts.yaml` add :

```yaml
script:
  desktop_remote_hibernate:
    sequence:
      - service: psexec.exec
        data:
          encrypt: false
          host: 192.168.1.10 # ip of your PC
          username: user # user name
          password: password # password for user
          command: cmd.exe /c start /b shutdown.exe /h # this command will hibernate PC
```
```yaml
switch:
  - platform: wake_on_lan
    name: Switch name
    mac: AB:CD:EF:GH:IK:LM
    host: 192.168.1.10
    turn_off:
      - service: script.desktop_remote_hibernate
```
This switch will be wake your PC on toggle ON and hibernate on toggle OFF.

## Installation
Manually copy `psexec` folder from [latest release](https://github.com/dimquea/PsExec/releases/latest) to `custom_components` folder in your config folder.

## Credits
Original posted by AlexxIT ([source](https://sprut.ai/client/blog/1724)).
I'm just create repository.
