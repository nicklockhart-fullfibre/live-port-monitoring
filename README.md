# Live Port Monitoring
This script generates a report of all ports that are operationally "up" but are ignored by LibreNMS,
in order to catch ports that are being ignored that should not be ignored.

## Usage
1. Get a local copy of the script. Either fetch the Windows executable from Releases, or clone the repository.
    - If you're using the raw Python script, make sure to install the requirements in `requirements.txt`.
2. Copy `config.example.ini` to `config.ini` in the same folder as the script or executable. Modify the configuration file to use your LibreNMS host URL and API key.
3. Run the script. By default, the report will be saved to `YYYY-MM-DD HH.MM.SS ignored_ports.txt`, but this can be changed in `config.ini`.

## Example output

```
The following ports are ignored but up:

'lorem' (172.16.0.1):
    'ipsum' (1/1/p65/eth)
    'dolor' (1/1/p65/fp-1)

'sit' (172.16.0.2):
    'amet' (amet)
    'consectetur' (consectetur)

'adipiscing' (172.16.0.3):
    'elit' (elit)

[...]
```

The output is separated by host, with ports on any given host indented by four spaces.
The host is identified by `sysName` and `hostname`, while ports are identified by `ifAlias` and `ifName`.