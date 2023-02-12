# Deploy

## Environment variables

| Name                    | Example                     | Description                                      |
| ----------------------- | --------------------------- | ------------------------------------------------ |
| `PRODUCTION`            | `true`                      | Turns the application to production mode         |
| `SECRET_KEY`            | `RANDOM_STRING`             | `SECRET KEY` used by the application             |
| `POSTGRES_DATABASE`     | `dealer`                    | Database name                                    |
| `POSTGRES_USERNAME`     | `dealer_admin`              | Database username                                |
| `POSTGRES_PASSWORD`     | `password`                  | Database password                                |
| `POSTGRES_HOST`         | `dealer-postgres`           | Database IP / DNS                                |
| `POSTGRES_PORT`         | `5432`                      | Database port                                    |
| `REDIS_LEADER`          | `redis://dealer-redis:6379` | Redis Leader                                     |
| `REDIS_WORKER_{NUMBER}` | `redis://dealer-redis:6379` | Redis workers `NUMBER` ranges from 1 to infinite |

