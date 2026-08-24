import subprocess
import re
from collections import Counter

def get_failed_ssh_logins():
    result = subprocess.run(
        ["sudo", "journalctl", "-u", "ssh", "--no-pager"],
        capture_output=True,
        text=True
    )

    return result.stdout


def extract_failed_logins(log_data):
    pattern = r"Failed password for (?:invalid user )?(\S+) from ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)"

    return re.findall(pattern, log_data)


def main():
    logs = get_failed_ssh_logins()
    failed_logins = extract_failed_logins(logs)

    ip_counts = Counter(source_ip for _, source_ip in failed_logins)

    print(f"Total failed SSH attempts: {len(failed_logins)}")

    for source_ip, count in ip_counts.items():
        if count >= 3:
            print(
                f"ALERT: {count} failed SSH authentication attempts "
                f"from {source_ip}"
            )


if __name__ == "__main__":
    main()
