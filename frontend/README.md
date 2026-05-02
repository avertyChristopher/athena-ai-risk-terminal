# Athena Frontend

The frontend is a Vite + React + TypeScript shell aligned with `docs/architecture.md`.

## Run locally

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173`.

## Environment

Copy `.env.example` if you want to override defaults:

```bash
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=Athena AI Risk Terminal
```

## Current foundation

- App shell with sidebar, topbar, and routed placeholder pages.
- Bilingual UI using English and French translation files.
- Shared API client and a `useHealth` hook for `GET /api/health`.
- Reusable finance display components ready for future feature work.
