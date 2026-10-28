import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import ChatWidget from './components/ChatWidget'
import ProtectedRoute from './components/ProtectedRoute'

import Home from './pages/Home'
import Search from './pages/Search'
import ProductAnalysis from './pages/ProductAnalysis'
import Reviews from './pages/Reviews'
import Recommendations from './pages/Recommendations'
import Compare from './pages/Compare'
import Trends from './pages/Trends'
import Rankings from './pages/Rankings'
import Personalized from './pages/Personalized'
import RatingPredict from './pages/RatingPredict'
import Authenticity from './pages/Authenticity'
import PriceTracking from './pages/PriceTracking'
import Notifications from './pages/Notifications'
import Wishlist from './pages/Wishlist'
import Alerts from './pages/Alerts'
import Login from './pages/Login'
import Register from './pages/Register'
import Account from './pages/Account'
import Assistant from './pages/Assistant'
import NotFound from './pages/NotFound'

export default function App() {
  return (
    <>
      <Navbar />
      <main className="container page">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/search" element={<Search />} />
          <Route path="/product/:id" element={<ProductAnalysis />} />
          <Route path="/product/:id/reviews" element={<Reviews />} />
          <Route path="/product/:id/trends" element={<Trends />} />
          <Route path="/product/:id/authenticity" element={<Authenticity />} />
          <Route path="/product/:id/price" element={<PriceTracking />} />
          <Route path="/recommend" element={<Recommendations />} />
          <Route path="/compare" element={<Compare />} />
          <Route path="/rankings" element={<Rankings />} />
          <Route path="/rating-predict" element={<RatingPredict />} />
          <Route path="/assistant" element={<Assistant />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/personalized" element={<ProtectedRoute><Personalized /></ProtectedRoute>} />
          <Route path="/wishlist" element={<ProtectedRoute><Wishlist /></ProtectedRoute>} />
          <Route path="/alerts" element={<ProtectedRoute><Alerts /></ProtectedRoute>} />
          <Route path="/notifications" element={<ProtectedRoute><Notifications /></ProtectedRoute>} />
          <Route path="/account" element={<ProtectedRoute><Account /></ProtectedRoute>} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>
      <footer className="footer">
        <div className="container">
          ReviewLeaf · Product Review Analysis & Recommendation. Demo data for development.
        </div>
      </footer>
      <ChatWidget />
    </>
  )
}
