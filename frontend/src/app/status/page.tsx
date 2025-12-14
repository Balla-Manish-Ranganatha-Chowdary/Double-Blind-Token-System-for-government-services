'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import Link from 'next/link'

export default function StatusPage() {
  const [token, setToken] = useState('')
  const [application, setApplication] = useState<any>(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [scrollY, setScrollY] = useState(0)

  useEffect(() => {
    const handleScroll = () => {
      setScrollY(window.scrollY)
    }
    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const checkStatus = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setApplication(null)

    try {
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL}/applications/status/${token}/`
      )
      setApplication(response.data)
    } catch (err: any) {
      setError(err.response?.data?.error || 'Application not found')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div 
      className="container" 
      style={{ 
        paddingTop: '8rem', 
        paddingBottom: '4rem',
        transform: `translateY(${scrollY * 0.1}px)`,
        transition: 'transform 0.1s linear'
      }}
    >
      <div className="card" style={{ maxWidth: '800px', margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
          <div style={{ 
            width: '80px',
            height: '80px',
            border: '1px solid var(--text-white)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 2rem'
          }}>
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="1">
              <circle cx="11" cy="11" r="8"/>
              <path d="m21 21-4.35-4.35"/>
            </svg>
          </div>
          <h1 style={{ marginBottom: '1rem', letterSpacing: '0.05em', fontWeight: 300 }}>CHECK APPLICATION STATUS</h1>
          <p style={{ fontSize: '1rem' }}>
            Enter your tracking token to view application status
          </p>
        </div>
        
        <form onSubmit={checkStatus}>
          <div className="form-group">
            <label>Tracking Token</label>
            <input
              type="text"
              required
              value={token}
              onChange={e => setToken(e.target.value)}
              placeholder="Paste your token here"
              style={{ fontFamily: 'monospace' }}
            />
            <small style={{ color: 'var(--text-gray)', fontSize: '0.875rem', display: 'block', marginTop: '0.5rem' }}>
              Enter the token you received after submitting your application
            </small>
          </div>

          <button 
            type="submit" 
            className="btn btn-primary" 
            disabled={loading}
            style={{ width: '100%', padding: '1.25rem' }}
          >
            {loading ? (
              <>
                <span className="loading" style={{ marginRight: '0.5rem' }}></span>
                Checking...
              </>
            ) : (
              'Check Status'
            )}
          </button>
        </form>

        {error && (
          <div className="alert alert-error" style={{ marginTop: '1.5rem' }}>
            <strong>ERROR:</strong> {error}
          </div>
        )}

        {application && (
          <div style={{ marginTop: '2rem' }}>
            <div style={{
              background: 'var(--bg-darker)',
              padding: '2.5rem',
              border: '1px solid var(--border-dark)',
              marginBottom: '2rem'
            }}>
              <div style={{ marginBottom: '2rem' }}>
                <h2 style={{ margin: 0, marginBottom: '0.5rem', letterSpacing: '0.05em', fontWeight: 300 }}>APPLICATION #{application.id}</h2>
                <p style={{ margin: 0, fontSize: '0.875rem', textTransform: 'uppercase', letterSpacing: '0.1em' }}>
                  Current Status
                </p>
              </div>
              
              <div style={{
                background: 'var(--bg-black)',
                padding: '1.5rem',
                border: '1px solid var(--border-dark)'
              }}>
                <div style={{ 
                  fontSize: '1.25rem', 
                  fontWeight: 400,
                  marginBottom: '0.5rem',
                  letterSpacing: '0.05em',
                  textTransform: 'uppercase'
                }}>
                  {application.status.replace(/_/g, ' ')}
                </div>
                <div style={{ fontSize: '0.875rem', color: 'var(--text-gray)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  {application.service_category ? `Service: ${application.service_category.replace(/_/g, ' ')}` : 'Processing...'}
                </div>
              </div>
            </div>

            <div className="card" style={{ marginBottom: '2rem' }}>
              <h3 style={{ marginTop: 0, marginBottom: '2rem', letterSpacing: '0.05em', fontWeight: 400, textTransform: 'uppercase' }}>Application Details</h3>
              
              <div style={{ display: 'grid', gap: '1rem' }}>
                <div style={{ 
                  display: 'flex', 
                  justifyContent: 'space-between',
                  padding: '1.5rem',
                  background: 'var(--bg-black)',
                  border: '1px solid var(--border-dark)'
                }}>
                  <span style={{ fontWeight: 400, color: 'var(--text-gray)', fontSize: '0.875rem', letterSpacing: '0.05em', textTransform: 'uppercase' }}>Application ID</span>
                  <span style={{ fontWeight: 400, color: 'var(--text-white)' }}>#{application.id}</span>
                </div>

                <div style={{ 
                  display: 'flex', 
                  justifyContent: 'space-between',
                  padding: '1.5rem',
                  background: 'var(--bg-black)',
                  border: '1px solid var(--border-dark)'
                }}>
                  <span style={{ fontWeight: 400, color: 'var(--text-gray)', fontSize: '0.875rem', letterSpacing: '0.05em', textTransform: 'uppercase' }}>Service Category</span>
                  <span style={{ fontWeight: 400, color: 'var(--text-white)' }}>
                    {application.service_category ? application.service_category.replace(/_/g, ' ') : 'Processing...'}
                  </span>
                </div>

                <div style={{ 
                  display: 'flex', 
                  justifyContent: 'space-between',
                  padding: '1.5rem',
                  background: 'var(--bg-black)',
                  border: '1px solid var(--border-dark)'
                }}>
                  <span style={{ fontWeight: 400, color: 'var(--text-gray)', fontSize: '0.875rem', letterSpacing: '0.05em', textTransform: 'uppercase' }}>Submitted On</span>
                  <span style={{ fontWeight: 400, color: 'var(--text-white)' }}>
                    {new Date(application.created_at).toLocaleDateString('en-IN', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                  </span>
                </div>

                {application.files && application.files.length > 0 && (
                  <div style={{ 
                    padding: '1.5rem',
                    background: 'var(--bg-black)',
                    border: '1px solid var(--border-dark)'
                  }}>
                    <span style={{ fontWeight: 400, color: 'var(--text-gray)', display: 'block', marginBottom: '0.5rem', fontSize: '0.875rem', letterSpacing: '0.05em', textTransform: 'uppercase' }}>
                      Uploaded Documents
                    </span>
                    <div style={{ fontSize: '0.875rem', color: 'var(--text-white)' }}>
                      {application.files.length} file(s) attached
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Status Timeline */}
            <div className="card">
              <h3 style={{ marginTop: 0, marginBottom: '2rem', letterSpacing: '0.05em', fontWeight: 400, textTransform: 'uppercase' }}>Application Timeline</h3>
              <div>
                {['SUBMITTED', 'CLASSIFIED', 'REDACTION_CLEARED', 'ASSIGNED', 'IN_REVIEW', 'APPROVED'].map((status, idx) => {
                  const isCompleted = ['SUBMITTED', 'CLASSIFIED', 'REDACTION_CLEARED', 'ASSIGNED'].includes(status)
                  const isCurrent = application.status === status
                  
                  return (
                    <div key={status} style={{ display: 'flex', gap: '1.5rem', marginBottom: '1.5rem' }}>
                      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                        <div style={{
                          width: '40px',
                          height: '40px',
                          border: `1px solid ${isCurrent || isCompleted ? 'var(--text-white)' : 'var(--border-dark)'}`,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          color: isCurrent || isCompleted ? 'var(--text-white)' : 'var(--text-gray)',
                          fontWeight: 300,
                          fontSize: '0.875rem',
                          transition: 'all 0.3s'
                        }}>
                          {isCompleted || isCurrent ? '✓' : idx + 1}
                        </div>
                        {idx < 5 && (
                          <div style={{
                            width: '1px',
                            height: '30px',
                            background: isCompleted ? 'var(--text-white)' : 'var(--border-dark)',
                            transition: 'all 0.3s'
                          }} />
                        )}
                      </div>
                      <div style={{ flex: 1, paddingTop: '0.5rem' }}>
                        <div style={{ 
                          fontWeight: 400,
                          color: isCurrent || isCompleted ? 'var(--text-white)' : 'var(--text-gray)',
                          fontSize: '0.875rem',
                          letterSpacing: '0.05em',
                          textTransform: 'uppercase'
                        }}>
                          {status.replace(/_/g, ' ')}
                        </div>
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          </div>
        )}

        <div style={{ marginTop: '2rem', textAlign: 'center' }}>
          <Link href="/" style={{ color: 'var(--text-white)', textDecoration: 'none', fontWeight: 400, letterSpacing: '0.05em', fontSize: '0.875rem' }}>
            ← BACK TO HOME
          </Link>
        </div>
      </div>
    </div>
  )
}
