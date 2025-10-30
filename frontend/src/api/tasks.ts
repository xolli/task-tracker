export type TaskStatus = 'pending' | 'in_progress' | 'done'

export interface Task {
  id: number
  title: string
  description?: string
  status: TaskStatus
  created_at?: string
  updated_at?: string
}

export interface NewTask {
  title: string
  description?: string
  status?: TaskStatus
}

export type UpdateTask = Partial<Pick<Task, 'title' | 'description' | 'status'>>

const BASE = '' // use Vite proxy in dev; empty means same origin

async function request<T>(input: RequestInfo, init?: RequestInit): Promise<T> {
  const res = await fetch(input, {
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers || {}),
    },
    ...init,
  })
  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(`API error ${res.status}: ${text || res.statusText}`)
  }
  if (res.status === 204) return undefined as unknown as T
  return res.json() as Promise<T>
}

export async function getTasks(status?: TaskStatus): Promise<Task[]> {
  const url = new URL(`${BASE}/tasks`, window.location.origin)
  if (status) url.searchParams.set('status', status)
  return request<Task[]>(url.toString())
}

export async function createTask(body: NewTask): Promise<{ id: number }> {
  return request<{ id: number }>(`${BASE}/tasks`, {
    method: 'POST',
    body: JSON.stringify({ status: 'pending', ...body }),
  })
}

export async function updateTask(id: number, patch: UpdateTask): Promise<Task> {
  return request<Task>(`${BASE}/tasks/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(patch),
  })
}

export async function deleteTask(id: number): Promise<void> {
  await request<void>(`${BASE}/tasks/${id}`, { method: 'DELETE' })
}

export function nextStatus(status: TaskStatus): TaskStatus | undefined {
  if (status === 'pending') return 'in_progress'
  if (status === 'in_progress') return 'done'
  return undefined
}
