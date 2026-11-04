# ReturnLoop LPU — 100% Free Cloud Deployment Guide (₹0 Stack)

This guide explains how to deploy **ReturnLoop LPU** to the internet completely free (₹0, zero credit card required).

---

## 1. Architecture Overview

| Component | Technology | Recommended Free Host | Cost |
| :--- | :--- | :--- | :--- |
| **Frontend** | React 19 + Vite + Tailwind | **Netlify** or **Vercel** | **100% Free Forever** |
| **Backend** | Python Flask + SQLAlchemy | **Render.com** (or **PythonAnywhere**) | **100% Free** |
| **Database** | SQLite / Neon PostgreSQL | Local SQLite or **Neon.tech** | **100% Free** |

> [!NOTE]
> **Why can't Netlify host the Flask backend directly?**  
> Netlify is specialized for static frontend assets (HTML, CSS, React, Vue) and serverless JavaScript functions. It does not run persistent Python Flask web servers or background Python threads.  
> Therefore, modern production architecture splits the system: **Netlify hosts the React frontend**, and **Render hosts the Flask API backend**.

---

## 2. Deploying the Frontend to Netlify (Free)

### Method A: Via GitHub (Recommended)
1. Push your project to GitHub:
   ```bash
   git add .
   git commit -m "Prepare production deployment"
   git push origin main
   ```
2. Go to [netlify.com](https://www.netlify.com) and log in with GitHub.
3. Click **"Add new site"** -> **"Import an existing project"** -> Select your **ReturnLoop** repository.
4. Netlify will automatically detect `netlify.toml`:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/dist`
5. Under **Environment variables**, add:
   - `VITE_API_BASE_URL`: `https://your-backend-name.onrender.com` (replace with your Render backend URL once created).
6. Click **"Deploy site"**. Your frontend will be live at `https://your-app-name.netlify.app`.

### Method B: Drag-and-Drop (Instant, No GitHub Required)
1. In your local terminal, build the production frontend:
   ```bash
   cd frontend
   npm run build
   ```
   This creates a `frontend/dist` folder.
2. Go to [app.netlify.com/drop](https://app.netlify.com/drop).
3. Drag and drop the `dist` folder directly into your browser.
4. Netlify will deploy your site in ~10 seconds with a free `.netlify.app` URL and free SSL certificate.

---

## 3. Deploying the Backend to Render.com (Free)

[Render.com](https://render.com) provides a free Web Service tier that runs Python Flask apps with zero cost.

### Step-by-Step Instructions:
1. Go to [render.com](https://render.com) and sign up for free (using GitHub or Google).
2. Click **"New +"** -> **"Web Service"**.
3. Connect your **ReturnLoop** GitHub repository.
4. Configure the Web Service settings:
   - **Name**: `returnloop-lpu-api`
   - **Region**: Singapore or Frankfurt (closest to your location)
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`
   - **Instance Type**: `Free` (0.1 CPU, 512 MB RAM)
5. Scroll down to **Environment Variables** and add:
   - `SECRET_KEY`: (generate any secure random string, e.g. `lpu-returnloop-production-secret-2026`)
   - `JWT_SECRET_KEY`: (generate any secure random string, e.g. `lpu-jwt-token-key-super-safe-99`)
   - `FLASK_DEBUG`: `False`
   - `DEV_ADMIN_EMAIL`: `admin@returnloop.lpu.in`
   - `DEV_ADMIN_PASSWORD`: `AdminPass123!`
   - `CORS_ORIGINS`: `https://your-app-name.netlify.app,http://localhost:5173`
6. Click **"Create Web Service"**.
7. Render will build and deploy your API in ~2 minutes. Once finished, Render gives you a free HTTPS URL:
   `https://returnloop-lpu-api.onrender.com`

---

## 4. Alternative: Deploy Backend to PythonAnywhere (100% Free)

If you prefer a host that natively keeps your **SQLite** file permanently on disk without resetting when idle:
1. Sign up for free at [pythonanywhere.com](https://www.pythonanywhere.com).
2. Go to the **Web** tab -> **"Add a new web app"** -> Select **Flask** -> **Python 3.10**.
3. Upload your `backend/` folder via the Files tab or `git clone` in the Bash console.
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. In the Web tab, point the WSGI configuration file to `run.py`.
6. Your backend will run at `https://yourusername.pythonanywhere.com`.

---

## 5. Linking Frontend and Backend

Once your backend is live:
1. Open your Netlify dashboard for the frontend.
2. Go to **Site configuration** -> **Environment variables**.
3. Set:
   ```env
   VITE_API_BASE_URL=https://returnloop-lpu-api.onrender.com
   ```
4. Trigger a new deploy (**Deploys** -> **Trigger deploy** -> **Clear cache and deploy site**).
5. Open your Netlify URL: your frontend will now communicate with your live cloud backend!

---

## 6. Pre-Configured Files in Codebase

To make your deployment effortless, the following files are already configured in this repository:
- `netlify.toml`: Directs Netlify on root build commands and configures client-side React Router redirects (`/* -> /index.html`).
- `frontend/public/_redirects`: Prevents 404 errors on browser page reloads in Netlify.
- `backend/requirements.txt`: Includes production `gunicorn>=21.2.0` WSGI server.
- `backend/run.py`: Automatically runs database table creation and admin seeding on cloud boot.
