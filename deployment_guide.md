# Deployment Guide: Medisync (Synapse Clinical AI) 🚀

Your code is now live on GitHub: [https://github.com/Ansh7473/medisync](https://github.com/Ansh7473/medisync). Follow these steps to host it in the cloud.

---

## 1. Frontend Deployment (Cloudflare Pages)
**Best for:** Vite/React (Fast, Global, and Free tier available).

### Step-by-Step:
1.  Log in to the [Cloudflare Dashboard](https://dash.cloudflare.com/).
2.  Go to **Workers & Pages** > **Create application** > **Pages** > **Connect to Git**.
3.  Select your `medisync` repository.
4.  **Build Settings**:
    -   **Framework preset**: `Vite`
    -   **Build command**: `npm run build`
    -   **Build output directory**: `dist`
    -   **Root directory**: `/frontend` (IMPORTANT: Point this to the frontend folder).
5.  Click **Save and Deploy**.

---

## 2. Backend Deployment (Railway)
**Best for:** Python FastAPI (Easy setup for environment variables).

### Step-by-Step:
1.  Log in to [Railway.app](https://railway.app/).
2.  Click **+ New Project** > **Deploy from GitHub repo**.
3.  Choose your `medisync` repository.
4.  Go to the **Variables** tab and add:
    -   `GROQ_API_KEY`: Your key from Groq Cloud.
    -   `ELEVENLABS_API_KEY`: (Optional) If you want premium voice.
5.  Railway will automatically detect the `server.py` and the `requirements.txt` and start the server.
6.  Copy the generated URL (e.g., `medisync-production.up.railway.app`).

---

## 3. Linking Frontend to Backend
Once your backend is live (e.g., on Railway):
1.  In your local code, update the `API_BASE_URL` in `frontend/src/App.jsx`:
    ```javascript
    const API_BASE_URL = 'https://YOUR-BACKEND-URL.railway.app';
    ```
2.  Commit and push the change:
    ```bash
    git add .
    git commit -m "Update API URL for production"
    git push
    ```
3.  Cloudflare Pages will automatically rebuild and your app will be live!

---

## 🏆 Summary of Platform Choices
| Component | Best Cloud Provider | Why? |
| :--- | :--- | :--- |
| **Frontend** | **Cloudflare Pages** | Native Vite support, global CDN. |
| **Backend** | **Railway / Render** | Better for persistent Python web services. |
| **Domain** | **Cloudflare** | Already integrated with Pages. |

> [!TIP]
> Use **Render.com** if you prefer a simplified free tier for web services, though it may take a few seconds to "wake up" on the first request.
