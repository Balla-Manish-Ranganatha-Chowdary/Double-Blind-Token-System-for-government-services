'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import Link from 'next/link'

export default function ApplyPage() {
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    address: '',
    aadhaar: ''
  })
  const [files, setFiles] = useState<FileList | null>(null)
  const [token, setToken] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [copied, setCopied] = useState(false)
  const [scrollY, setScrollY] = useState(0)

  useEffect(() => {
    const handleScroll = () => {
      setScrollY(window.scrollY)
    }
    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    const data = new FormData()
    data.append('name', formData.name)
    data.append('age', formData.age)
    data.append('address', formData.address)
    data.append('aadhaar', formData.aadhaar)
    
    if (files) {
      Array.from(files).forEach(file => {
        data.append('files', file)
      })
    }

    try {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/applications/submit/`,
        data,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      )
      setToken(response.data.token)
    } catch (err: any) {
      setError(err.response?.data?.error || 'Submission failed')
    } finally {
      setLoading(false)
    }
  }

  const copyToken = () => {
    navigator.clipboard.writeText(token)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  if (token) {
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
              width: '100px',
              height: '100px',
              border: '1px solid var(--text-white)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '0 auto 2rem'
            }}>
              <svg width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="1">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
            </div>
            <h1 style={{ marginBottom: '1rem', letterSpacing: '0.05em', fontWeight: 300 }}>APPLICATION SUBMITTED</h1>
            <p style={{ fontSize: '1rem' }}>
              Your application has been submitted and is being processed
            </p>
          </div>

          <div style={{ 
            background: 'var(--bg-darker)',
            padding: '2.5rem',
            marginBottom: '2rem',
            border: '1px solid var(--border-dark)'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
              <span style={{ fontSize: '0.875rem', fontWeight: 400, letterSpacing: '0.1em', textTransform: 'uppercase' }}>
                Tracking Token
              </span>
              <button
                onClick={copyToken}
                style={{
                  background: 'transparent',
                  border: '1px solid var(--text-white)',
                  padding: '0.75rem 1.5rem',
                  color: 'white',
                  cursor: 'pointer',
                  transition: 'all 0.3s',
                  fontWeight: 400,
                  fontSize: '0.75rem',
                  letterSpacing: '0.1em',
                  textTransform: 'uppercase'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = 'var(--text-white)'
                  e.currentTarget.style.color = 'var(--bg-black)'
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = 'transparent'
                  e.currentTarget.style.color = 'white'
                }}
              >
                {copied ? 'COPIED' : 'COPY'}
              </button>
            </div>
            <div style={{ 
              background: 'var(--bg-black)',
              padding: '1.5rem',
              wordBreak: 'break-all',
              fontFamily: 'monospace',
              fontSize: '1rem',
              border: '1px solid var(--border-dark)',
              color: 'var(--text-white)'
            }}>
              {token}
            </div>
          </div>

          <div className="alert alert-info" style={{ marginBottom: '2rem' }}>
            <strong>IMPORTANT:</strong> Save this token securely. You will need it to track your application status.
          </div>

          <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
            <Link href="/status" className="btn btn-primary" style={{ flex: 1 }}>
              Check Status
            </Link>
            <Link href="/" className="btn" style={{ flex: 1 }}>
              Back to Home
            </Link>
          </div>
        </div>
      </div>
    )
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
      <div className="card" style={{ maxWidth: '900px', margin: '0 auto' }}>
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
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
              <line x1="16" y1="13" x2="8" y2="13"/>
              <line x1="16" y1="17" x2="8" y2="17"/>
            </svg>
          </div>
          <h1 style={{ marginBottom: '1rem', letterSpacing: '0.05em', fontWeight: 300 }}>APPLY FOR SERVICE</h1>
          <p style={{ fontSize: '1rem' }}>
            Fill in your details to submit an application
          </p>
        </div>

        <div className="alert alert-info" style={{ marginBottom: '2rem' }}>
          <strong>IMPORTANT NOTICE:</strong> Ensure your uploaded documents do NOT contain personal identifiers (name, Aadhaar, phone numbers). 
          Applications with personal information will be automatically rejected.
        </div>
        
        {error && (
          <div className="alert alert-error">
            <strong>ERROR:</strong> {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Full Name</label>
            <input
              type="text"
              required
              placeholder="Enter your full name"
              value={formData.name}
              onChange={e => setFormData({...formData, name: e.target.value})}
            />
          </div>

          <div className="form-group">
            <label>Age</label>
            <input
              type="number"
              required
              min="18"
              max="100"
              placeholder="Enter your age"
              value={formData.age}
              onChange={e => setFormData({...formData, age: e.target.value})}
            />
          </div>

          <div className="form-group">
            <label>Address</label>
            <textarea
              required
              rows={3}
              placeholder="Enter your complete address"
              value={formData.address}
              onChange={e => setFormData({...formData, address: e.target.value})}
            />
          </div>

          <div className="form-group">
            <label>Aadhaar Number</label>
            <input
              type="text"
              required
              maxLength={12}
              pattern="[0-9]{12}"
              placeholder="Enter 12-digit Aadhaar number"
              value={formData.aadhaar}
              onChange={e => setFormData({...formData, aadhaar: e.target.value.replace(/\D/g, '')})}
            />
            <small style={{ color: '#64748b', fontSize: '0.875rem', display: 'block', marginTop: '0.5rem' }}>
              Enter 12 digits without spaces
            </small>
          </div>

          <div className="form-group">
            <label>Upload Documents (PDF)</label>
            <div style={{
              border: '1px solid var(--border-dark)',
              padding: '2.5rem',
              textAlign: 'center',
              background: 'var(--bg-black)',
              transition: 'all 0.3s',
              cursor: 'pointer'
            }}
            onDragOver={(e) => {
              e.preventDefault()
              e.currentTarget.style.borderColor = 'var(--text-white)'
            }}
            onDragLeave={(e) => {
              e.currentTarget.style.borderColor = 'var(--border-dark)'
            }}
            >
              <div style={{ 
                width: '64px',
                height: '64px',
                border: '1px solid var(--text-white)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 1.5rem'
              }}>
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="1">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                  <polyline points="17 8 12 3 7 8"/>
                  <line x1="12" y1="3" x2="12" y2="15"/>
                </svg>
              </div>
              <input
                type="file"
                accept=".pdf"
                multiple
                required
                onChange={e => setFiles(e.target.files)}
                style={{ display: 'none' }}
                id="file-upload"
              />
              <label htmlFor="file-upload" style={{ cursor: 'pointer' }}>
                <span style={{ color: 'var(--text-white)', fontWeight: 400, letterSpacing: '0.05em', textTransform: 'uppercase', fontSize: '0.875rem' }}>Click to upload</span>
                <span style={{ color: 'var(--text-gray)' }}> or drag and drop</span>
              </label>
              <p style={{ fontSize: '0.875rem', color: 'var(--text-gray)', marginTop: '0.75rem' }}>
                PDF FILES ONLY • MULTIPLE FILES ALLOWED
              </p>
              {files && (
                <div style={{ marginTop: '1.5rem', textAlign: 'left', background: 'var(--bg-darker)', padding: '1.5rem', border: '1px solid var(--border-dark)' }}>
                  <strong style={{ color: 'var(--text-white)', fontSize: '0.875rem', letterSpacing: '0.05em', textTransform: 'uppercase' }}>Selected files:</strong>
                  <ul style={{ marginTop: '0.75rem', paddingLeft: '1.5rem', listStyle: 'none' }}>
                    {Array.from(files).map((file, idx) => (
                      <li key={idx} style={{ color: 'var(--text-gray)', marginBottom: '0.5rem', fontSize: '0.875rem' }}>
                        {file.name}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
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
                Processing...
              </>
            ) : (
              'Submit Application'
            )}
          </button>
        </form>

        <div style={{ marginTop: '2rem', textAlign: 'center' }}>
          <Link href="/" style={{ color: 'var(--text-white)', textDecoration: 'none', fontWeight: 400, letterSpacing: '0.05em', fontSize: '0.875rem' }}>
            ← BACK TO HOME
          </Link>
        </div>
      </div>
    </div>
  )
}
