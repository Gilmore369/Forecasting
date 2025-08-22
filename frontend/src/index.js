import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

// Render the React application into the root DOM node.  We use
// React.StrictMode to highlight potential problems and ensure
// adherence to best practices during development.
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);