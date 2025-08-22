import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import ResultsPage from './pages/ResultsPage';

/**
 * The root component for the ForecastForge front‑end.
 *
 * This component defines the client‑side routes for the application
 * using React Router.  The ``HomePage`` handles CSV uploads and
 * task initiation, while the ``ResultsPage`` polls the backend for
 * task status and displays model results.
 */
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/results/:taskId" element={<ResultsPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;