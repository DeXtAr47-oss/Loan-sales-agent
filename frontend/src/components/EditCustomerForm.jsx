import React, { useState } from 'react';
import { X, Search, Mail, User, Phone, MapPin, Home, CreditCard, Calendar, Loader, AlertCircle } from 'lucide-react';
import { getCustomerByEmail, updateCustomer } from '../services/api';

export default function EditCustomerForm({ onClose }) {
  const [email, setEmail] = useState('');
  const [customerData, setCustomerData] = useState(null);
  const [customerId, setCustomerId] = useState('');
  const [loading, setLoading] = useState(false);
  const [searching, setSearching] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!email.trim()) {
      setError('Please enter an email address');
      return;
    }

    setSearching(true);
    setError('');
    setCustomerData(null);

    try {
      const data = await getCustomerByEmail(email.trim());
      setCustomerId(data.id || data.customer_id || '');
      setCustomerData({
        name: data.name || '',
        age: data.age || '',
        phone: data.phone || '',
        email: data.email || '',
        city: data.city || '',
        address: data.address || '',
        creditScore: data.credit_score || data.creditScore || ''
      });
    } catch (err) {
      setError(err.message || 'Customer not found. Please check the email and try again.');
    } finally {
      setSearching(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCustomerData(prev => ({ ...prev, [name]: value }));
    setError('');
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    if (!customerId) {
      setError('Customer ID is missing. Please search again.');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const payload = {
        name: customerData.name,
        age: parseInt(customerData.age),
        phone: customerData.phone,
        email: customerData.email,
        city: customerData.city,
        address: customerData.address,
        credit_score: parseInt(customerData.creditScore)
      };

      await updateCustomer(customerId, payload);
      setSuccess(true);

      setTimeout(() => {
        onClose();
      }, 2000);
    } catch (err) {
      setError(err.message || 'Failed to update customer. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="account-form-overlay">
        <div className="account-form success">
          <div className="success-icon">✓</div>
          <h2>Customer Updated!</h2>
          <p>Customer details have been updated successfully.</p>
          <button onClick={onClose} className="btn-primary">Done</button>
        </div>
      </div>
    );
  }

  return (
    <div className="account-form-overlay">
      <div className="account-form">
        <div className="form-header">
          <h2><Mail size={24} /> Edit Customer</h2>
          <button onClick={onClose} className="close-btn">
            <X size={24} />
          </button>
        </div>

        {error && (
          <div className="api-error-banner">
            <AlertCircle size={16} />
            {error}
          </div>
        )}

        {/* Search by Email */}
        {!customerData && (
          <form onSubmit={handleSearch} style={{ marginBottom: '24px' }}>
            <div className="form-group full-width">
              <label><Mail size={16} /> Customer Email</label>
              <div style={{ display: 'flex', gap: '12px' }}>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="customer@example.com"
                  style={{ flex: 1 }}
                />
                <button
                  type="submit"
                  className="btn-primary"
                  disabled={searching}
                  style={{ width: 'auto', padding: '12px 24px', margin: 0 }}
                >
                  {searching ? <Loader size={18} className="spinning" /> : <Search size={18} />}
                  {searching ? 'Searching...' : 'Search'}
                </button>
              </div>
            </div>
          </form>
        )}

        {/* Edit Form */}
        {customerData && (
          <form onSubmit={handleUpdate}>
            <div style={{ marginBottom: '20px', padding: '12px 16px', background: 'var(--bg-tertiary)', borderRadius: '10px' }}>
              <span style={{ color: 'var(--text-muted)', fontSize: '13px' }}>Editing: </span>
              <span style={{ color: 'var(--accent-primary)', fontWeight: '600' }}>{email}</span>
            </div>

            <div className="form-grid">
              <div className="form-group">
                <label><User size={16} /> Full Name</label>
                <input
                  type="text"
                  name="name"
                  value={customerData.name}
                  onChange={handleChange}
                  placeholder="John Doe"
                />
              </div>

              <div className="form-group">
                <label><Calendar size={16} /> Age</label>
                <input
                  type="number"
                  name="age"
                  value={customerData.age}
                  onChange={handleChange}
                  placeholder="25"
                  min="18"
                  max="100"
                />
              </div>

              <div className="form-group">
                <label><Phone size={16} /> Phone Number</label>
                <input
                  type="tel"
                  name="phone"
                  value={customerData.phone}
                  onChange={handleChange}
                  placeholder="9876543210"
                />
              </div>

              <div className="form-group">
                <label><Mail size={16} /> Email</label>
                <input
                  type="email"
                  name="email"
                  value={customerData.email}
                  onChange={handleChange}
                  placeholder="john@example.com"
                />
              </div>

              <div className="form-group">
                <label><MapPin size={16} /> City</label>
                <input
                  type="text"
                  name="city"
                  value={customerData.city}
                  onChange={handleChange}
                  placeholder="Mumbai"
                />
              </div>

              <div className="form-group">
                <label><CreditCard size={16} /> Credit Score</label>
                <input
                  type="number"
                  name="creditScore"
                  value={customerData.creditScore}
                  onChange={handleChange}
                  placeholder="750"
                  min="300"
                  max="850"
                />
              </div>
            </div>

            <div className="form-group full-width">
              <label><Home size={16} /> Address</label>
              <textarea
                name="address"
                value={customerData.address}
                onChange={handleChange}
                placeholder="123 Main Street, Apartment 4B"
                rows="3"
              />
            </div>

            <div style={{ display: 'flex', gap: '12px', marginTop: '24px' }}>
              <button
                type="button"
                className="btn-secondary"
                onClick={() => { setCustomerData(null); setEmail(''); }}
                style={{ flex: 1 }}
              >
                Back to Search
              </button>
              <button
                type="submit"
                className="btn-primary submit-btn"
                disabled={loading}
                style={{ flex: 1, margin: 0 }}
              >
                {loading ? <Loader size={18} className="spinning" /> : null}
                {loading ? 'Updating...' : 'Update Customer'}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}