import React from 'react'
import { Outlet, Link } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'

export const Layout = () => {
  const { signOut } = useAuthStore()
  
  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-gray-200 hidden md:block">
        <div className="p-6">
          <h1 className="text-xl font-bold text-gray-800">Business OS</h1>
        </div>
        <nav className="mt-6 px-4 space-y-2">
          <Link to="/" className="block py-2 px-4 text-gray-700 hover:bg-gray-100 rounded">Dashboard</Link>
          <Link to="/crm" className="block py-2 px-4 text-gray-700 hover:bg-gray-100 rounded">CRM</Link>
          <Link to="/finance" className="block py-2 px-4 text-gray-700 hover:bg-gray-100 rounded">Finance</Link>
          <Link to="/hrm" className="block py-2 px-4 text-gray-700 hover:bg-gray-100 rounded">HRM</Link>
          <Link to="/projects" className="block py-2 px-4 text-gray-700 hover:bg-gray-100 rounded">Projects</Link>
          <Link to="/support" className="block py-2 px-4 text-gray-700 hover:bg-gray-100 rounded">Support</Link>
          <Link to="/automation" className="block py-2 px-4 text-gray-700 hover:bg-gray-100 rounded">Automation</Link>
        </nav>
        <div className="absolute bottom-0 w-64 p-4 border-t">
          <button onClick={signOut} className="w-full py-2 px-4 text-sm text-red-600 hover:bg-red-50 rounded">
            Sign Out
          </button>
        </div>
      </aside>
      
      {/* Main Content */}
      <main className="flex-1 overflow-y-auto p-8">
        <Outlet />
      </main>
    </div>
  )
}
