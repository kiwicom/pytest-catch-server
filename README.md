# Pytest Catch Server

[![PyPI version](https://img.shields.io/pypi/v/pytest-catch-server.svg)](https://pypi.org/project/pytest-catch-server)
[![Python versions](https://img.shields.io/pypi/pyversions/pytest-catch-server.svg)](https://pypi.org/project/pytest-catch-server)
[![Build status](https://travis-ci.org/kiwicom/pytest-catch-server.svg?branch=master)](https://travis-ci.org/kiwicom/pytest-catch-server)
[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

[Pytest](http://pytest.org) plugin with server fixture for catching HTTP requests.
It's handy for integration tests or for testing 3rd party packages which have
network side effects like reporting to 3rd party services (DataDog APM, Sentry, ...).

## Installation

You can install "pytest-catch-server" via `pip`:

```
pip install pytest-catch-server
```

## Usage

This plugin comes with three fixtures. The main `catch_server` is for use in your tests:

```python
def test_something(catch_server):
    url = f"http://{catch_server.host}:{catch_server.port}/something"
    requests.get(url)
    assert catch_server.requests == [
        {"method": "GET", "path": "/something", "data": b""}
    ]
```

In more real world examples you may need to patch global module (like some tracer).

It will flush list of catched `requests` between each test.

Catching these methods: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`

You may want to setup your app fixture with catch server as dependency. You can
use session scoped fixture `background_catch_server` for that:

```python
@pytest.fixture(scope="session")
def app(background_catch_server):
    tracer_dsn = f"http://{background_catch_server.host}:{background_catch_server.port}"
    return create_app(tracer_dsn=tracer_dsn)

def test_tracing(app, catch_server):
    app.do_something_that_calls_tracer()
    assert catch_server.requests == [
        {"method": "PUT", "path": "/trace", "data": b"..."}
    ]
```

Port for catch server is a random free port. If you want to use specific port, you
can override `catch_server_port` fixture in your tests which is returning free
port number.

If you encounter any problems, please
[file an issue](https://github.com/kiwicom/pytest-catch-server/issues) along
with a detailed description.

## Contributing

Contributions are very welcome. Tests can be run with
[tox](https://tox.readthedocs.io/en/latest/), please ensure the coverage at
least stays the same before you submit a pull request.

[Pre-commit](https://pre-commit.com/) hooks are set up for this project. Please
make sure you have [pre-commit](https://pre-commit.com/) installed and set up on
this repo.

## License

Distributed under the terms of the [MIT](http://opensource.org/licenses/MIT)
license, "pytest-catch-server" is free and open source software.

## Footnote

This [pytest](https://pytest.org) plugin was generated with [Cookiecutter](https://github.com/cookiecutter/cookiecutter)
along with [@hackebrot's](https://github.com/hackebrot)
[cookiecutter-pytest-plugin](https://github.com/pytest-dev/cookiecutter-pytest-plugin) template.
