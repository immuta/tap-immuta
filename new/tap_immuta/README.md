# tap-immuta

`tap-immuta` is a Singer tap for Immuta.

Build with the [Singer SDK](https://gitlab.com/meltano/singer-sdk).

## Installation

- [ ] `Developer TODO:` Update the below as needed to correctly describe the install procedure. For instance, if you do not have a PyPi repo, or if you want users to directly install from your git repo, you can modify this step as appropriate.

```bash
pipx install tap-immuta
```

## Configuration

### Accepted Config Options

- [ ] `Developer TODO:` Provide a list of config options accepted by the tap.

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-immuta --about
```

### Source Authentication and Authorization

- [ ] `Developer TODO:` If your tap requires special access on the source system, or any special authentication requirements, provide those here.

## Usage

You can easily run `tap-immuta` by itself or in a pipeline using [Meltano](www.meltano.com).

### Executing the Tap Directly

```bash
tap-immuta --version
tap-immuta --help
tap-immuta --config CONFIG --discover > ./catalog.json
```

## Developer Resources

- [ ] `Developer TODO:` As a first step, scan the entire project for the text "`TODO:`" and complete any recommended steps, deleting the "TODO" references once completed.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_immuta/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-immuta` CLI interface directly using `poetry run`:

```bash
poetry run tap-immuta --help
```

### Testing with [Meltano](meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-immuta
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-immuta --version
# OR run a test `elt` pipeline:
meltano etl tap-immuta target-jsonl
```

### Singer SDK Dev Guide

See the [dev guide](../../docs/dev_guide.md) for more instructions on how to use the Singer SDK to develop your own taps and targets.
