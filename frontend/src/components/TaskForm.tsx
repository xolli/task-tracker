import { useState, type FormEvent } from 'react'

interface Props {
  onSubmit: (data: { title: string; description?: string }) => Promise<void> | void
}

export default function TaskForm({ onSubmit }: Props) {
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    if (!title.trim()) return
    try {
      setLoading(true)
      await onSubmit({ title: title.trim(), description: description.trim() || undefined })
      setTitle('')
      setDescription('')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <div className="flex flex-col sm:flex-row gap-3">
        <input
          type="text"
          className="flex-1 rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          placeholder="Task title *"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
          maxLength={200}
        />
        <button
          type="submit"
          disabled={loading || !title.trim()}
          className="rounded-md bg-indigo-600 px-4 py-2 text-white font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:bg-indigo-700 transition"
        >
          {loading ? 'Adding...' : 'Add Task'}
        </button>
      </div>
      <textarea
        className="w-full rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        placeholder="Description (optional)"
        rows={3}
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        maxLength={1000}
      />
    </form>
  )
}
