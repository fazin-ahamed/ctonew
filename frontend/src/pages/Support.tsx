import React, { useEffect, useState } from 'react'

export const Support = () => {
  const [tickets, setTickets] = useState<any[]>([])

  useEffect(() => {
    // mock fetch
    setTickets([
        { id: 1, subject: 'Login issue', status: 'open', priority: 'high' },
        { id: 2, subject: 'Feature request', status: 'closed', priority: 'low' },
    ])
  }, [])

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Support Tickets</h2>
      <div className="bg-white rounded shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Subject</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Priority</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {tickets.map((t) => (
              <tr key={t.id}>
                <td className="px-6 py-4 whitespace-nowrap">{t.subject}</td>
                <td className="px-6 py-4 whitespace-nowrap">{t.status}</td>
                <td className="px-6 py-4 whitespace-nowrap">{t.priority}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
