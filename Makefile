.PHONY: setup install dev prod test clean backup logs restart

setup:
	chmod +x scripts/*.sh
	./scripts/setup.sh

install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

dev:
	docker-compose up

prod:
	docker-compose -f docker-compose.prod.yml up -d

test:
	./scripts/test.sh

backup:
	./scripts/backup.sh

clean:
	docker-compose down -v || true
	rm -rf backend/__pycache__ || true
	rm -rf backend/reports/* || true
	rm -rf backend/logs/* || true
	rm -rf frontend/node_modules || true
	rm -rf frontend/build || true

logs:
	docker-compose logs -f

restart:
	docker-compose restart
