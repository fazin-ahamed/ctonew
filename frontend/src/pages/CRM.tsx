import React, { useEffect, useState } from 'react'

export const CRM = () => {
  const [leads, setLeads] = useState<any[]>([])

  // Mock fetch for now, or use React Query with API client
  useEffect(() => {
    // fetch('/api/v1/crm/leads').then(res => res.json()).then(data => setLeads(data))
    setLeads([
        { id: 1, name: 'Acme Corp', status: 'New', value: '$10,000' },
        { id: 2, name: 'Globex', status: 'Qualified', value: '$5,000' },
    ])
  }, [])

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">CRM - Leads</h2>
      <div className="bg-white rounded shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Value</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {leads.map((lead) => (
              <tr key={lead.id}>
                <td className="px-6 py-4 whitespace-nowrap">{lead.name}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                    {lead.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">{lead.value}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
