# SSH Brute-Force Detection

## Objective

Detect repeated failed SSH authentication attempts that may indicate a brute-force attack.

## Data Source

Linux SSH authentication logs collected through systemd journal.

## Detection Logic

The detection counts failed SSH authentication attempts by source IP address.

An alert is generated when the same source IP produces three or more failed authentication attempts.

## Test

Three intentional failed SSH authentication attempts were generated against the Ubuntu lab server.

The detection successfully identified the repeated attempts from the source IP.

## Security Relevance

Repeated authentication failures may indicate:

- Brute-force attacks
- Password spraying
- Credential guessing
- Unauthorized access attempts

## Limitations

A threshold-based detection can generate false positives. Multiple failed attempts may occur because of:

- Forgotten passwords
- Misconfigured applications
- Legitimate administrative activity
- Automated systems using outdated credentials
