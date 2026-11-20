# Camera API Keys

We generate Unifi API Keys per-console, to help limit the amount of data any one group or service accesses. This helps manage security risk across the services.

## Generating A New Key

Keys are set to expire regularly. Although keys can be generated that never expire *we do not create keys without expiration dates*. To create a new key you can follow the [Unifi Developer Instructions](https://developer.ui.com/network/v10.4.57/gettingstarted). Otherwise:

* Connect to the Unifi Site Manager
* Go to settings for the whole network
* "Add an API Key"

This should only be available to the Network Admin or Owner. End users should not be able to create or remove API keys.

