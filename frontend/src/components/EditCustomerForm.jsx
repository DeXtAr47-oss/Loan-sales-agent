import React, { useEffect, useState } from 'react';
import {
  X,
  Mail,
  User,
  Phone,
  MapPin,
  Home,
  CreditCard,
  Calendar,
  Loader,
  AlertCircle
} from 'lucide-react';

import {
  getCurrentCustomer,
  updateCurrentCustomer
} from '../services/api';

export default function EditCustomerForm({ onClose }) {

  const [customerData, setCustomerData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  useEffect(() => {

    const fetchCustomer = async () => {

      try {

        const data = await getCurrentCustomer();

        setCustomerData({
          name: data.name || '',
          age: data.age || '',
          phone: data.phone || '',
          email: data.email || '',
          city: data.city || '',
          address: data.address || '',
          creditScore:
            data.credit_score?.credit_score || ''
        });

      } catch (err) {

        setError(
          err.message || 'Failed to load customer details'
        );

      } finally {

        setFetching(false);

      }
    };

    fetchCustomer();

  }, []);

  const handleChange = (e) => {

    const { name, value } = e.target;

    setCustomerData(prev => ({
      ...prev,
      [name]: value
    }));

    setError('');

  };

  const handleUpdate = async (e) => {

    e.preventDefault();

    setLoading(true);
    setError('');

    try {

      const payload = {
        name: customerData.name,
        age: customerData.age
          ? parseInt(customerData.age)
          : null,

        phone: customerData.phone,
        email: customerData.email,
        city: customerData.city,
        address: customerData.address,

        credit_score: customerData.creditScore
          ? {
              credit_score: parseInt(
                customerData.creditScore
              )
            }
          : null
      };

      await updateCurrentCustomer(payload);

      setSuccess(true);

      setTimeout(() => {

        onClose();

      }, 2000);

    } catch (err) {

      setError(
        err.message ||
        'Failed to update customer. Please try again.'
      );

    } finally {

      setLoading(false);

    }
  };

  if (fetching) {

    return (
      <div className="account-form-overlay">
        <div className="account-form">
          <Loader
            size={24}
            className="spinning"
          />
        </div>
      </div>
    );
  }

  if (success) {

    return (
      <div className="account-form-overlay">
        <div className="account-form success">
          <div className="success-icon">✓</div>

          <h2>Profile Updated!</h2>

          <p>
            Your details have been updated successfully.
          </p>

          <button
            onClick={onClose}
            className="btn-primary"
          >
            Done
          </button>

        </div>
      </div>
    );
  }

  return (
    <div className="account-form-overlay">

      <div className="account-form">

        <div className="form-header">

          <h2>
            <User size={24} />
            Edit Profile
          </h2>

          <button
            onClick={onClose}
            className="close-btn"
          >
            <X size={24} />
          </button>

        </div>

        {error && (
          <div className="api-error-banner">
            <AlertCircle size={16} />
            {error}
          </div>
        )}

        {customerData && (

          <form onSubmit={handleUpdate}>

            <div className="form-grid">

              <div className="form-group">
                <label>
                  <User size={16} />
                  Full Name
                </label>

                <input
                  type="text"
                  name="name"
                  value={customerData.name}
                  onChange={handleChange}
                  placeholder="John Doe"
                />
              </div>

              <div className="form-group">
                <label>
                  <Calendar size={16} />
                  Age
                </label>

                <input
                  type="number"
                  name="age"
                  value={customerData.age}
                  onChange={handleChange}
                  min="18"
                  max="100"
                />
              </div>

              <div className="form-group">
                <label>
                  <Phone size={16} />
                  Phone Number
                </label>

                <input
                  type="tel"
                  name="phone"
                  value={customerData.phone}
                  onChange={handleChange}
                />
              </div>

              <div className="form-group">
                <label>
                  <Mail size={16} />
                  Email
                </label>

                <input
                  type="email"
                  name="email"
                  value={customerData.email}
                  onChange={handleChange}
                />
              </div>

              <div className="form-group">
                <label>
                  <MapPin size={16} />
                  City
                </label>

                <input
                  type="text"
                  name="city"
                  value={customerData.city}
                  onChange={handleChange}
                />
              </div>

              <div className="form-group">
                <label>
                  <CreditCard size={16} />
                  Credit Score
                </label>

                <input
                  type="number"
                  name="creditScore"
                  value={customerData.creditScore}
                  onChange={handleChange}
                  min="300"
                  max="850"
                />
              </div>

            </div>

            <div className="form-group full-width">

              <label>
                <Home size={16} />
                Address
              </label>

              <textarea
                rows="3"
                name="address"
                value={customerData.address}
                onChange={handleChange}
              />

            </div>

            <button
              type="submit"
              className="btn-primary submit-btn"
              disabled={loading}
            >

              {loading
                ? <Loader size={18} className="spinning" />
                : null}

              {loading
                ? 'Updating...'
                : 'Update Profile'}

            </button>

          </form>

        )}

      </div>

    </div>
  );
}