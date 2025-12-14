'use client'

import Link from 'next/link'
import { useEffect, useState, useRef } from 'react'

export default function Home() {
  const [isVisible, setIsVisible] = useState<{ [key: string]: boolean }>({})
  const observerRef = useRef<IntersectionObserver | null>(null)

  useEffect(() => {
    // Simple Intersection Observer for fade-in animations
    observerRef.current = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsVisible((prev) => ({ ...prev, [entry.target.id]: true }))
          }
        })
      },
      { threshold: 0.1 }
    )

    // Observe all sections
    document.querySelectorAll('section[id]').forEach((el) => {
      if (observerRef.current) observerRef.current.observe(el)
    })
    
    return () => {
      if (observerRef.current) observerRef.current.disconnect()
    }
  }, [])

  return (
    <main style={{ paddingTop: '5rem' }}>
      {/* Hero Section */}
      <section className="hero" id="hero">
        <div className="container">
          <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
            <h1 style={{ marginBottom: '2rem', letterSpacing: '0.05em' }}>
              GOVERNMENT SERVICES PORTAL
            </h1>
            <p style={{ fontSize: '1.125rem', marginBottom: '3rem', color: '#a0a0a0', maxWidth: '800px', margin: '0 auto 3rem' }}>
              Secure, transparent, and corruption-free service delivery powered by double-blind token encryption technology
            </p>
            <div style={{ display: 'flex', gap: '1.5rem', justifyContent: 'center', flexWrap: 'wrap' }}>
              <Link href="/apply" className="btn btn-primary">
                Apply for Service
              </Link>
              <Link href="/status" className="btn">
                Check Status
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section 
        className="section" 
        id="features"
        style={{
          opacity: isVisible['features'] ? 1 : 0,
          transform: isVisible['features'] ? 'translateY(0)' : 'translateY(30px)',
          transition: 'opacity 0.8s ease-out, transform 0.8s ease-out'
        }}
      >
        <div className="container">
          <div className="grid grid-3">
            {[
              {
                title: 'DOUBLE-BLIND SECURITY',
                description: 'Complete anonymity between citizens and officers through military-grade two-layer encryption',
                icon: (
                  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                  </svg>
                )
              },
              {
                title: 'AI-POWERED PROCESSING',
                description: 'Intelligent classification and automated PII detection for enhanced security and efficiency',
                icon: (
                  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M12 16v-4M12 8h.01"/>
                  </svg>
                )
              },
              {
                title: 'FAIR ASSIGNMENT',
                description: 'Workload-based routing ensures efficient, unbiased, and transparent processing',
                icon: (
                  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1">
                    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
                  </svg>
                )
              }
            ].map((feature, idx) => (
              <div key={idx} className="feature-card">
                <div className="icon-box">
                  {feature.icon}
                </div>
                <h3 style={{ marginBottom: '1rem', letterSpacing: '0.05em' }}>{feature.title}</h3>
                <p style={{ fontSize: '0.9375rem' }}>{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* About Section */}
      <section 
        className="section"
        id="about"
        style={{
          opacity: isVisible['about'] ? 1 : 0,
          transform: isVisible['about'] ? 'translateY(0)' : 'translateY(30px)',
          transition: 'opacity 0.8s ease-out, transform 0.8s ease-out'
        }}
      >
        <div className="container">
          <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
            <h2 style={{ marginBottom: '3rem', textAlign: 'center', letterSpacing: '0.05em' }}>ABOUT THE PLATFORM</h2>
            <div style={{ 
              background: '#0a0a0a',
              padding: '3rem',
              border: '1px solid #2a2a2a'
            }}>
              <p style={{ marginBottom: '2rem', fontSize: '1.0625rem', lineHeight: '1.9' }}>
                This platform eliminates corruption in government service delivery through a revolutionary double-blind token system. 
                When you submit an application, your identity is encrypted using two layers of military-grade encryption. Officers reviewing your 
                application cannot see who you are, and you don't know which officer is handling your case.
              </p>
              <p style={{ fontSize: '1.0625rem', lineHeight: '1.9' }}>
                AI agents automatically classify your application, check for personal information in documents, and assign it to 
                officers based on workload and hierarchy. The system ensures fair, transparent, and efficient service delivery.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section 
        className="section"
        id="how-it-works"
        style={{
          opacity: isVisible['how-it-works'] ? 1 : 0,
          transform: isVisible['how-it-works'] ? 'translateY(0)' : 'translateY(30px)',
          transition: 'opacity 0.8s ease-out, transform 0.8s ease-out'
        }}
      >
        <div className="container">
          <h2 style={{ marginBottom: '4rem', textAlign: 'center', letterSpacing: '0.05em' }}>HOW IT WORKS</h2>
          <div style={{ maxWidth: '900px', margin: '0 auto', display: 'grid', gap: '2rem' }}>
            {[
              { title: 'SUBMIT APPLICATION', desc: 'Submit your application with required documents ensuring no personal identifiers are in PDFs' },
              { title: 'RECEIVE TOKEN', desc: 'Receive a secure encrypted token to track your application throughout the process' },
              { title: 'AI CLASSIFICATION', desc: 'AI automatically classifies service type and checks for identity information' },
              { title: 'OFFICER ASSIGNMENT', desc: 'Application is assigned to appropriate officer based on workload and hierarchy' },
              { title: 'ANONYMOUS REVIEW', desc: 'Officers review anonymously without knowing your identity' },
              { title: 'MULTI-LEVEL APPROVAL', desc: 'Multi-level approvals happen automatically if required' },
              { title: 'TRACK STATUS', desc: 'Track status anytime using your secure token' }
            ].map((step, idx) => (
              <div 
                key={idx}
                style={{
                  display: 'flex',
                  gap: '2rem',
                  padding: '2rem',
                  background: '#0a0a0a',
                  border: '1px solid #2a2a2a',
                  transition: 'all 0.3s'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'translateX(12px)'
                  e.currentTarget.style.borderColor = '#a0a0a0'
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'translateX(0)'
                  e.currentTarget.style.borderColor = '#2a2a2a'
                }}
              >
                <div style={{
                  minWidth: '60px',
                  width: '60px',
                  height: '60px',
                  border: '1px solid #ffffff',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: '#ffffff',
                  fontWeight: 300,
                  fontSize: '1.5rem',
                  flexShrink: 0
                }}>
                  {idx + 1}
                </div>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <h4 style={{ marginBottom: '0.75rem', fontSize: '1rem', letterSpacing: '0.1em', fontWeight: 400, marginTop: 0 }}>{step.title}</h4>
                  <p style={{ margin: 0, fontSize: '0.9375rem' }}>{step.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Portal Access */}
      <section 
        className="section"
        id="portals"
        style={{
          opacity: isVisible['portals'] ? 1 : 0,
          transform: isVisible['portals'] ? 'translateY(0)' : 'translateY(30px)',
          transition: 'opacity 0.8s ease-out, transform 0.8s ease-out'
        }}
      >
        <div className="container">
          <h2 style={{ marginBottom: '4rem', textAlign: 'center', letterSpacing: '0.05em' }}>PORTAL ACCESS</h2>
          <div className="grid grid-3">
            {[
              {
                href: '/apply',
                title: 'CITIZENS',
                desc: 'Apply for services and track applications',
                icon: (
                  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                  </svg>
                )
              },
              {
                href: '/officer/login',
                title: 'OFFICERS',
                desc: 'Review and process applications',
                icon: (
                  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                    <circle cx="9" cy="7" r="4"/>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                  </svg>
                )
              },
              {
                href: '/admin/login',
                title: 'ADMINISTRATORS',
                desc: 'Manage system and officers',
                icon: (
                  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1">
                    <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
                  </svg>
                )
              }
            ].map((portal, idx) => (
              <Link key={idx} href={portal.href} style={{ textDecoration: 'none', display: 'block' }}>
                <div className="card" style={{ height: '100%', cursor: 'pointer', display: 'flex', flexDirection: 'column' }}>
                  <div style={{
                    width: '80px',
                    height: '80px',
                    border: '1px solid #ffffff',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    marginBottom: '2rem',
                    color: '#ffffff',
                    flexShrink: 0
                  }}>
                    {portal.icon}
                  </div>
                  <h3 style={{ marginBottom: '1rem', letterSpacing: '0.1em', fontWeight: 400, marginTop: 0 }}>{portal.title}</h3>
                  <p style={{ marginBottom: '2rem', fontSize: '0.9375rem', flex: 1 }}>{portal.desc}</p>
                  <div style={{
                    display: 'inline-block',
                    padding: '0.75rem 1.5rem',
                    border: '1px solid #ffffff',
                    fontSize: '0.75rem',
                    fontWeight: 400,
                    letterSpacing: '0.1em',
                    transition: 'all 0.3s',
                    alignSelf: 'flex-start'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.background = '#ffffff'
                    e.currentTarget.style.color = '#000000'
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.background = 'transparent'
                    e.currentTarget.style.color = '#ffffff'
                  }}
                  >
                    ACCESS PORTAL →
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Security Badge */}
      <section 
        id="security"
        style={{ 
          padding: '8rem 0', 
          textAlign: 'center',
          opacity: isVisible['security'] ? 1 : 0,
          transform: isVisible['security'] ? 'translateY(0)' : 'translateY(30px)',
          transition: 'opacity 0.8s ease-out, transform 0.8s ease-out'
        }}
      >
        <div className="container">
          <div style={{
            width: '100px',
            height: '100px',
            border: '1px solid #ffffff',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 2rem'
          }}>
            <svg width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="1">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            </svg>
          </div>
          <h2 style={{ marginBottom: '1.5rem', letterSpacing: '0.05em' }}>BUILT WITH SECURITY & TRANSPARENCY</h2>
          <p style={{ maxWidth: '800px', margin: '0 auto', fontSize: '1rem' }}>
            AES-256 ENCRYPTION • AI-POWERED VALIDATION • ZERO-TRUST ARCHITECTURE • COMPLETE AUDIT TRAILS
          </p>
        </div>
      </section>
    </main>
  )
}
