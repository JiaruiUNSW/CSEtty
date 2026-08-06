# Security policy

The supported release line is the latest `0.1.0a1` alpha. This local simulator is
not an authentication, invigilation, or official submission system; the threat
model and explicit exclusions are documented in `README.md`.

For a suspected vulnerability that could expose host files or credentials,
escape a judge/container boundary, forge accepted submissions, or bypass an
exam deadline, use GitHub's private vulnerability-reporting or Security
Advisory interface for this repository. Do not include exploit details or real
credentials in a public issue. Ordinary bugs that do not disclose sensitive
information may use the public issue tracker.

The project never needs a real UNSW password or a PyPI token at runtime. If one
is accidentally disclosed, revoke it with its issuer immediately; deleting it
from a later commit or message is not sufficient.
