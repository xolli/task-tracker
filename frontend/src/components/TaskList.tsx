import TaskItem from './TaskItem'
import type { Task, TaskStatus } from '../api/tasks'

interface Props {
  tasks: Task[]
  onToggleStatus: (id: number, next: TaskStatus) => void
  onDelete: (id: number) => void
}

export default function TaskList({ tasks, onToggleStatus, onDelete }: Props) {
  if (!tasks.length) {
    return (
      <div className="rounded-lg border border-dashed border-gray-300 p-8 text-center text-gray-500">
        No tasks yet. Add your first task above.
      </div>
    )
  }
  return (
    <div className="space-y-3">
      {tasks.map((t) => (
        <TaskItem key={t.id} task={t} onToggleStatus={onToggleStatus} onDelete={onDelete} />
      ))}
    </div>
  )
}
