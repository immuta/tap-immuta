# tap-immuta

`tap-immuta` is a Singer tap for Immuta.

This package is being made available by Immuta's internal analytics
team and is NOT officially supported by Immuta. Users are welcome to open issues
or pull requests to improve the tap.

Built with the [Singer SDK](https://gitlab.com/meltano/singer-sdk).

## Installation

This tap can be installed using:

```bash
git clone https://github.com/immuta/tap-immuta.git
pip install tap-immuta
```

## Configuration

The following configuration options are available:

- `api_key` (required): User-generated Immuta API Key
- `hostname` (required): Immuta hostname, e.g. `https://my-immuta.my-domain.com`
- `user_agent` (optional): should be set to something that includes a contact email address should the API provider need to contact you for any reason.

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-immuta --about
```

## Usage

You can easily run `tap-immuta` by itself or in a pipeline using, for example, [Meltano](www.meltano.com).

### Executing the Tap Directly

To execute the tap directly, specify the config file, output the catalog, and then run it in sync mode.

```bash
tap-immuta --config CONFIG --discover > ./catalog.json
tap-immuta --config CONFIG --catalog ./catalog.json
```

### Create and Run Tests

Create tests within the `tap_immuta/tests` subfolder and
  then run:

```bash
pip install pytest
pytest tap_immuta/tests
```
