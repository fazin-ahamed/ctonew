import React, { useEffect, useState } from 'react'

export const Automation = () => {
  const [workflows, setWorkflows] = useState<any[]>([])

  useEffect(() => {
    // mock fetch
    setWorkflows([
        { id: 1, name: 'Lead Assignment', trigger: 'lead_created', active: true },
        { id: 2, name: 'Invoice Reminder', trigger: 'schedule', active: false },
    ])
  }, [])

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Automation Workflows</h2>
      <div className="bg-white rounded shadow overflow-hidden">
        <ul className="divide-y divide-gray-200">
            {workflows.map((wf) => (
                <li key={wf.id} className="p-4 flex justify-between items-center hover:bg-gray-50">
                    <div>
                        <p className="font-semibold text-gray-800">{wf.name}</p>
                        <p className="text-sm text-gray-500">Trigger: {wf.trigger}</p>
                    </div>
                    <div>
                        <span className={`px-2 py-1 text-xs font-bold rounded ${wf.active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                            {wf.active ? 'Active' : 'Inactive'}
                        </span>
                    </div>
                </li>
            ))}
        </ul>
      </div>
    </div>
  )
}
