# SSH Successful Login After Failed Attempts

## Objective

Detect a successful SSH authentication that occurs shortly after multiple failed authentication attempts from the same source IP.

## Data Source

Linux SSH authentication logs collected through systemd journal.

## Detection Logic

The detection examines SSH authentication events from the previous 30 minutes.

For each successful SSH login, the detection looks back five minutes for failed authentication attempts from the same source IP.

An alert is generated when a successful login occurs after three or more failed attempts within five minutes.

## Test

Three intentional failed SSH authentication attempts were generated against the Ubuntu lab server, followed by a successful SSH login.

The detection successfully identified the sequence and generated an alert.

## Security Relevance

This activity may indicate:

- Brute-force credential guessing followed by successful access
- Compromised credentials
- Unauthorized account access
- Password spraying followed by successful authentication

## Limitations

This detection does not prove that an account was compromised.

Legitimate users can make several failed login attempts before successfully authenticating.

Additional investigation should consider:

- Source IP reputation
- Username
- Login time
- User's expected location
- Previous authentication activity
- Other activity after the successful login
