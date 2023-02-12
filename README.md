# dealer
Dealer is the backend for the ReSupply application

## Contributing

Make sure you follow the [CONTRIBUTING.md](CONTRIBUTING.md) guidelines before making changes to the project.

## Documentation

| Document                             | Description                                                  |
| ------------------------------------ | ------------------------------------------------------------ |
| [docs/Database.md](docs/Database.md) | Database documentation including schemas, triggers and procedures |
| [docs/CICD.md](docs/CICD.md)         | CICD documentation.                                          |
| [Deploy.md](Deploy.md)               | Deployment manual                                            |

## Development

### Virtual environment

Make sure you have a virtual environment.

```shell
python -m venv venv && ./venv/scripts/activate
```

Install dependencies

```shell
pip install -r requirements.txt
```

### Services

To start the `redis` and `postgres` service in the localhost run:

```shell
docker compose up -d
```

Then you can run the application with:

```shell
./dev.ps1
```

## Testing API

For testing purpose you can deploy a **testing API** using:

```shell
docker compose -f ./api-test.docker-compose.yaml up -d
```

