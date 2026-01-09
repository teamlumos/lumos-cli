---
title: Authentication
slug: cli-authentication
category:
  uri: TOOLS
content:
  excerpt: Authenticating the Lumos CLI
parent:
  uri: cli
---

# Authentication

After installation, authenticate with your Lumos account:

```bash
# Setup authentication (first time)
lumos setup

# Or login directly via OAuth
lumos login
```

You'll be directed to authenticate in your browser. Once complete, you can verify your login:

```bash
lumos whoami
```

You must use `lumos login` and complete one of the authentication mechanisms before using the CLI. API Tokens last indefinitely. OAuth 2.0 tokens last for 12 hours.

## Authentication issues

If you have trouble logging in:

```bash
# Clear existing credentials
lumos logout

# Re-run setup
lumos setup
```
