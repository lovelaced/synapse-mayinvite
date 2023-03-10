# Matrix-Synapse Shielded User Invites Module

This module is a matrix-synapse server module that blocks certain users from receiving invites from users on other homeservers. This is useful if you have a specific list of users that should not receive invites from users on other homeservers, for example if you want to protect the privacy of these users.

## Usage

To use this module, follow these steps:

1. Add the module to your matrix-synapse configuration file. To configure the module, specify a list of shielded users in the "shielded_users" field. Each shielded user should be identified by a unique identifier and defined by their Matrix ID and email address. The Matrix ID is used to identify the user in Matrix, and the email address is used to provide a way for users to contact the shielded user if they need to.

```yaml
# In the "modules" section
- module: "matrix_synapse_shielded_user_invites_module.SynapseMayInvite"
  config:
    shielded_users:
      user1:
        - mxid: "@test:matrix.org"
        - email: "test@gmail.com"
      user2:
        - mxid: "@test2:matrix.org"
        - email:  "test2@gmail.com"
```


2. Restart matrix-synapse to apply the changes.

That's it! The module should now be active and blocking certain users from receiving invites from users on other homeservers.

You may also want to add the following to your logging configuration to debug the module:

```yaml
loggers:
  matrix_synapse_shielded_user_invites_module:
    level: INFO
```
