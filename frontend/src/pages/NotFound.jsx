import { Link } from 'react-router-dom'

export default function NotFound() {
  return (
    <div className="state">
      <h1>404</h1>
      <p>This page could not be found.</p>
      <Link className="btn" to="/">Back to home</Link>
    </div>
  )
}
