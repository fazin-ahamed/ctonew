import React, { useEffect, useState } from 'react'

export const HRM = () => {
  const [employees, setEmployees] = useState<any[]>([])

  useEffect(() => {
    // mock fetch
    setEmployees([
        { id: 1, name: 'John Doe', position: 'Software Engineer', department: 'Engineering' },
        { id: 2, name: 'Jane Smith', position: 'HR Manager', department: 'HR' },
    ])
  }, [])

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">HRM - Employees</h2>
      <div className="bg-white rounded shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Position</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Department</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {employees.map((emp) => (
              <tr key={emp.id}>
                <td className="px-6 py-4 whitespace-nowrap">{emp.name}</td>
                <td className="px-6 py-4 whitespace-nowrap">{emp.position}</td>
                <td className="px-6 py-4 whitespace-nowrap">{emp.department}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
