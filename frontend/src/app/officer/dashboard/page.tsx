'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import axios from 'axios'

interface Application {
  id: number
  token_te2: string
  service_category: string
  status: string
  created_at: string
  files: any[]
}

export default function OfficerDashboardPage() {
  const router = useRouter()
  const [applications, setApplications] = useState<Application[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedApp, setSelectedApp] = useState<Application | null>(null)
  const [scrollY, setScrollY] = useState(0)

  useEffect(() => {
    fetchApplications()
    
    const handleScroll = () => {
      setScrollY(window.scrollY)
    }
    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const fetchApplications = async () => {
    const token = localStorage.getItem('authToken')
    if (!token) {
      router.push('/officer/login')
      return
    }

    try {
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL}/applications/officer/list/`,
        { headers: { Authorization: `Token ${token}` } }
      )
      setApplications(response.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleAction = async (appId: number, action: 'APPROVE' | 'REJECT') => {
    const token = localStorage.getItem('authToken')
    
    try {
      await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/applications/officer/action/${appId}/`,
        { action },
        { headers: { Authorization: `Token ${token}` } }
      )
      
      alert(`Application ${action.toLowerCase()}d successfully`)
      fetchApplications()
      setSelectedApp(null)
    } catch (err) {
      alert('Action failed')
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('authToken')
    localStorage.removeItem('userType')
    router.push('/officer/login')
  }

  if (loading) {
    return (
      <div className="container" style={{ paddingTop: '8rem' }}>
        <p style={{ textAlign: 'center' }}>Loading...</p>
      </div>
    )
  }

  return (
    <div 
      className="container" 
      style={{ 
        paddingTop: '8rem', 
        paddingBottom: '4rem',
        transform: `translateY(${scrollY * 0.08}px)`,
        transition: 'transform 0.1s linear'
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '3rem' }}>
        <h1 style={{ letterSpacing: '0.05em', fontWeight: 300 }}>OFFICER DASHBOARD</h1>
        <button onClick={handleLogout} className="btn">Logout</button>
      </div>

      <div className="card">
        <h2 style={{ marginTop: 0, marginBottom: '2rem', letterSpacing: '0.05em', fontWeight: 400, textTransform: 'uppercase' }}>
          Assigned Applications ({applications.length})
        </h2>
        
        {applications.length === 0 ? (
          <p style={{ marginTop: '1rem' }}>No applications assigned</p>
        ) : (
          <div style={{ display: 'grid', gap: '1rem' }}>
            {applications.map(app => (
              <div 
                key={app.id} 
                style={{ 
                  border: `1px solid ${selectedApp?.id === app.id ? 'var(--text-white)' : 'var(--border-dark)'}`, 
                  padding: '2rem', 
                  cursor: 'pointer',
                  background: selectedApp?.id === app.id ? 'var(--bg-black)' : 'var(--bg-darker)',
                  transition: 'all 0.3s'
                }}
                onClick={() => setSelectedApp(app)}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
                  <div style={{ flex: 1 }}>
                    <p style={{ marginBottom: '0.75rem' }}>
                      <span style={{ color: 'var(--text-gray)', fontSize: '0.875rem', letterSpacing: '0.05em', textTransform: 'uppercase' }}>Application ID: </span>
                      <span style={{ color: 'var(--text-white)', fontWeight: 400 }}>#{app.id}</span>
                    </p>
                    <p style={{ marginBottom: '0.75rem' }}>
                      <span style={{ color: 'var(--text-gray)', fontSize: '0.875rem', letterSpacing: '0.05em', textTransform: 'uppercase' }}>Category: </span>
                      <span style={{ color: 'var(--text-white)', fontWeight: 400 }}>{app.service_category}</span>
                    </p>
                    <p style={{ marginBottom: '0.75rem' }}>
                      <span style={{ color: 'var(--text-gray)', fontSize: '0.875rem', letterSpacing: '0.05em', textTransform: 'uppercase' }}>Status: </span>
                      <span style={{ color: 'var(--text-white)', fontWeight: 400 }}>{app.status}</span>
                    </p>
                    <p style={{ fontSize: '0.875rem', color: 'var(--text-gray)', margin: 0 }}>
                      Submitted: {new Date(app.created_at).toLocaleString()}
                    </p>
                  </div>
                  
                  {selectedApp?.id === app.id && (
                    <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
                      <button 
                        onClick={(e) => { e.stopPropagation(); handleAction(app.id, 'APPROVE') }}
                        className="btn btn-primary"
                      >
                        Approve
                      </button>
                      <button 
                        onClick={(e) => { e.stopPropagation(); handleAction(app.id, 'REJECT') }}
                        className="btn"
                      >
                        Reject
                      </button>
                    </div>
                  )}
                </div>
                
                {selectedApp?.id === app.id && app.files.length > 0 && (
                  <div style={{ marginTop: '1.5rem', paddingTop: '1.5rem', borderTop: '1px solid var(--border-dark)' }}>
                    <strong style={{ color: 'var(--text-white)', fontSize: '0.875rem', letterSpacing: '0.05em', textTransform: 'uppercase' }}>Documents:</strong>
                    <ul style={{ marginTop: '0.75rem', paddingLeft: '1.5rem', listStyle: 'none' }}>
                      {app.files.map(file => (
                        <li key={file.id} style={{ marginBottom: '0.5rem' }}>
                          <a 
                            href={file.file} 
                            target="_blank" 
                            rel="noopener noreferrer" 
                            style={{ 
                              color: 'var(--text-white)', 
                              textDecoration: 'none',
                              fontSize: '0.875rem',
                              borderBottom: '1px solid var(--text-white)',
                              paddingBottom: '2px'
                            }}
                          >
                            View Document {file.id} →
                          </a>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
