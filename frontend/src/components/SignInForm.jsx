import React, { useState } from 'react';
import { X, Mail, Lock, Loader, AlertCircle, LogIn } from 'lucide-react';
import { loginCustomer } from '../services/api';

export default function SignInForm({ onClose, onSwitchToSignUp, onSuccess }) {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
    setApiError('');
  };

  const validate = () => {
    const newErrors = {};

    if (!formData.email.trim()) newErrors.email = 'Email is required';
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email';
    }

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
      const response = await loginCustomer({
        email: formData.email,
        password: formData.password
      });

      if (onSuccess) onSuccess(response);
      onClose();
    } catch (error) {
      setApiError(error.message || 'Invalid email or password. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="account-form-overlay">
      <div className="account-form auth-form">
        <div className="form-header">
          <h2><LogIn size={24} /> Sign In</h2>
          <button onClick={onClose} className="close-btn">
            <X size={24} />
          </button>
        </div>

        {apiError && (
          <div className="api-error-banner">
            <AlertCircle size={16} />
            {apiError}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group full-width">
            <label><Mail size={16} /> Email</label>
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
            <label><Lock size={16} /> Password</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="••••••••"
              className={errors.password ? 'error' : ''}
            />
            {errors.password && <span className="error-text">{errors.password}</span>}
          </div>

          <button
            type="submit"
            className="btn-primary submit-btn"
            disabled={loading}
          >
            {loading ? <Loader size={18} className="spinning" /> : null}
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
