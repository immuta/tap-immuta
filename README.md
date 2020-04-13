# tap-immuta

**Author**: Stephen Bailey (sbailey@immuta.com)

This is a [Singer](http://singer.io) tap that produces JSON-formatted data following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md). It can generate a catalog of available data in Immuta Accounts and extract the following resources:

- Data Source - [API](https://instance.immuta.com/api/dataSource)
- Project - [API](https://instance.immuta.com/api/project)
- Built-in Groups - [API](https://instance.immuta.com/api/bim/group)
- Built-in Users - [API](https://instance.immuta.com/api/bim/user)
- Purpose - [API](https://instance.immuta.com/api/governance/purpose)-resource

## Quick Start

1. Install

```bash
git clone git@github.com:immuta/tap-immuta.git
cd tap-immuta
pip install .
```

1. Get an [API key](https://immuta.me/developers-api) from immuta

1. Create the config file. There is a template you can use at `config.json.example`, just copy it to `config.json` in the repo root and insert your token

1. Run the application to generate a catalog.

```bash
tap-immuta -c config.json --discover > catalog.json
```

1. Select the tables you'd like to replicate. Step 4 generates a a file called `catalog.json` that specifies all the available endpoints and fields. You'll need to open the file and select the ones you'd like to replicate. See the [Singer guide on Catalog Format](https://github.com/singer-io/getting-started/blob/c3de2a10e10164689ddd6f24fee7289184682c1f/BEST_PRACTICES.md#catalog-format) for more information on how tables are selected.

1. Run it!

```bash
tap-immuta -c config.json --catalog catalog.json
```

## Configuration

The following configuration options are available:

- `api-key` (required): Immuta Accounts API token
- `start-date` (optional): should be used on first sync to indicate how far back to grab records. Start dates should conform to the RFC3339 specification.
- `user-agent` (optional): should be set to something that includes a contact email address should the API provider need to contact you for any reason.

---

Copyright &copy; 2019 Immuta
