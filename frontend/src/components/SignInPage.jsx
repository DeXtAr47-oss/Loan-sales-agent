import React, { useState } from 'react';
import { X, Mail, Lock, Loader, AlertCircle, LogIn, Eye, EyeOff } from 'lucide-react';
import { loginCustomer } from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function SignInModal({ onClose, onSwitchToSignUp }) {
  const { login } = useAuth();

  const [formData, setFormData] = useState({ email: '', password: '' });
  const [errors, setErrors]     = useState({});
  const [loading, setLoading]   = useState(false);
  const [apiError, setApiError] = useState('');
  const [showPwd, setShowPwd]   = useState(false);
  const [success, setSuccess]   = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) setErrors(prev => ({ ...prev, [name]: '' }));
    setApiError('');
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.email.trim()) newErrors.email = 'Email is required';
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email))
      newErrors.email = 'Please enter a valid email';
    if (!formData.password) newErrors.password = 'Password is required';
    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const validationErrors = validate();
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setLoading(true);
    setApiError('');

    try {
      const response = await loginCustomer({ email: formData.email, password: formData.password });
      login(response);
      setSuccess(true);
      setTimeout(() => onClose(), 1800);
    } catch (error) {
      setApiError(error.message || 'Invalid email or password. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="account-form-overlay">
        <div className="account-form success">
          <div className="success-icon">✓</div>
          <h2>Welcome back!</h2>
          <p>You've signed in successfully.</p>
          <button onClick={onClose} className="btn-primary">Continue</button>
        </div>
      </div>
    );
  }

  return (
    <div className="account-form-overlay">
      <div className="account-form auth-form">
        <div className="form-header">
          <h2><LogIn size={22} /> Sign In</h2>
          <button onClick={onClose} className="close-btn"><X size={22} /></button>
        </div>

        {apiError && (
          <div className="api-error-banner">
            <AlertCircle size={16} />
            {apiError}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group full-width">
            <label><Mail size={15} /> Email address</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="john@example.com"
              className={errors.email ? 'error' : ''}
              autoFocus
            />
            {errors.email && <span className="error-text">{errors.email}</span>}
          </div>

          <div className="form-group full-width">
            <div className="label-row">
              <label><Lock size={15} /> Password</label>
              <button type="button" className="link-btn forgot-link">Forgot password?</button>
            </div>
            <div className="password-input-wrap">
              <input
                type={showPwd ? 'text' : 'password'}
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="••••••••"
                className={errors.password ? 'error' : ''}
              />
              <button
                type="button"
                className="pwd-toggle"
                onClick={() => setShowPwd(!showPwd)}
                tabIndex={-1}
              >
                {showPwd ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
            {errors.password && <span className="error-text">{errors.password}</span>}
          </div>

          <button
            type="submit"
            className="btn-primary submit-btn"
            disabled={loading}
          >
            {loading ? <Loader size={18} className="spinning" /> : <LogIn size={18} />}
            {loading ? 'Signing in...' : 'Sign In'}
          </button>

          <p className="auth-switch">
            Don't have an account?{' '}
            <button type="button" className="link-btn" onClick={onSwitchToSignUp}>
              Create Account
            </button>
          </p>
        </form>
      </div>
    </div>
  );
}