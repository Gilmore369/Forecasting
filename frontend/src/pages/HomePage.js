import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

/**
 * Home page component.
 *
 * Presents a form that allows users to upload a CSV file containing
 * historical demand data.  When submitted the file is posted to the
 * backend ``/api/process`` endpoint.  On success the user is
 * redirected to the results page where task progress is displayed.
 */
export default function HomePage() {
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Por favor, selecciona un archivo CSV.');
      return;
    }
    setLoading(true);
    setError('');
    const formData = new FormData();
    formData.append('file', file);
    try {
      const response = await axios.post(
        'http://localhost:8000/api/process',
        formData,
        {
          headers: { 'Content-Type': 'multipart/form-data' },
        }
      );
      // Redirect to the results page with the returned task ID
      navigate(`/results/${response.data.task_id}`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Ocurrió un error al subir el archivo.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-8 text-center">
      <h1 className="text-4xl font-bold mb-4">ForecastForge</h1>
      <p className="text-lg text-gray-600 mb-8">
        Sube tus datos de demanda y encuentra el mejor modelo de pronóstico.
      </p>
      <form onSubmit={handleSubmit} className="max-w-md mx-auto">
        <input
          type="file"
          onChange={handleFileChange}
          accept=".csv"
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
        />
        <button
          type="submit"
          disabled={loading}
          className="mt-4 w-full bg-blue-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-700 disabled:bg-blue-300"
        >
          {loading ? 'Procesando...' : 'Analizar Datos'}
        </button>
        {error && <p className="mt-4 text-red-500">{error}</p>}
      </form>
    </div>
  );
}