# Database Migration

## How to create a new migration

1. Create a new migration file using the following command:

```bash
docker exec -it -w /webapi webapi-auth alembic revision --autogenerate -m "migration message"
```

2. Check the migration file created in the `webapi/migrations/versions` directory.

3. If the migration file is correct, apply the migration using the following command:

```bash
docker exec -it -w /webapi webapi-auth alembic upgrade head
```

## How to rollback the migration

1. Rollback the migration using the following command:

```bash
docker exec -it -w /webapi webapi-auth alembic downgrade -1
```

2. Check the migration file deleted in the `webapi/migrations/versions` directory.

3. If the migration file is correct, apply the migration using the following command:

```bash
docker exec -it -w /webapi webapi-auth alembic upgrade head
```

## How to check the migration history

1. Check the migration history using the following command:

```bash
docker exec -it -w /webapi webapi-auth alembic history
```

## How to check the migration status

1. Check the migration status using the following command:

```bash
docker exec -it -w /webapi webapi-auth alembic current
```

