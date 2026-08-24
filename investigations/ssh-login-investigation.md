# SSH Login Investigation

## Alert

A successful SSH login occurred after multiple failed authentication attempts from the same source IP within a five-minute period.

## Investigation Summary

The detection identified multiple failed SSH authentication attempts followed by a successful login.

The activity involved a test account and originated from the same source IP.

## Timeline

| Event                     | Details                                              |
| ------------------------- | ---------------------------------------------------- |
| Failed authentication     | Multiple failed SSH attempts from the same source IP |
| Successful authentication | `testuser`                                           |
| Authentication method     | Password                                             |
| Session activity          | User session established                             |
| Post-login activity       | Commands executed                                    |

## Evidence Sources

* `journalctl` SSH authentication logs
* `who` for active sessions
* Bash command history

## Assessment

The sequence is suspicious because multiple failed authentication attempts were followed by a successful login from the same source IP.

This behavior can be consistent with credential guessing followed by successful authentication.

However, the activity alone does not prove account compromise.

## Recommended Analyst Actions

1. Validate whether the account owner expected the login.
2. Confirm whether the source IP belongs to an authorized device.
3. Review additional activity performed after authentication.
4. Check for other suspicious authentication activity.
5. If the login is unauthorized, consider terminating the session and resetting the account credentials.

## Privacy Note

Real usernames, IP addresses, hostnames, credentials, tokens, and other identifying information have been removed or replaced with placeholders before committing investigation data.
