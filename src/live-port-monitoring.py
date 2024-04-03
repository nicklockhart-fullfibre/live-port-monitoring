import requests
import datetime
import sys

from configparser import ConfigParser

config = ConfigParser()

try:
    with open("config.ini") as config_file:
        config.read_file(config_file)
except Exception as e:
    print(f"Couldn't load the config file. ({e})")
    print("Make sure config.ini is in the current working directory.")
    input("Press Enter to exit.")
    sys.exit(1)

LNMS_HOST = config['LibreNMS']['Host']
LNMS_API_KEY = config['LibreNMS']['ApiKey']

if config.getboolean("Result", "PrependTimestamp"):
    NOW = datetime.datetime.now()
    TIMESTAMP = NOW.strftime("%Y-%m-%d %H.%M.%S")
    REPORT_FILENAME = f"{TIMESTAMP} {config['Result']['FileName']}"    
else:
    REPORT_FILENAME = config['Result']['FileName']

print(f"Using LibreNMS host at {LNMS_HOST}.")
print(f"The report will be saved to {REPORT_FILENAME}.")

SESSION = requests.Session()
SESSION.headers = {"X-Auth-Token": LNMS_API_KEY}
LNMS_API_ROOT = f"{LNMS_HOST}/api/v0"

CLEAR_LINE = "\33[2K\r"

print(f"{CLEAR_LINE}getting port info...", end="")

# get port info
port_info = SESSION.get(
    url=f"{LNMS_API_ROOT}/ports",
    params={
        "columns": "ifName,ifAlias,device_id,ignore,ifOperStatus,ifAdminStatus"
    }
).json()

ignored_ports = [
    port for port in port_info['ports']
    if port['ignore'] == 1
    and port['ifOperStatus'] == 'up'
    and port['ifAdminStatus'] == 'up'
]

ignored_device_ids = list(set(
    port['device_id'] for port in ignored_ports
))

device_table = {}

for device_id in ignored_device_ids:
    print(f"{CLEAR_LINE}Getting info for device {device_id}...", end="")
    device_info_raw = SESSION.get(
        url=f"{LNMS_API_ROOT}/devices/{device_id}"
    ).json()
    if "devices" in device_info_raw:
        device_info = device_info_raw['devices'][0]
        device_table[device_id] = device_info

with open(REPORT_FILENAME, mode="w", encoding="utf-8") as report_file:
    report_file.write("The following ports are ignored but up:\n\n")

    for device_id, device in device_table.items():
        hostname = device['hostname']
        sysname = device['sysName']
        report_file.write(f"'{sysname}' ({hostname}):\n")

        ignored_ports_on_device = [
            port for port in ignored_ports
            if port['device_id'] == device_id
        ]
        for port in ignored_ports_on_device:
            port_name = port['ifName']
            port_alias = port['ifAlias']
            oper_status = port['ifOperStatus']
            admin_status = port['ifAdminStatus']

            report_file.write(f"    '{port_alias}' ({port_name})\n")

        report_file.write('\n')

print(f"{CLEAR_LINE}Done.")
