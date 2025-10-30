import { nextStatus, type Task, type TaskStatus } from '../api/tasks'

interface Props {
  task: Task
  onToggleStatus: (id: number, next: TaskStatus) => void
  onDelete: (id: number) => void
}

const statusColors: Record<TaskStatus, string> = {
  pending: 'bg-yellow-100 text-yellow-800 ring-yellow-600/20',
  in_progress: 'bg-blue-100 text-blue-800 ring-blue-600/20',
  done: 'bg-green-100 text-green-800 ring-green-600/20',
}

export default function TaskItem({ task, onToggleStatus, onDelete }: Props) {
  const next = nextStatus(task.status)
  return (
    <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3 justify-between rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
      <div className="min-w-0">
        <div className="flex items-center gap-2">
          <h3 className="text-base font-semibold text-gray-900 truncate">{task.title}</h3>
          <span className={`inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset ${statusColors[task.status]}`}>
            {labelForStatus(task.status)}
          </span>
        </div>
        {task.description && (
          <p className="mt-1 text-sm text-gray-600 whitespace-pre-wrap break-words">{task.description}</p>
        )}
        {(task.created_at || task.updated_at) && (
          <p className="mt-1 text-xs text-gray-400">
            {task.created_at && <>Created: {formatDate(task.created_at)} </>}
          </p>
        )}
      </div>
      <div className="flex items-center gap-2 w-full sm:w-auto">
          {next &&
              <button
                  onClick={() => onToggleStatus(task.id, next)}
                  className="inline-flex items-center justify-center rounded-md border border-gray-300 bg-white px-3 py-1.5 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50"
              >
                  Move to {labelForStatus(next)}
              </button>
          }
        <button
          onClick={() => onDelete(task.id)}
          className="inline-flex items-center justify-center rounded-md bg-rose-600 px-3 py-1.5 text-sm font-medium text-white shadow-sm hover:bg-rose-700"
        >
          Delete
        </button>
      </div>
    </div>
  )
}

function labelForStatus(s: TaskStatus): string {
  if (s === 'pending') return 'Pending'
  if (s === 'in_progress') return 'In progress'
  return 'Done'
}

function formatDate(iso: string): string {
  try {
    const d = new Date(iso)
    return d.toLocaleString()
  } catch {
    return iso
  }
}
