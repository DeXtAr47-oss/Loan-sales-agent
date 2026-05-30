import React, { useState } from 'react';
import { X, User, Lock, Phone, Mail, MapPin, Home, CreditCard, Calendar, Loader, AlertCircle } from 'lucide-react';
import { createCustomer } from '../services/api';

export default function AccountForm({ onClose }) {
  const [formData, setFormData] = useState({
    name: '',
    password: '',
    confirmPassword: '',
    age: '',
    phone: '',
    email: '',
    city: '',
    address: '',
    creditScore: ''
  });

  const [errors, setErrors] = useState({});
  const [submitted, setSubmitted] = useState(false);
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

    if (!formData.name.trim()) newErrors.name = 'Name is required';
    if (!formData.password) newErrors.password = 'Password is required';
    else if (formData.password.length < 6) newErrors.password = 'Password must be at least 6 characters';

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    if (!formData.age) newErrors.age = 'Age is required';
    else if (formData.age < 18 || formData.age > 100) newErrors.age = 'Age must be between 18 and 100';

    if (!formData.phone.trim()) newErrors.phone = 'Phone is required';
    else if (!/^\d{10}$/.test(formData.phone.replace(/\D/g, ''))) {
      newErrors.phone = 'Please enter a valid 10-digit phone number';
    }

    if (!formData.email.trim()) newErrors.email = 'Email is required';
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email';
    }

    if (!formData.city.trim()) newErrors.city = 'City is required';
    if (!formData.address.trim()) newErrors.address = 'Address is required';

    if (!formData.creditScore) newErrors.creditScore = 'Credit score is required';
    else if (formData.creditScore < 300 || formData.creditScore > 850) {
      newErrors.creditScore = 'Credit score must be between 300 and 850';
    }

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
      const payload = {
        name: formData.name,
        password: formData.password,
        age: parseInt(formData.age),
        phone: formData.phone,
        email: formData.email,
        city: formData.city,
        address: formData.address,
        credit_score: {
          credit_score: parseInt(formData.creditScore)
        }
      };

      const response = await createCustomer(payload);
      console.log('Account created:', response);
      setSubmitted(true);

      setTimeout(() => {
        onClose();
      }, 2500);
    } catch (error) {
      setApiError(error.message || 'Failed to create account. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    return (
      <div className="account-form-overlay">
        <div className="account-form success">
          <div className="success-icon">✓</div>
          <h2>Account Created!</h2>
          <p>Welcome to Loan Sales Agent. You can now start chatting.</p>
          <button onClick={onClose} className="btn-primary">Continue</button>
        </div>
      </div>
    );
  }

  return (
    <div className="account-form-overlay">
      <div className="account-form">
        <div className="form-header">
          <h2><User size={24} /> Create Account</h2>
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
          <div className="form-grid">
            <div className="form-group">
              <label><User size={16} /> Full Name</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="John Doe"
                className={errors.name ? 'error' : ''}
              />
              {errors.name && <span className="error-text">{errors.name}</span>}
            </div>

            <div className="form-group">
              <label><Calendar size={16} /> Age</label>
              <input
                type="number"
                name="age"
                value={formData.age}
                onChange={handleChange}
                placeholder="25"
                min="18"
                max="100"
                className={errors.age ? 'error' : ''}
              />
              {errors.age && <span className="error-text">{errors.age}</span>}
            </div>

            <div className="form-group">
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

            <div className="form-group">
              <label><Lock size={16} /> Confirm Password</label>
              <input
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                placeholder="••••••••"
                className={errors.confirmPassword ? 'error' : ''}
              />
              {errors.confirmPassword && <span className="error-text">{errors.confirmPassword}</span>}
            </div>

            <div className="form-group">
              <label><Phone size={16} /> Phone Number</label>
              <input
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                placeholder="9876543210"
                className={errors.phone ? 'error' : ''}
              />
              {errors.phone && <span className="error-text">{errors.phone}</span>}
            </div>

            <div className="form-group">
              <label><Mail size={16} /> Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="john@example.com"
                className={errors.email ? 'error' : ''}
              />
              {errors.email && <span className="error-text">{errors.email}</span>}
            </div>

            <div className="form-group">
              <label><MapPin size={16} /> City</label>
              <input
                type="text"
                name="city"
                value={formData.city}
                onChange={handleChange}
                placeholder="Mumbai"
                className={errors.city ? 'error' : ''}
              />
              {errors.city && <span className="error-text">{errors.city}</span>}
            </div>

            <div className="form-group">
              <label><CreditCard size={16} /> Credit Score</label>
              <input
                type="number"
                name="creditScore"
                value={formData.creditScore}
                onChange={handleChange}
                placeholder="750"
                min="300"
                max="850"
                className={errors.creditScore ? 'error' : ''}
              />
              {errors.creditScore && <span className="error-text">{errors.creditScore}</span>}
            </div>
          </div>

          <div className="form-group full-width">
            <label><Home size={16} /> Address</label>
            <textarea
              name="address"
              value={formData.address}
              onChange={handleChange}
              placeholder="123 Main Street, Apartment 4B"
              rows="3"
              className={errors.address ? 'error' : ''}
            />
            {errors.address && <span className="error-text">{errors.address}</span>}
          </div>

          <button
            type="submit"
            className="btn-primary submit-btn"
            disabled={loading}
          >
            {loading ? <Loader size={18} className="spinning" /> : null}
            {loading ? 'Creating...' : 'Create Account'}
          </button>
        </form>
      </div>
    </div>
  );
}