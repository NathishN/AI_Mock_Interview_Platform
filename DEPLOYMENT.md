# Deployment Guide — InterviewAce AI

This guide walks you through deploying the InterviewAce AI application to production.

---

## Architecture Overview

- **Frontend:** React 19 + Vite + TypeScript + Tailwind CSS
  - Target: **Vercel** (or Netlify / Cloudflare Pages)
  - Pre-configured with `vercel.json` for Single Page Application (SPA) routing.
- **Backend:** FastAPI + Python 3.12 + SQLAlchemy + Alembic + JWT Auth
  - Target: **Render**, **Railway**, **Fly.io**, or any container platform
  - Database: **Managed PostgreSQL** (Supabase, Neon, Render, or Railway)

---

## 1. Deploying the Backend (API + Database)

The backend needs a persistent PostgreSQL database and Python/Docker environment.

### Option A: Render (Recommended & Fastest with `render.yaml`)

We included a `render.yaml` blueprint in the repository root.

1. Push your repository to **GitHub** or **GitLab**.
2. Log into [Render](https://render.com/).
3. Click **New +** -> **Blueprint**.
4. Connect your repository. Render will automatically detect `render.yaml` and configure:
   - A free managed **PostgreSQL** database (`interviewace-db`).
   - A web service for the **FastAPI backend** building directly from `./backend/Dockerfile`.
5. Under Environment Variables in the Render dashboard, set:
   - `GROQ_API_KEY`: Your Groq API key (`gsk_...`)
   - `CORS_ORIGINS`: Your Vercel frontend URL (e.g. `https://your-app.vercel.app`)
6. Deploy! Render will run Alembic migrations and bootstrap the questions database automatically.
7. Note down your backend URL (e.g., `https://interviewace-backend.onrender.com`).

---

### Option B: Railway

1. Go to [Railway.app](https://railway.app/) and create a **New Project**.
2. Add a **PostgreSQL** plugin.
3. Add a **GitHub Repo** service pointing to your repository:
   - Set **Root Directory** to `/backend` (or use Dockerfile).
4. In Railway variables, set:
   - `DATABASE_URL`: `${{Postgres.DATABASE_URL}}`
   - `ENVIRONMENT`: `production`
   - `JWT_SECRET_KEY`: A secure 32+ character random secret string
   - `CORS_ORIGINS`: Your frontend URL (e.g., `https://your-app.vercel.app`)
   - `GROQ_API_KEY`: Your Groq API key
   - `SEED_QUESTIONS`: `true`
5. Generate a public domain under Settings -> Networking.

---

## 2. Deploying the Frontend to Vercel

1. Push your code to **GitHub**.
2. Go to [Vercel](https://vercel.com/) and click **Add New...** -> **Project**.
3. Import your GitHub repository.
4. In the project configuration:
   - **Root Directory:** Click **Edit** and choose `interviewace/frontend` (or `frontend` if the repo root is already `interviewace`).
   - **Framework Preset:** Vite (automatically detected).
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
5. Under **Environment Variables**, add:
   - **Name:** `VITE_API_URL`
   - **Value:** `https://<your-backend-domain>/api/v1` (e.g., `https://interviewace-backend.onrender.com/api/v1`)
6. Click **Deploy**.

> **Note:** We already created [`frontend/vercel.json`](file:///d:/interviewace-phase2-ab/interviewace/frontend/vercel.json) with SPA rewrites so direct navigation to subpages like `/login` or `/dashboard` won't result in 404 errors.

---

## 3. Post-Deployment Verification

1. Open your Vercel URL in your browser.
2. Verify you can access the login and signup pages.
3. Test logging in with your bootstrapped admin or create a new user account.
4. If CORS errors occur:
   - Check that `CORS_ORIGINS` in your backend environment matches your exact Vercel domain (including `https://` with no trailing slash).
