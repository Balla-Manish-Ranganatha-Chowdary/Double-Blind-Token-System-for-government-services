'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

export default function Navbar() {
  const pathname = usePathname()

  return (
    <nav style={{
      background: 'rgba(0, 0, 0, 0.8)',
      backdropFilter: 'blur(20px)',
      borderBottom: '1px solid var(--border-dark)',
      padding: '1.5rem 0',
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      zIndex: 1000
    }}>
      <div className="container" style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <Link href="/" style={{
          fontSize: '1rem',
          fontWeight: 400,
          color: 'var(--text-white)',
          textDecoration: 'none',
          transition: 'all 0.3s',
          letterSpacing: '0.1em',
          textTransform: 'uppercase'
        }}>
          Government Services
        </Link>

        <div style={{
          display: 'flex',
          gap: '2rem',
          alignItems: 'center'
        }}>
          <Link href="/apply" style={{
            color: 'var(--text-white)',
            textDecoration: 'none',
            fontWeight: 400,
            transition: 'all 0.3s',
            padding: '0.5rem 0',
            fontSize: '0.875rem',
            letterSpacing: '0.05em',
            textTransform: 'uppercase',
            borderBottom: pathname === '/apply' ? '1px solid var(--text-white)' : '1px solid transparent'
          }}>
            Apply
          </Link>
          <Link href="/status" style={{
            color: 'var(--text-white)',
            textDecoration: 'none',
            fontWeight: 400,
            transition: 'all 0.3s',
            padding: '0.5rem 0',
            fontSize: '0.875rem',
            letterSpacing: '0.05em',
            textTransform: 'uppercase',
            borderBottom: pathname === '/status' ? '1px solid var(--text-white)' : '1px solid transparent'
          }}>
            Status
          </Link>
        </div>
      </div>
    </nav>
  )
}
