import subprocess
import re
from collections import Counter


def get_failed_ssh_logins():
    result = subprocess.run(
        [
            "sudo",
            "journalctl",
            "-u",
            "ssh",
            "--since",
            "5 minutes ago",
            "--no-pager"
        ],
        capture_output=True,
        text=True
    )

    return result.stdout


def extract_failed_logins(log_data):
    pattern = (
        r"Failed password for "
        r"(?:invalid user )?(\S+)"
        r" from "
        r"([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)"
    )

    return re.findall(pattern, log_data)


def main():
    logs = get_failed_ssh_logins()

    failed_logins = extract_failed_logins(logs)

    ip_counts = Counter(
        source_ip
        for _, source_ip in failed_logins
    )

    print(
        f"Failed SSH attempts in the last 5 minutes: "
        f"{len(failed_logins)}"
    )

    for source_ip, count in ip_counts.items():

        if count >= 3:
            print(
                f"ALERT: {count} failed SSH attempts "
                f"from {source_ip} within 5 minutes"
            )


if __name__ == "__main__":
    main()
