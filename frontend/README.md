# TaskTracker Frontend (React + Vite + Tailwind)

A simple SPA for managing tasks: add, list, change status, and delete. Connects to a REST API at `http://localhost:8000` with a Vite dev proxy to avoid CORS in development.

## Features
- View list of tasks (title, description, status)
- Add a new task (title, optional description)
- Change task status (cycles: pending → in_progress → done → pending)
- Delete a task
- Basic filtering: All, Pending, In progress, Done
- Responsive layout (320–1440px)

## Tech Stack
- React + TypeScript + Vite
- Tailwind CSS (no external UI libraries)

## Development
1. Install dependencies
   ```bash
   npm i
   ```
2. Start the backend on `http://localhost:8000` (for example with `../docker/prod/docker-compose.yml`)
3. Start the dev server
   ```bash
   npm run dev
   ```

Open the app at http://localhost:5173


## Project Structure
- `src/api/tasks.ts` — TypeScript types and API calls
- `src/components/TaskForm.tsx` — form to add a task
- `src/components/TaskItem.tsx` — task row with status button and delete
- `src/components/TaskList.tsx` — list of tasks
- `src/App.tsx` — main page: filters, list, CRUD operations

## Notes
- In production, ensure the frontend is hosted under the same origin as the backend
