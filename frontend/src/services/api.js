const API_BASE = process.env.REACT_APP_API_URL || '';

/**
 * Send message to Python backend
 * Expects your backend to have an endpoint like POST /api/chat
 */
const safeJson = async (response) => {
  const text = await response.text();
  if (!text) return {};  // Empty response
  try {
    return JSON.parse(text);
  } catch (e) {
    throw new Error(`Invalid JSON response: ${text.substring(0, 100)}`);
  }
};

const getAuthHeaders = () => {
  const token = sessionStorage.getItem("access_token");

  return {
    "Content-Type": "application/json",
    ...(token && {
      Authorization: `Bearer ${token}`
    })
  };
};

export const sendMessageToBackend = async (message, options = {}) => {
  const { thread_id, file } = options;

  if (file) {
    const formData = new FormData();
    formData.append('message', message);
    if (thread_id) formData.append('thread_id', thread_id);
    formData.append('file', file);

    const token = sessionStorage.getItem( "access_token" );

    const response = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: token ? { Authorization: `Bearer ${token}` } : {},
      body: formData,
    });

    if (!response.ok) {
      const error = await safeJson(response);
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    return safeJson(response);
  }

  const response = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({ message, thread_id }),
  });

  if (!response.ok) {
    const error = await safeJson(response);
    throw new Error(error.detail || `HTTP error! status: ${response.status}`);
  }

  return safeJson(response);
};

export const createCustomer = async (customerData) => {
  const response = await fetch(
    `${API_BASE}/customers/`,
    {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify(customerData),
    }
  );

  if (!response.ok) {
    const error = await safeJson(response);
    throw new Error(error.detail || "Failed to create customer");
  }

  return safeJson(response);
};

export const updateCustomer = async (customerId, customerData) => {
  const response = await fetch(
    `${API_BASE}/customers/${customerId}`,
    {
      method: "PUT",
      headers: getAuthHeaders(),
      body: JSON.stringify(customerData),
    }
  );

  if (!response.ok) {
    const error = await safeJson(response);
    throw new Error(error.detail || "Failed to update customer");
  }
  return safeJson(response);
};

export const getCustomerByEmail = async (
  email
) => {

  const response = await fetch(
    `${API_BASE}/customers/email/${email}`,
      { method: "GET", headers: getAuthHeaders() }
  );

  if (!response.ok) {
    const error = await safeJson(response);
    throw new Error(error.detail || `Customer not found with email: ${email}`);
  }

  return safeJson(response);
};
export const loginCustomer = async (credentials) => {
  const response = await fetch(
    `${API_BASE}/signin/`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(credentials),
    }
  );

  if (!response.ok) {
    const error = await safeJson(response);
    throw new Error(error.detail || "Invalid email or password");
  }

  return safeJson(response);
};

export const logoutCustomer = () => {
  sessionStorage.removeItem( "access_token" );
  sessionStorage.removeItem( "abc_finance_user" );
};

export const getCurrentCustomer = async () => {

  const response = await fetch(
    `${API_BASE}/customers/me`,
    {
      method: "GET",
      headers: getAuthHeaders()
    }
  );

  if (!response.ok) {

    const error = await safeJson(response);

    throw new Error(
      error.detail ||
      "Failed to fetch customer"
    );
  }

  return safeJson(response);
};


export const updateCurrentCustomer = async (
  customerData
) => {

  const response = await fetch(
    `${API_BASE}/customers/me`,
    {
      method: "PUT",
      headers: getAuthHeaders(),
      body: JSON.stringify(customerData)
    }
  );

  if (!response.ok) {

    const error = await safeJson(response);

    throw new Error(
      error.detail ||
      "Failed to update customer"
    );
  }

  return safeJson(response);
};

/**
 * Alternative: WebSocket connection for real-time updates
 * Uncomment if your backend supports WebSockets
 */
/*
export const createWebSocketConnection = (onMessage) => {
  const ws = new WebSocket('ws://localhost:8000/ws');

  ws.onopen = () => console.log('WebSocket connected');
  ws.onmessage = (event) => onMessage(JSON.parse(event.data));
  ws.onerror = (error) => console.error('WebSocket error:', error);
  ws.onclose = () => console.log('WebSocket disconnected');

  return ws;
};
*/