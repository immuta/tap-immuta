# tap-immuta

`tap-immuta` is a Singer tap for Immuta.

This package is being made available by Immuta's internal analytics
team and is NOT officially supported by Immuta. Users are welcome to open issues
or pull requests to improve the tap.

Built with the [Singer SDK](https://gitlab.com/meltano/singer-sdk).

## Installation

This tap is avaiable on PyPi and can be installed using:

```bash
pip install tap-immuta
```

## Configuration

The following configuration options are available:

- `api_key` (required): User-generated Immuta API Key
- `immuta_host` (required): Immuta hostname, e.g. `https://my-immuta.my-domain.com`
- `start_date` (optional): should be used on first sync to indicate how far back to grab records. Start dates should conform to the RFC3339 specification.
- `user_agent` (optional): should be set to something that includes a contact email address should the API provider need to contact you for any reason.

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-immuta --about
```

## Usage

You can easily run `tap-immuta` by itself or in a pipeline using [Meltano](www.meltano.com).

### Executing the Tap Directly

```bash
tap-immuta --version
tap-immuta --help
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

### Singer SDK Dev Guide

See the [dev guide](../../docs/dev_guide.md) for more instructions on how to use the Singer SDK to develop your own taps and targets.
