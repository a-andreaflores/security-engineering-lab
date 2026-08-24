import subprocess
import re

def get_failed_ssh_logins():
    result = subprocess.run(
        ["sudo", "journalctl", "-u", "ssh", "--no-pager"],
        capture_output=True,
        text=True
    )

    return result.stdout

def extract_failed_logins(log_data):
    pattern = r"Failed password for (?:invalid user )?(\S+) from ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)"

    matches = re.findall(pattern, log_data)

    return matches

def main():
    logs = get_failed_ssh_logins()
    failed_logins = extract_failed_logins(logs)

    print(f"Failed SSH authentication attempts: {len(failed_logins)}")

    for username, source_ip in failed_logins:
        print(f"Username: {username} | Source IP: {source_ip}")

if __name__ == "__main__":
    main()
