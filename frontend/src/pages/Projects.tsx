import React, { useEffect, useState } from 'react'

export const Projects = () => {
  const [projects, setProjects] = useState<any[]>([])

  useEffect(() => {
    // mock fetch
    setProjects([
        { id: 1, name: 'Website Redesign', status: 'active' },
        { id: 2, name: 'Mobile App Launch', status: 'planning' },
    ])
  }, [])

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Projects</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {projects.map((proj) => (
            <div key={proj.id} className="p-4 bg-white rounded shadow border border-gray-200">
                <h3 className="text-lg font-bold">{proj.name}</h3>
                <span className="text-sm text-gray-500 capitalize">{proj.status}</span>
            </div>
        ))}
      </div>
    </div>
  )
}
