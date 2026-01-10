#!/bin/bash

set -e

echo "🚀 Setting up SnippetVault development environment..."

echo "📝 Creating/Updating .env file..."
cat > .env << EOF
# Database
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=snippetvault

# Backend
BACKEND_PORT=8000
SECRET_JWT_SECRET=dev_secret_key_change_me
PROVIDER_YANDEX_CLIENT_ID=
PROVIDER_YANDEX_CLIENT_SECRET=
PROVIDER_YANDEX_REDIRECT_URI=http://localhost:5173/auth/callback

# Frontend
FRONTEND_PORT=5173
VITE_API_URL=http://localhost:8000
VITE_YANDEX_REDIRECT_URI=http://localhost:5173/

EOF
echo "✅ .env file updated"

echo "📝 Creating/Updating backend/.env file..."
cat > backend/.env << EOF
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=snippetvault
SECURE_JWT_SECRET=dev_secret_key_change_me
PROVIDER_YANDEX_CLIENT_ID=
PROVIDER_YANDEX_CLIENT_SECRET=
PROVIDER_YANDEX_REDIRECT_URI=http://localhost:5173/auth/callback
EOF
echo "✅ backend/.env updated"

echo "📝 Creating/Updating frontend/.env file..."
cat > web/.env << EOF
VITE_API_URL=http://localhost:8000
VITE_YANDEX_CLIENT_ID=your_client_id_here
VITE_YANDEX_REDIRECT_URI=http://localhost:5173/
EOF
echo "✅ frontend/.env updated"

echo "🐳 Building Docker containers..."
docker compose -f docker-compose.yml -f docker-compose.dev.yml build

echo "🗄️ Starting PostgreSQL..."
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d postgres

echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 5

echo "📦 Running database migrations..."
docker compose -f docker-compose.yml -f docker-compose.dev.yml run --rm backend alembic upgrade head

echo "✅ Setup complete!"
echo ""
echo "To start all services, run:"
echo "  docker compose -f docker-compose.yml -f docker-compose.dev.yml up"
echo ""
echo "Or use shortcuts:"
echo "  npm run dev    (if you add this to package.json in root)"
echo ""
