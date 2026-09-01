# Acad’Emy

Site web du centre de formation professionnelle **Acad’Emy** — *Learn. Build. Lead.* — filiale de LawApp Group50.

Le projet comprend un site public bilingue (FR / EN) en Vue 3 et une API FastAPI connectée à PostgreSQL (Supabase). Un espace d’administration permet de gérer les formations, sessions, inscriptions, actualités, témoignages et coordonnées.

## Démarrage local

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # renseigner DATABASE_URL, SECRET_KEY, identifiants admin
uvicorn app.main:app --reload --host 0.0.0.0 --port 8765
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Le site s’ouvre sur [http://127.0.0.1:4321](http://127.0.0.1:4321). Les appels `/api` sont proxifiés vers le backend.

## Espace équipe

- URL : `/admin/login`
- Identifiants par défaut (à changer) : `admin@acad-emy.com` / `AcadEmy243!`

## Pages publiques

Accueil, À propos, Nos formations, Calendrier et inscriptions, Entreprises, Actualités, Contact — plus le formulaire d’inscription et WhatsApp.

## Déploiement

Le frontend Vue peut être déployé sur Vercel (`frontend/` comme racine, `npm run build`, dossier `dist`). L’API FastAPI doit tourner sur un hébergeur Python (Render, Railway, Fly.io, etc.) avec les variables d’environnement du fichier `.env.example`. En production, pointer `VITE` n’est pas nécessaire : configurer le reverse-proxy `/api` vers l’API, ou servir `frontend/dist` depuis FastAPI.
