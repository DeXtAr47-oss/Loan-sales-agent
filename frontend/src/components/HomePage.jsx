import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  MessageCircle,
  Shield,
  TrendingUp,
  Clock,
  ChevronRight,
  Star,
  Users,
  Award
} from 'lucide-react';

export default function HomePage() {
  const navigate = useNavigate();

  return (
    <div className="home-page">
      <section className="hero">
        <div className="hero-content">
          <div className="hero-badge">
            <Star size={16} />
            Trusted by 10,000+ customers
          </div>
          <h1>Your Personal Loan Assistant</h1>
          <p>
            Get instant loan approvals, check eligibility, compare rates,
            and manage your applications — all through a simple conversation.
          </p>
          <div className="hero-buttons">
            <button
              className="btn-primary btn-large"
              onClick={() => navigate('/chat')}
            >
              <MessageCircle size={20} />
              Start Chatting
              <ChevronRight size={20} />
            </button>
            <button
              className="btn-secondary btn-large"
              onClick={() => navigate('/chat')}
            >
              Check Eligibility
            </button>
          </div>
          <div className="hero-stats">
            <div className="stat">
              <span className="stat-number">₹50Cr+</span>
              <span className="stat-label">Loans Disbursed</span>
            </div>
            <div className="stat">
              <span className="stat-number">2 mins</span>
              <span className="stat-label">Average Approval</span>
            </div>
            <div className="stat">
              <span className="stat-number">8.5%</span>
              <span className="stat-label">Starting Interest</span>
            </div>
          </div>
        </div>
        <div className="hero-visual">
          <div className="chat-preview">
            <div className="preview-header">
              <div className="preview-dot"></div>
              <div className="preview-dot yellow"></div>
              <div className="preview-dot green"></div>
              <span>Loan Agent</span>
            </div>
            <div className="preview-messages">
              <div className="preview-msg bot">
                Hello! I can help you get a loan today. What's your name?
              </div>
              <div className="preview-msg user">
                Hi, I'm looking for a personal loan
              </div>
              <div className="preview-msg bot">
                Great! I can get you approved in 2 minutes. Let's start...
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="features">
        <h2>Why Choose Our Loan Agent?</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">
              <Clock size={28} />
            </div>
            <h3>Instant Approval</h3>
            <p>Get loan approval in just 2 minutes with our AI-powered assessment system.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">
              <Shield size={28} />
            </div>
            <h3>100% Secure</h3>
            <p>Bank-grade encryption protects your personal and financial data.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">
              <TrendingUp size={28} />
            </div>
            <h3>Best Rates</h3>
            <p>Starting from 8.5% APR. We compare offers from 50+ lenders instantly.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">
              <Users size={28} />
            </div>
            <h3>24/7 Support</h3>
            <p>Our AI assistant is available round the clock to answer your queries.</p>
          </div>
        </div>
      </section>

      <section className="loan-types">
        <h2>Loans We Offer</h2>
        <div className="loan-grid">
          <div className="loan-card">
            <Award size={32} />
            <h3>Personal Loan</h3>
            <p>Up to ₹25 Lakhs</p>
            <span className="loan-rate">From 8.5%</span>
          </div>
          <div className="loan-card">
            <TrendingUp size={32} />
            <h3>Business Loan</h3>
            <p>Up to ₹2 Crores</p>
            <span className="loan-rate">From 10.5%</span>
          </div>
          <div className="loan-card">
            <Shield size={32} />
            <h3>Home Loan</h3>
            <p>Up to ₹5 Crores</p>
            <span className="loan-rate">From 7.5%</span>
          </div>
        </div>
      </section>

      <section className="cta-section">
        <h2>Ready to Get Started?</h2>
        <p>Chat with our AI agent and get your loan approved in minutes.</p>
        <button
          className="btn-primary btn-large"
          onClick={() => navigate('/chat')}
        >
          <MessageCircle size={20} />
          Start Your Application
        </button>
      </section>

      <footer className="home-footer">
        <p>© 2026 Loan Sales Agent. All rights reserved.</p>
      </footer>
    </div>
  );
}