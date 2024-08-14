#  /*******************************************************************************
#   *
#   *  * Copyright (c)  2024.
#   *  * All Credits Goes to MrAlishr
#   *  * Email : Alishariatirad@gmail.com
#   *  * Github: github.com/MrAlishr
#   *  * Telegram : Alishrr
#   *  *
#   *
#   ******************************************************************************/

import re
import subprocess
import sys
import threading


def run_command(cmd):
    # Hide the window on Windows OS
    creationflags = 0
    if sys.platform.startswith('win'):
        creationflags = subprocess.CREATE_NO_WINDOW

    try:
        result = subprocess.run(['powershell', '-Command', cmd], capture_output=True, text=True,
                                creationflags=creationflags)
        return result.stdout.strip()
    except Exception as e:
        return str(e)


def get_active_adapter():
    cmd = "Get-NetAdapter | Where-Object { $_.Status -eq 'Up' } | Select-Object -ExpandProperty InterfaceAlias"
    return run_command(cmd)


def set_dns(adapter, primary, secondary):
    cmd = f"Set-DnsClientServerAddress -InterfaceAlias '{adapter}' -ServerAddresses ('{primary}', '{secondary}')"
    return run_command(cmd)


def unset_dns(adapter):
    cmd = f"Set-DnsClientServerAddress -InterfaceAlias '{adapter}' -ResetServerAddresses"
    return run_command(cmd)


def async_ping_dns(server, callback, count=4):
    """ Ping a DNS server asynchronously and return the average latency via a callback. """

    def run_ping():
        try:
            creationflags = 0
            if sys.platform.startswith('win'):
                creationflags = subprocess.CREATE_NO_WINDOW

            command = f'ping -n {count} {server}'
            output = subprocess.run(command, capture_output=True, text=True, shell=True,
                                    creationflags=creationflags).stdout

            match = re.search(r'Average = (\d+)ms', output)
            if match:
                latency = f"{match.group(1)} ms"
            else:
                latency = "No response"
        except subprocess.SubprocessError:
            latency = "Failed to ping"

        callback(latency)

    # Start the ping in a separate thread
    thread = threading.Thread(target=run_ping)
    thread.start()
