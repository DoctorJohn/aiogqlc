# Python Asyncio GraphQL Client

[![Versions][versions-image]][versions-url]
[![PyPI][pypi-image]][pypi-url]
[![Downloads][downloads-image]][downloads-url]
[![Codecov][codecov-image]][codecov-url]
[![License][license-image]][license-url]

[versions-image]: https://img.shields.io/pypi/pyversions/aiogqlc
[versions-url]: https://github.com/DoctorJohn/aiogqlc/blob/master/setup.py
[pypi-image]: https://img.shields.io/pypi/v/aiogqlc
[pypi-url]: https://pypi.org/project/aiogqlc/
[downloads-image]: https://img.shields.io/pypi/dm/aiogqlc
[downloads-url]: https://pypi.org/project/aiogqlc/
[codecov-image]: https://codecov.io/gh/DoctorJohn/aiogqlc/branch/main/graph/badge.svg?token=63WRUHG8SW
[codecov-url]: https://codecov.io/gh/DoctorJohn/aiogqlc
[license-image]: https://img.shields.io/pypi/l/aiogqlc
[license-url]: https://github.com/DoctorJohn/aiogqlc/blob/master/LICENSE

A simple asynchronous Python GraphQL client based on [asyncio][asyncio-url] and [aiohttp][aiohttp-url].

**[Get started](getting-started.md)**

## Features

- It's just a lightweight wrapper around [aiohttp][aiohttp-url] client sessions
- Support for **queries** and **mutations** compatible with the [GraphQL over HTTP spec][http-specs-url]
- Support for **file uploads** following the [GraphQL multipart form requests spec][multipart-specs-url]
- Support for **subscriptions** following the [graphql-ws protocol spec][graphql-ws-specs-url]
- Fully type annotated code base
- Full test coverage

[asyncio-url]: https://docs.python.org/3/library/asyncio.html
[aiohttp-url]: https://github.com/aio-libs/aiohttp
[http-specs-url]: https://github.com/graphql/graphql-over-http
[multipart-specs-url]: https://github.com/jaydenseric/graphql-multipart-request-spec
[graphql-ws-specs-url]: https://github.com/apollographql/subscriptions-transport-ws
