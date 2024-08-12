import subprocess
import sys


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
