import React, { useEffect, useState } from 'react'

export const Finance = () => {
  const [invoices, setInvoices] = useState<any[]>([])

  useEffect(() => {
    // mock fetch
    setInvoices([
        { id: 1, customer: 'Acme Corp', amount: 1500, status: 'paid', due_date: '2023-11-01' },
        { id: 2, customer: 'Globex', amount: 3000, status: 'pending', due_date: '2023-11-15' },
    ])
  }, [])

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Finance - Invoices</h2>
      <div className="bg-white rounded shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Customer</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Due Date</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {invoices.map((inv) => (
              <tr key={inv.id}>
                <td className="px-6 py-4 whitespace-nowrap">{inv.customer}</td>
                <td className="px-6 py-4 whitespace-nowrap">${inv.amount}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                   <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${inv.status === 'paid' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                    {inv.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">{inv.due_date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
