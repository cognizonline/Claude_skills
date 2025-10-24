# Compliance Pattern Catalog

| Pattern | Description | Default Action |
|---------|-------------|----------------|
| `email` | Detects email addresses. | Confirm business need; redact if unnecessary. |
| `ssn` | U.S. Social Security Number format `###-##-####`. | Remove immediately and notify security. |
| `credit_card` | 13-16 digit sequences that resemble payment cards. | Remove and validate PCI compliance requirements. |
| `secret` | Keywords such as `api_key`, `token`, `secret`, or `password`. | Rotate credentials, remove from memory, update secure store references. |
| `pii_terms` | Keywords referencing regulated personal data (passport, driver license). | Confirm lawful basis, redact if not required. |

Update this catalog when new patterns are introduced or when policies evolve.

