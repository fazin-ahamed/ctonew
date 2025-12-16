import React, { useEffect } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Layout } from '@/components/Layout'
import { Dashboard } from '@/pages/Dashboard'
import { CRM } from '@/pages/CRM'
import { Login } from '@/pages/Login'
import { useAuthStore } from '@/stores/authStore'

function App() {
  const { session, loading, initialize } = useAuthStore()

  useEffect(() => {
    initialize()
  }, [initialize])

  if (loading) {
    return <div className="flex h-screen items-center justify-center">Loading...</div>
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={!session ? <Login /> : <Navigate to="/" />} />
        
        <Route element={session ? <Layout /> : <Navigate to="/login" />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/crm" element={<CRM />} />
          <Route path="/finance" element={<div>Finance Module</div>} />
          <Route path="/hrm" element={<div>HRM Module</div>} />
          <Route path="/projects" element={<div>Projects Module</div>} />
          <Route path="/automation" element={<div>Automation Module</div>} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
