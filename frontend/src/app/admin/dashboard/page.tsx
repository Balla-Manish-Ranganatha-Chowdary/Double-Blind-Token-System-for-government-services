'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import axios from 'axios'
import Link from 'next/link'

interface Analytics {
  total_applications: number
  approval_rate: number
  rejection_rate: number
  recent_applications: number
  status_breakdown: any[]
  category_breakdown: any[]
  officer_workload: any[]
  department_breakdown: any[]
}

export default function AdminDashboardPage() {
  const router = useRouter()
  const [analytics, setAnalytics] = useState<Analytics | null>(null)
  const [loading, setLoading] = useState(true)
  const [scrollY, setScrollY] = useState(0)

  useEffect(() => {
    fetchAnalytics()
    
    const handleScroll = () => {
      setScrollY(window.scrollY)
    }
    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const fetchAnalytics = async () => {
    const token = localStorage.getItem('authToken')
    if (!token) {
      router.push('/admin/login')
      return
    }

    try {
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL}/analytics/dashboard/`,
        { headers: { Authorization: `Token ${token}` } }
      )
      setAnalytics(response.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('authToken')
    localStorage.removeItem('userType')
    router.push('/admin/login')
  }

  if (loading) {
    return (
      <div className="container" style={{ paddingTop: '8rem' }}>
        <p style={{ textAlign: 'center' }}>Loading...</p>
      </div>
    )
  }

  if (!analytics) {
    return (
      <div className="container" style={{ paddingTop: '8rem' }}>
        <p style={{ textAlign: 'center' }}>Failed to load analytics</p>
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
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '3rem', flexWrap: 'wrap', gap: '1rem' }}>
        <h1 style={{ letterSpacing: '0.05em', fontWeight: 300 }}>ADMIN DASHBOARD</h1>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          <Link href="/admin/officers" className="btn btn-primary">
            Manage Officers
          </Link>
          <button onClick={handleLogout} className="btn">Logout</button>
        </div>
      </div>

      {/* Summary Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
        <div className="card" style={{ textAlign: 'center' }}>
          <h3 style={{ fontSize: '2.5rem', color: 'var(--text-white)', margin: '0', fontWeight: 200 }}>{analytics.total_applications}</h3>
          <p style={{ marginTop: '0.75rem', fontSize: '0.875rem', letterSpacing: '0.05em', textTransform: 'uppercase' }}>Total Applications</p>
        </div>
        
        <div className="card" style={{ textAlign: 'center' }}>
          <h3 style={{ fontSize: '2.5rem', color: 'var(--text-white)', margin: '0', fontWeight: 200 }}>{analytics.approval_rate}%</h3>
          <p style={{ marginTop: '0.75rem', fontSize: '0.875rem', letterSpacing: '0.05em', textTransform: 'uppercase' }}>Approval Rate</p>
        </div>
        
        <div className="card" style={{ textAlign: 'center' }}>
          <h3 style={{ fontSize: '2.5rem', color: 'var(--text-white)', margin: '0', fontWeight: 200 }}>{analytics.rejection_rate}%</h3>
          <p style={{ marginTop: '0.75rem', fontSize: '0.875rem', letterSpacing: '0.05em', textTransform: 'uppercase' }}>Rejection Rate</p>
        </div>
        
        <div className="card" style={{ textAlign: 'center' }}>
          <h3 style={{ fontSize: '2.5rem', color: 'var(--text-white)', margin: '0', fontWeight: 200 }}>{analytics.recent_applications}</h3>
          <p style={{ marginTop: '0.75rem', fontSize: '0.875rem', letterSpacing: '0.05em', textTransform: 'uppercase' }}>Last 7 Days</p>
        </div>
      </div>

      {/* Status Breakdown */}
      <div className="card" style={{ marginBottom: '2rem' }}>
        <h2 style={{ marginTop: 0, marginBottom: '2rem', letterSpacing: '0.05em', fontWeight: 400, textTransform: 'uppercase' }}>Application Status</h2>
        <div>
          {analytics.status_breakdown.map((item, idx) => (
            <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', padding: '1rem 0', borderBottom: `1px solid var(--border-dark)` }}>
              <span style={{ fontSize: '0.875rem', letterSpacing: '0.05em', textTransform: 'uppercase', color: 'var(--text-gray)' }}>{item.status}</span>
              <strong style={{ color: 'var(--text-white)', fontWeight: 400 }}>{item.count}</strong>
            </div>
          ))}
        </div>
      </div>

      {/* Service Categories */}
      <div className="card" style={{ marginBottom: '2rem' }}>
        <h2 style={{ marginTop: 0, marginBottom: '2rem', letterSpacing: '0.05em', fontWeight: 400, textTransform: 'uppercase' }}>Service Categories</h2>
        <div>
          {analytics.category_breakdown.map((item, idx) => (
            <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', padding: '1rem 0', borderBottom: `1px solid var(--border-dark)` }}>
              <span style={{ fontSize: '0.875rem', letterSpacing: '0.05em', textTransform: 'uppercase', color: 'var(--text-gray)' }}>{item.service_category || 'Uncategorized'}</span>
              <strong style={{ color: 'var(--text-white)', fontWeight: 400 }}>{item.count}</strong>
            </div>
          ))}
        </div>
      </div>

      {/* Officer Workload */}
      <div className="card">
        <h2 style={{ marginTop: 0, marginBottom: '2rem', letterSpacing: '0.05em', fontWeight: 400, textTransform: 'uppercase' }}>Officer Workload</h2>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: `1px solid var(--border-dark)` }}>
                <th style={{ textAlign: 'left', padding: '1rem 0.5rem', fontSize: '0.875rem', letterSpacing: '0.05em', textTransform: 'uppercase', color: 'var(--text-gray)', fontWeight: 400 }}>Officer</th>
                <th style={{ textAlign: 'left', padding: '1rem 0.5rem', fontSize: '0.875rem', letterSpacing: '0.05em', textTransform: 'uppercase', color: 'var(--text-gray)', fontWeight: 400 }}>Department</th>
                <th style={{ textAlign: 'center', padding: '1rem 0.5rem', fontSize: '0.875rem', letterSpacing: '0.05em', textTransform: 'uppercase', color: 'var(--text-gray)', fontWeight: 400 }}>Level</th>
                <th style={{ textAlign: 'center', padding: '1rem 0.5rem', fontSize: '0.875rem', letterSpacing: '0.05em', textTransform: 'uppercase', color: 'var(--text-gray)', fontWeight: 400 }}>Workload</th>
              </tr>
            </thead>
            <tbody>
              {analytics.officer_workload.map((officer, idx) => (
                <tr key={idx} style={{ borderBottom: `1px solid var(--border-dark)` }}>
                  <td style={{ padding: '1rem 0.5rem', color: 'var(--text-white)' }}>{officer.user__username}</td>
                  <td style={{ padding: '1rem 0.5rem', color: 'var(--text-white)' }}>{officer.department}</td>
                  <td style={{ textAlign: 'center', padding: '1rem 0.5rem', color: 'var(--text-white)' }}>{officer.hierarchy_level}</td>
                  <td style={{ textAlign: 'center', padding: '1rem 0.5rem', color: 'var(--text-white)' }}>{officer.workload_count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
