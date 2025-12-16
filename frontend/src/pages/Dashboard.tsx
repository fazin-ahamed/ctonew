import React from 'react'

export const Dashboard = () => {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Dashboard</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 bg-white rounded shadow">
          <h3 className="text-lg font-semibold text-gray-700">Total Revenue</h3>
          <p className="text-3xl font-bold mt-2">$124,500</p>
        </div>
        <div className="p-6 bg-white rounded shadow">
          <h3 className="text-lg font-semibold text-gray-700">Active Deals</h3>
          <p className="text-3xl font-bold mt-2">45</p>
        </div>
        <div className="p-6 bg-white rounded shadow">
          <h3 className="text-lg font-semibold text-gray-700">Employees</h3>
          <p className="text-3xl font-bold mt-2">12</p>
        </div>
      </div>
    </div>
  )
}
