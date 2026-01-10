build:
	docker compose -f docker-compose.yml up -d --build $(app)

log:
	docker compose -f docker-compose.yml logs -f $(app)

down:
	docker compose -f docker-compose.yml down $(app)


build-debug:
	docker compose --env-file ./debug.env -f docker-compose.yml -f docker-compose.dev.yml up -d --build $(app)


down-debug:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml down $(app)


log-debug:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml logs -f $(app)


.PHONY: migration-create
migration-create:
	docker compose --env-file ./debug.env run  --rm migrations uv run alembic -c alembic.ini revision --autogenerate -m "$(msg)"

.PHONY: migration-upgrade
migration-upgrade:
	docker compose run --rm migrations uv run alembic -c alembic.ini upgrade head

migration-downgrade:
	docker compose run --rm migrations uv run alembic -c alembic.ini downgrade -1

alembic-revision:
	alembic -c backend/alembic.ini revision --autogenerate -m "init schema"