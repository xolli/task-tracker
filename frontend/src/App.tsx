import {useEffect, useMemo, useState} from 'react'
import TaskForm from './components/TaskForm'
import TaskList from './components/TaskList'
import {type Task, type TaskStatus, createTask, deleteTask, getTasks, updateTask} from './api/tasks'

function App() {
    const [tasks, setTasks] = useState<Task[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    const [filter, setFilter] = useState<'all' | TaskStatus>('all')

    useEffect(() => {
        let active = true
        setLoading(true)
        getTasks(filter === 'all' ? undefined : filter)
            .then((data) => {
                if (!active) return
                setTasks(data)
                setError(null)
            })
            .catch((e) => active && setError(e.message || 'Failed to load tasks'))
            .finally(() => active && setLoading(false))
        return () => {
            active = false
        }
    }, [filter])

    const counts = useMemo(() => {
        const base = {all: tasks.length, pending: 0, in_progress: 0, done: 0}
        for (const t of tasks) {
            if (t.status === 'pending') base.pending++
            else if (t.status === 'in_progress') base.in_progress++
            else base.done++
        }
        return base
    }, [tasks])

    async function handleAdd({title, description}: { title: string; description?: string }) {
        await createTask({title, description})
        const fresh = await getTasks(filter === 'all' ? undefined : filter)
        setTasks(fresh)
    }

    async function handleToggleStatus(id: number, next: TaskStatus) {
        setTasks((prev) => prev.map((t) => (t.id === id ? {...t, status: next} : t)))
        try {
            const updated = await updateTask(id, {status: next})
            setTasks((prev) => prev.map((t) => (t.id === id ? updated : t)))
        } catch (e: unknown) {
            if (e instanceof Error) {
                setError(e.message)
            } else {
                setError('Failed to update task')
            }
            const fresh = await getTasks(filter === 'all' ? undefined : filter)
            setTasks(fresh)
        }
    }

    async function handleDelete(id: number) {
        const prev = tasks
        setTasks((curr) => curr.filter((t) => t.id !== id))
        try {
            await deleteTask(id)
        } catch (e: unknown) {
            if (e instanceof Error) {
                setError(e.message)
            } else {
                setError('Failed to update task')
            }
            setTasks(prev)
        }
    }

    return (
        <div className="min-h-full">
            <header className="bg-white border-b border-gray-200">
                <div className="mx-auto max-w-5xl px-4 py-4 sm:py-6">
                    <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">Task Tracker</h1>
                    <p className="text-sm text-gray-500">Add, track, update, and delete your tasks</p>
                </div>
            </header>

            <main className="mx-auto max-w-5xl px-4 py-6 sm:py-8">
                <section className="mb-6">
                    <TaskForm onSubmit={handleAdd}/>
                </section>

                <section className="mb-4">
                    <div className="flex flex-wrap items-center gap-2">
                        <FilterButton active={filter === 'all'} onClick={() => setFilter('all')}>
                            All
                            {filter === 'all' && counts.all > 0 && <Badge>{counts.all}</Badge>}
                        </FilterButton>
                        <FilterButton active={filter === 'pending'} onClick={() => setFilter('pending')}>
                            Pending
                            {filter === 'pending' && counts.pending > 0 && <Badge>{counts.pending}</Badge>}
                        </FilterButton>
                        <FilterButton active={filter === 'in_progress'} onClick={() => setFilter('in_progress')}>
                            In progress
                            {filter === 'in_progress' && counts.in_progress > 0 && <Badge>{counts.in_progress}</Badge>}
                        </FilterButton>
                        <FilterButton active={filter === 'done'} onClick={() => setFilter('done')}>
                            Done
                            {filter === 'done' && counts.done > 0 && <Badge>{counts.done}</Badge>}
                        </FilterButton>
                        <div className="ml-auto text-sm text-gray-500">
                            {loading ? 'Loading...' : error ?
                                <span className="text-rose-600">{error}</span> : `${tasks.length} task(s)`}
                        </div>
                    </div>
                </section>

                <section>
                    {loading ? (
                        <div
                            className="rounded-lg border border-gray-200 bg-white p-6 text-center text-gray-500">Loading
                            tasks...</div>
                    ) : (
                        <TaskList tasks={tasks} onToggleStatus={handleToggleStatus} onDelete={handleDelete}/>
                    )}
                </section>
            </main>
        </div>
    )
}

function FilterButton({active, onClick, children}: {
    active: boolean;
    onClick: () => void;
    children: React.ReactNode
}) {
    return (
        <button
            onClick={onClick}
            className={
                'inline-flex items-center gap-2 rounded-md border px-3 py-1.5 text-sm transition ' +
                (active
                    ? 'border-indigo-600 bg-indigo-50 text-indigo-700'
                    : 'border-gray-300 bg-white text-gray-700 hover:bg-gray-50')
            }
        >
            {children}
        </button>
    )
}

function Badge({children}: { children: React.ReactNode }) {
    return (
        <span
            className="ml-1 inline-flex items-center rounded-full bg-indigo-600 px-2 py-0.5 text-xs font-medium text-white">
      {children}
    </span>
    )
}

export default App
