# Suspicious Process Detection

## Objective

Detect a netcat process running on the Linux system.

## Detection Logic

The detection checks running processes and generates an alert when it finds a process containing `nc`.

## Test

A netcat process was intentionally started on the Ubuntu lab system.

The detection successfully identified the process and generated an alert.

The test process was then stopped.

## Security Relevance

Netcat can be used for legitimate network troubleshooting, but attackers can also use it for network connections or command execution.

Therefore, a detected netcat process should be investigated rather than automatically treated as malicious.

## Limitations

The detection only looks for the `nc` process name.

A more advanced detection would examine additional information such as:

- User
- Parent process
- Command arguments
- Network connections
