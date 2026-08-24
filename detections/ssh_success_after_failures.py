import subprocess
import re
from collections import defaultdict
from datetime import datetime, timedelta


def get_ssh_logs():
    result = subprocess.run(
        [
            "sudo",
            "journalctl",
            "-u",
            "ssh",
            "--since",
            "30 minutes ago",
            "--no-pager",
            "-o",
            "short-iso"
        ],
        capture_output=True,
        text=True
    )

    return result.stdout


def extract_events(log_data):
    failed_pattern = (
        r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2})"
        r".*?Failed password for "
        r"(?:invalid user )?(\S+)"
        r" from "
        r"([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)"
    )

    successful_pattern = (
        r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2})"
        r".*?Accepted (?:password|publickey) for "
        r"(\S+)"
        r" from "
        r"([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)"
    )

    failed = [
        ("failed", timestamp, username, source_ip)
        for timestamp, username, source_ip
        in re.findall(failed_pattern, log_data)
    ]

    successful = [
        ("success", timestamp, username, source_ip)
        for timestamp, username, source_ip
        in re.findall(successful_pattern, log_data)
    ]

    return failed + successful


def main():
    logs = get_ssh_logs()
    events = extract_events(logs)

    failed_by_ip = defaultdict(list)
    successful_logins = []

    for event_type, timestamp, username, source_ip in events:
        event_time = datetime.fromisoformat(timestamp)

        if event_type == "failed":
            failed_by_ip[source_ip].append(
                (event_time, username)
            )
        else:
            successful_logins.append(
                (event_time, username, source_ip)
            )

    for success_time, username, source_ip in successful_logins:

        window_start = success_time - timedelta(minutes=5)

        recent_failures = [
            failure
            for failure in failed_by_ip[source_ip]
            if window_start <= failure[0] < success_time
        ]

        if len(recent_failures) >= 3:
            print(
                f"ALERT: Successful SSH login from {source_ip} "
                f"after {len(recent_failures)} failed attempts "
                f"within 5 minutes"
            )

            print(
                f"Successful username: {username}"
            )


if __name__ == "__main__":
    main()
