import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  MessageCircle,
  Shield,
  TrendingUp,
  Clock,
  ChevronRight,
  ChevronDown,
  Star,
  Users,
  Award,
  Calculator,
  FileCheck,
  Wallet,
  Building2,
  Car,
  GraduationCap,
  Home as HomeIcon,
  Briefcase,
  X,
  ArrowRight,
  LogIn,
  UserPlus
} from 'lucide-react';
import AccountForm from './AccountForm';
import SignInForm from './SignInForm';

const EMI_RATE_DEFAULT = 11.5;

function EmiCalculator() {
  const [amount, setAmount] = useState(500000);
  const [tenure, setTenure] = useState(36);
  const [rate, setRate] = useState(EMI_RATE_DEFAULT);

  const monthlyRate = rate / 12 / 100;
  const emi =
    amount *
    monthlyRate *
    Math.pow(1 + monthlyRate, tenure) /
    (Math.pow(1 + monthlyRate, tenure) - 1);

  const totalPayment = emi * tenure;
  const totalInterest = totalPayment - amount;

  return (
    <div className="emi-calculator">
      <div className="emi-inputs">
        <div className="emi-field">
          <div className="emi-field-label">
            <span>Loan amount</span>
            <span className="emi-value">₹{amount.toLocaleString('en-IN')}</span>
          </div>
          <input
            type="range"
            min="50000"
            max="5000000"
            step="10000"
            value={amount}
            onChange={(e) => setAmount(Number(e.target.value))}
          />
        </div>
        <div className="emi-field">
          <div className="emi-field-label">
            <span>Tenure</span>
            <span className="emi-value">{tenure} months</span>
          </div>
          <input
            type="range"
            min="6"
            max="84"
            step="6"
            value={tenure}
            onChange={(e) => setTenure(Number(e.target.value))}
          />
        </div>
        <div className="emi-field">
          <div className="emi-field-label">
            <span>Interest rate</span>
            <span className="emi-value">{rate}% p.a.</span>
          </div>
          <input
            type="range"
            min="8"
            max="24"
            step="0.1"
            value={rate}
            onChange={(e) => setRate(Number(e.target.value))}
          />
        </div>
      </div>

      <div className="emi-results">
        <div className="emi-result-main">
          <span className="emi-result-label">Monthly EMI</span>
          <span className="emi-result-value">
            ₹{Math.round(emi).toLocaleString('en-IN')}
          </span>
        </div>
        <div className="emi-result-grid">
          <div>
            <span className="emi-result-label">Total interest</span>
            <span className="emi-result-sub">
              ₹{Math.round(totalInterest).toLocaleString('en-IN')}
            </span>
          </div>
          <div>
            <span className="emi-result-label">Total payment</span>
            <span className="emi-result-sub">
              ₹{Math.round(totalPayment).toLocaleString('en-IN')}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

function FaqItem({ question, answer }) {
  const [open, setOpen] = useState(false);
  return (
    <div className={`faq-item ${open ? 'open' : ''}`}>
      <button className="faq-question" onClick={() => setOpen(!open)}>
        {question}
        <ChevronDown size={18} className="faq-chevron" />
      </button>
      {open && <div className="faq-answer">{answer}</div>}
    </div>
  );
}

export default function HomePage() {
  const navigate = useNavigate();
  const [eligAmount, setEligAmount] = useState('');
  const [eligIncome, setEligIncome] = useState('');
  const [authModal, setAuthModal] = useState(null); // 'signin' | 'signup' | null

  const goToChat = (prefill) => {
    navigate('/chat', { state: prefill ? { prefill } : undefined });
  };

  const handleEligibilitySubmit = (e) => {
    e.preventDefault();
    goToChat(
      `I'd like to check my loan eligibility. My monthly income is ₹${eligIncome} and I'm looking for a loan of ₹${eligAmount}.`
    );
  };

  return (
    <div className="home-page">
      {/* NAVBAR */}
      <nav className="navbar">
        <div className="navbar-brand">
          <div className="brand-mark">AF</div>
          <span>ABC Finance</span>
        </div>
        <div className="navbar-links">
          <a href="#products">Loans</a>
          <a href="#calculator">EMI Calculator</a>
          <a href="#eligibility">Eligibility</a>
          <a href="#track">Track Application</a>
          <a href="#faq">FAQs</a>
        </div>
        <div className="navbar-actions">
          <button className="btn-ghost" onClick={() => setAuthModal('signin')}>
            <LogIn size={16} />
            Sign In
          </button>
          <button className="btn-primary" onClick={() => setAuthModal('signup')}>
            <UserPlus size={16} />
            Create Account
          </button>
        </div>
      </nav>

      {/* HERO */}
      <section className="hero">
        <div className="hero-content">
          <div className="hero-badge">
            <Star size={16} />
            RBI-registered NBFC · Trusted by 10,000+ customers
          </div>
          <h1>Borrow smarter with ABC Finance</h1>
          <p>
            Instant loan approvals, transparent rates, and a digital-first
            process. Talk to our AI lending assistant — check eligibility,
            compare offers, apply, and track your application, all in one
            conversation.
          </p>
          <div className="hero-buttons">
            <button className="btn-primary btn-large" onClick={() => goToChat()}>
              <MessageCircle size={20} />
              Start Chatting
              <ChevronRight size={20} />
            </button>
            <button
              className="btn-secondary btn-large"
              onClick={() =>
                document
                  .getElementById('eligibility')
                  .scrollIntoView({ behavior: 'smooth' })
              }
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
              <span>ABC Finance Assistant</span>
            </div>
            <div className="preview-messages">
              <div className="preview-msg bot">
                Hello! I'm your ABC Finance assistant. What's your name?
              </div>
              <div className="preview-msg user">
                Hi, I'm looking for a personal loan
              </div>
              <div className="preview-msg bot">
                Great! I can check your eligibility right now. Let's start...
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* TRUST STRIP */}
      <section className="trust-strip">
        <div className="trust-item">
          <Shield size={20} />
          <span>RBI Registered NBFC</span>
        </div>
        <div className="trust-item">
          <FileCheck size={20} />
          <span>100% Paperless KYC</span>
        </div>
        <div className="trust-item">
          <Award size={20} />
          <span>ISO 27001 Certified</span>
        </div>
        <div className="trust-item">
          <Users size={20} />
          <span>4.7★ Customer Rating</span>
        </div>
      </section>

      {/* PRODUCTS */}
      <section className="loan-types" id="products">
        <h2>Loans We Offer</h2>
        <p className="section-subtitle">
          Pick a product or just tell our assistant what you need —
          we'll match you with the right loan.
        </p>
        <div className="loan-grid">
          <div className="loan-card" onClick={() => goToChat('I want to apply for a personal loan')}>
            <Award size={32} />
            <h3>Personal Loan</h3>
            <p>Up to ₹25 Lakhs</p>
            <span className="loan-rate">From 8.5%</span>
          </div>
          <div className="loan-card" onClick={() => goToChat('I want to apply for a business loan')}>
            <Briefcase size={32} />
            <h3>Business Loan</h3>
            <p>Up to ₹2 Crores</p>
            <span className="loan-rate">From 10.5%</span>
          </div>
          <div className="loan-card" onClick={() => goToChat('I want to apply for a home loan')}>
            <HomeIcon size={32} />
            <h3>Home Loan</h3>
            <p>Up to ₹5 Crores</p>
            <span className="loan-rate">From 7.5%</span>
          </div>
          <div className="loan-card" onClick={() => goToChat('I want to apply for a vehicle loan')}>
            <Car size={32} />
            <h3>Vehicle Loan</h3>
            <p>Up to ₹50 Lakhs</p>
            <span className="loan-rate">From 9%</span>
          </div>
          <div className="loan-card" onClick={() => goToChat('I want to apply for an education loan')}>
            <GraduationCap size={32} />
            <h3>Education Loan</h3>
            <p>Up to ₹40 Lakhs</p>
            <span className="loan-rate">From 9.5%</span>
          </div>
          <div className="loan-card" onClick={() => goToChat('I want to apply for a loan against property')}>
            <Building2 size={32} />
            <h3>Loan Against Property</h3>
            <p>Up to ₹3 Crores</p>
            <span className="loan-rate">From 9.75%</span>
          </div>
        </div>
      </section>

      {/* FEATURES */}
      <section className="features">
        <h2>Why Choose ABC Finance?</h2>
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
            <p>Bank-grade encryption and RBI-compliant data handling protect your information.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">
              <TrendingUp size={28} />
            </div>
            <h3>Best Rates</h3>
            <p>Starting from 7.5% APR with transparent pricing — no hidden charges.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">
              <Users size={28} />
            </div>
            <h3>24/7 Support</h3>
            <p>Our AI assistant and support team are available round the clock.</p>
          </div>
        </div>
      </section>

      {/* EMI CALCULATOR */}
      <section className="calculator-section" id="calculator">
        <div className="calculator-intro">
          <h2>Plan your EMI</h2>
          <p className="section-subtitle">
            Adjust the sliders to estimate your monthly repayment before you apply.
          </p>
          <div className="calculator-cta">
            <Calculator size={20} />
            <span>Want exact numbers for your profile? Ask our assistant.</span>
            <button className="btn-secondary" onClick={() => goToChat('Can you calculate my EMI based on my profile?')}>
              Ask Assistant
            </button>
          </div>
        </div>
        <EmiCalculator />
      </section>

      {/* ELIGIBILITY CHECK */}
      <section className="eligibility-section" id="eligibility">
        <h2>Check Your Eligibility</h2>
        <p className="section-subtitle">
          Get a quick read on what you may qualify for — then continue
          with our assistant to complete your application.
        </p>
        <form className="eligibility-form" onSubmit={handleEligibilitySubmit}>
          <div className="form-group">
            <label>
              <Wallet size={16} />
              Monthly income (₹)
            </label>
            <input
              type="number"
              placeholder="e.g. 60000"
              value={eligIncome}
              onChange={(e) => setEligIncome(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>
              <Award size={16} />
              Desired loan amount (₹)
            </label>
            <input
              type="number"
              placeholder="e.g. 500000"
              value={eligAmount}
              onChange={(e) => setEligAmount(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="btn-primary btn-large submit-btn">
            Check Eligibility with Assistant
            <ArrowRight size={18} />
          </button>
        </form>
      </section>

      {/* TRACK APPLICATION */}
      <section className="track-section" id="track">
        <div className="track-card">
          <FileCheck size={36} />
          <div>
            <h3>Already applied?</h3>
            <p>Track your loan application status, upload pending documents, or ask about disbursal timelines.</p>
          </div>
          <button className="btn-secondary" onClick={() => goToChat('I want to track my loan application status')}>
            Track Application
          </button>
        </div>
      </section>

      {/* FAQ */}
      <section className="faq-section" id="faq">
        <h2>Frequently Asked Questions</h2>
        <div className="faq-list">
          <FaqItem
            question="What documents do I need to apply?"
            answer="You'll typically need PAN card, Aadhaar card, recent bank statements (3-6 months), salary slips or income proof, and a passport-size photo. Our assistant will guide you through uploading these securely."
          />
          <FaqItem
            question="How long does approval take?"
            answer="Most personal loan applications receive an in-principle decision within 2 minutes. Final disbursal, after document verification, typically happens within 24-48 hours."
          />
          <FaqItem
            question="Are there any prepayment charges?"
            answer="Personal and business loans can be foreclosed after 12 EMIs with nominal charges. Home loans and loans against property have zero prepayment charges on floating rates, as per RBI guidelines."
          />
          <FaqItem
            question="Is my data safe?"
            answer="Yes. ABC Finance is ISO 27001 certified and follows RBI's data protection guidelines. Your information is encrypted end-to-end and never shared with third parties without consent."
          />
          <FaqItem
            question="Can I apply with a co-applicant?"
            answer="Yes, for home loans, loans against property, and certain business loans, you can add a co-applicant to improve eligibility. Just mention this to our assistant during the application."
          />
        </div>
      </section>

      {/* CTA */}
      <section className="cta-section">
        <h2>Ready to Get Started?</h2>
        <p>Chat with our AI agent and get your loan approved in minutes.</p>
        <button className="btn-primary btn-large" onClick={() => goToChat()}>
          <MessageCircle size={20} />
          Start Your Application
        </button>
      </section>

      {/* FOOTER */}
      <footer className="home-footer">
        <div className="footer-grid">
          <div className="footer-col">
            <div className="navbar-brand">
              <div className="brand-mark">AF</div>
              <span>ABC Finance</span>
            </div>
            <p>
              ABC Finance Pvt. Ltd. is a Non-Banking Financial Company
              registered with the Reserve Bank of India.
            </p>
          </div>
          <div className="footer-col">
            <h4>Products</h4>
            <a href="#products">Personal Loan</a>
            <a href="#products">Business Loan</a>
            <a href="#products">Home Loan</a>
            <a href="#products">Vehicle Loan</a>
          </div>
          <div className="footer-col">
            <h4>Company</h4>
            <a href="#faq">FAQs</a>
            <a href="#eligibility">Eligibility</a>
            <a href="#track">Track Application</a>
          </div>
          <div className="footer-col">
            <h4>Legal</h4>
            <a href="#">Privacy Policy</a>
            <a href="#">Terms of Service</a>
            <a href="#">Grievance Redressal</a>
            <a href="#">RBI Disclosures</a>
          </div>
        </div>
        <p className="footer-bottom">© 2026 ABC Finance Pvt. Ltd. All rights reserved. CIN: U65900XX2024PLC000000 · NBFC Registration No. N-00.00000</p>
      </footer>

      {/* FLOATING CHAT LAUNCHER */}
      <button className="chat-launcher" onClick={() => goToChat()} aria-label="Open chat assistant">
        <MessageCircle size={26} />
        <span className="chat-launcher-pulse"></span>
      </button>

      {/* AUTH MODALS */}
      {authModal === 'signin' && (
        <SignInForm
          onClose={() => setAuthModal(null)}
          onSwitchToSignUp={() => setAuthModal('signup')}
          onSuccess={() => goToChat()}
        />
      )}
      {authModal === 'signup' && (
        <AccountForm onClose={() => setAuthModal(null)} />
      )}
    </div>
  );
} 