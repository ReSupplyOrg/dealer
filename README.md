# dealer
Dealer is the backend for the ReSupply application

## Contributing

Make sure you follow the [CONTRIBUTING.md](CONTRIBUTING.md) guidelines before making changes to the project.

## Documentation

| Document                             | Description                                                  |
| ------------------------------------ | ------------------------------------------------------------ |
| [docs/Database.md](docs/Database.md) | Database documentation including schemas, triggers and procedures |
| [docs/CICD.md](docs/CICD.md)         | CICD documentation.                                          |
|                                      |                                                              |

## Development

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

