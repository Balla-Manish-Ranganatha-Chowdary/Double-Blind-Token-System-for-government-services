'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import axios from 'axios'
import Link from 'next/link'

interface Officer {
  id: number
  username: string
  email: string
  department: string
  hierarchy_level: number
  workload_count: number
  is_active: boolean
}

export default function ManageOfficersPage() {
  const router = useRouter()
  const [officers, setOfficers] = useState<Officer[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    email: '',
    department: '',
    hierarchy_level: 1
  })

  useEffect(() => {
    fetchOfficers()
  }, [])

  const fetchOfficers = async () => {
    const token = localStorage.getItem('authToken')
    if (!token) {
      router.push('/admin/login')
      return
    }

    try {
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL}/officers/`,
        { headers: { Authorization: `Token ${token}` } }
      )
      setOfficers(response.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateOfficer = async (e: React.FormEvent) => {
    e.preventDefault()
    const token = localStorage.getItem('authToken')

    try {
      await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/officers/create/`,
        formData,
        { headers: { Authorization: `Token ${token}` } }
      )
      
      alert('Officer created successfully')
      setShowForm(false)
      setFormData({ username: '', password: '', email: '', department: '', hierarchy_level: 1 })
      fetchOfficers()
    } catch (err: any) {
      alert(err.response?.data?.error || 'Failed to create officer')
    }
  }

  const handleDeactivate = async (officerId: number) => {
    if (!confirm('Are you sure you want to deactivate this officer?')) return

    const token = localStorage.getItem('authToken')

    try {
      await axios.delete(
        `${process.env.NEXT_PUBLIC_API_URL}/officers/delete/${officerId}/`,
        { headers: { Authorization: `Token ${token}` } }
      )
      
      alert('Officer deactivated')
      fetchOfficers()
    } catch (err) {
      alert('Failed to deactivate officer')
    }
  }

  if (loading) {
    return <div className="container"><p>Loading...</p></div>
  }

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1>Manage Officers</h1>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <button onClick={() => setShowForm(!showForm)} className="btn btn-primary">
            {showForm ? 'Cancel' : 'Add Officer'}
          </button>
          <Link href="/admin/dashboard" className="btn btn-primary">
            Back to Dashboard
          </Link>
        </div>
      </div>

      {showForm && (
        <div className="card">
          <h2>Create New Officer</h2>
          <form onSubmit={handleCreateOfficer}>
            <div className="form-group">
              <label>Username</label>
              <input
                type="text"
                required
                value={formData.username}
                onChange={e => setFormData({...formData, username: e.target.value})}
              />
            </div>

            <div className="form-group">
              <label>Password</label>
              <input
                type="password"
                required
                value={formData.password}
                onChange={e => setFormData({...formData, password: e.target.value})}
              />
            </div>

            <div className="form-group">
              <label>Email (Optional)</label>
              <input
                type="email"
                value={formData.email}
                onChange={e => setFormData({...formData, email: e.target.value})}
              />
            </div>

            <div className="form-group">
              <label>Department</label>
              <select
                required
                value={formData.department}
                onChange={e => setFormData({...formData, department: e.target.value})}
                style={{ width: '100%', padding: '0.75rem', border: '1px solid #ddd', borderRadius: '4px' }}
              >
                <option value="">Select Department</option>
                <option value="Revenue">Revenue</option>
                <option value="Police">Police</option>
                <option value="Transport">Transport</option>
                <option value="Municipal">Municipal</option>
                <option value="Civil Supplies">Civil Supplies</option>
                <option value="Agriculture">Agriculture</option>
                <option value="General">General</option>
              </select>
            </div>

            <div className="form-group">
              <label>Hierarchy Level</label>
              <input
                type="number"
                min="1"
                max="10"
                required
                value={formData.hierarchy_level}
                onChange={e => setFormData({...formData, hierarchy_level: parseInt(e.target.value)})}
              />
            </div>

            <button type="submit" className="btn btn-primary">Create Officer</button>
          </form>
        </div>
      )}

      <div className="card">
        <h2>Officers List ({officers.length})</h2>
        
        <div style={{ marginTop: '1.5rem', overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #ddd' }}>
                <th style={{ textAlign: 'left', padding: '0.75rem' }}>Username</th>
                <th style={{ textAlign: 'left', padding: '0.75rem' }}>Email</th>
                <th style={{ textAlign: 'left', padding: '0.75rem' }}>Department</th>
                <th style={{ textAlign: 'center', padding: '0.75rem' }}>Level</th>
                <th style={{ textAlign: 'center', padding: '0.75rem' }}>Workload</th>
                <th style={{ textAlign: 'center', padding: '0.75rem' }}>Status</th>
                <th style={{ textAlign: 'center', padding: '0.75rem' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {officers.map(officer => (
                <tr key={officer.id} style={{ borderBottom: '1px solid #eee' }}>
                  <td style={{ padding: '0.75rem' }}>{officer.username}</td>
                  <td style={{ padding: '0.75rem' }}>{officer.email || '-'}</td>
                  <td style={{ padding: '0.75rem' }}>{officer.department}</td>
                  <td style={{ textAlign: 'center', padding: '0.75rem' }}>{officer.hierarchy_level}</td>
                  <td style={{ textAlign: 'center', padding: '0.75rem' }}>{officer.workload_count}</td>
                  <td style={{ textAlign: 'center', padding: '0.75rem' }}>
                    <span style={{ 
                      padding: '0.25rem 0.5rem', 
                      borderRadius: '4px', 
                      background: officer.is_active ? '#d4edda' : '#f8d7da',
                      color: officer.is_active ? '#155724' : '#721c24',
                      fontSize: '0.85rem'
                    }}>
                      {officer.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td style={{ textAlign: 'center', padding: '0.75rem' }}>
                    {officer.is_active && (
                      <button
                        onClick={() => handleDeactivate(officer.id)}
                        style={{ 
                          background: '#dc3545', 
                          color: 'white', 
                          padding: '0.25rem 0.75rem', 
                          border: 'none', 
                          borderRadius: '4px', 
                          cursor: 'pointer',
                          fontSize: '0.85rem'
                        }}
                      >
                        Deactivate
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
