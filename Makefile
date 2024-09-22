ifneq (,$(wildcard ./.env))
	include .env
	export
endif

.PHONY: up down init-db logs

up:
	docker-compose up -d

down:
	docker-compose down -v

# Initialize the database (if needed)
init-db:
	@echo "Initializing the database..."
	@until docker-compose exec db pg_isready -U ${POSTGRES_USER} -h db -p ${POSTGRES_PORT}; do \
		echo "PostgreSQL is unavailable - sleeping"; \
		sleep 2; \
	done
	@echo "Database is up! Running the init_db.sql script..."
	@docker-compose exec -e PGPASSWORD=${POSTGRES_PASSWORD} db psql -U ${POSTGRES_USER} -h db -p ${POSTGRES_PORT} -d ${POSTGRES_DB} -f /docker-entrypoint-initdb.d/init_db.sql || true
	@echo "Database initialization complete."
logs:
	docker-compose logs -f app

run: up init-db
	@if ! poetry run python -c "import loguru" >/dev/null 2>&1; then \
		echo "Dependencies are missing. Running 'poetry lock' and 'poetry install'..."; \
		poetry lock && poetry install; \
	fi
	poetry run python main.py

test: up init-db
	poetry run pytest tests/test_metrics_collector.py
