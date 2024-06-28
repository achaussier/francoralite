# Francoralite
![example workflow](https://github.com/Francoralite/francoralite/actions/workflows/docker_publish_image.yml/badge.svg)
[![codecov](https://codecov.io/gh/Francoralite/francoralite/branch/develop/graph/badge.svg?token=0FZPO67WYJ)](https://codecov.io/gh/Francoralite/francoralite)

## Installation

### System dependencies


* Install Docker

See [Docker CE](https://docs.docker.com/install/#platform-support-matrix)

### Git dependencies

* Clone the repository

```
git clone git@github.com:francoralite/francoralite.git
```

* Manage sub modules

```
git submodule update --recursive --init
```

### Run stack

> You must have Docker Compose 2 installed (update to last version)

```
docker compose watch
```

## Documentation

Documentation is managed with [mkdocs](https://www.mkdocs.org/).

### Show documentation

```
docker run --rm -it -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material
```

### Run tests (back and front)

We need to install tests dependencies inside container before run tests

```
docker compose down && KEYCLOAK_HOSTNAME=keycloak docker compose up -d

# If Keycloak not initialized, run this command
KEYCLOAK_HOSTNAME=keycloak ./scripts/load_keycloak_data.sh

# Prepare tests dependencies
./scripts/load_env_test.sh
```

Now, we can launch all tests
```
docker compose exec app bash -c 'py.test -Werror -x'
```

In case, we want to launch front tests only
```
docker compose exec app bash -c 'py.test francoralite/apps/francoralite_front/tests/ -x'
```

### Generate graph models

```
docker compose exec app bash -c './scripts/generate_graph_models.sh'
```

## URLs

> Replace **50000** with your Traefik listening port

With Traefik as reverse proxy, you can use explicit fqdn instead IP addresses.

* [Root app](http://nginx.francoralite.localhost:50000)
* [Keycloak](http://keycloak.francoralite.localhost:50000)

During development, all services are accessible behind the reverse proxy but this must be change for the production deployment.

### Documentation

> You **MUST** update the permission linked to these URLs

* [Redoc UI](http://nginx.francoralite.localhost:50000/redoc/)
* [Swagger UI](http://nginx.francoralite.localhost:50000/swagger/)
* [JSON Swagger export](http://nginx.francoralite.localhost:50000/swagger.json)
* [YAML Swagger export](http://nginx.francoralite.localhost:50000/swagger.yaml)
