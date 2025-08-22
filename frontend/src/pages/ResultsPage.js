import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

/**
 * Results page component.
 *
 * Uses the ``taskId`` route parameter to poll the backend for task
 * status and results.  While the background job is running it
 * displays a progress indicator.  Once completed it renders a
 * leaderboard of models ordered by MAPE.
 */
export default function ResultsPage() {
  const { taskId } = useParams();
  const [taskStatus, setTaskStatus] = useState({ status: 'PENDING', meta: {} });
  const [results, setResults] = useState(null);

  useEffect(() => {
    const poll = setInterval(async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/results/${taskId}`);
        if (response.data.status === 'SUCCESS') {
          setResults(response.data.results);
          clearInterval(poll);
        } else {
          setTaskStatus(response.data);
        }
      } catch (error) {
        console.error('Error fetching results:', error);
        clearInterval(poll);
      }
    }, 3000);
    return () => clearInterval(poll);
  }, [taskId]);

  if (!results) {
    const { meta } = taskStatus;
    const progress = meta?.total ? (meta.current / meta.total) * 100 : 0;
    return (
      <div className="text-center p-10">
        <h2 className="text-2xl font-semibold mb-4">Analizando modelos...</h2>
        {meta?.model && (
          <p className="text-gray-600">
            Calculando: {meta.model} ({meta.current} de {meta.total})
          </p>
        )}
        <div className="w-full bg-gray-200 rounded-full h-4 mt-4">
          <div
            className="bg-blue-600 h-4 rounded-full"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-8">
      <h1 className="text-3xl font-bold mb-6">Resultados del Análisis</h1>
      <div className="overflow-x-auto bg-white rounded-lg shadow">
        <table className="min-w-full">
          <thead>
            <tr className="bg-gray-100">
              <th className="p-4 text-left font-semibold">#</th>
              <th className="p-4 text-left font-semibold">Modelo</th>
              <th className="p-4 text-left font-semibold">MAPE</th>
              <th className="p-4 text-left font-semibold">MAE</th>
            </tr>
          </thead>
          <tbody>
            {results.map((res, index) => (
              <tr key={index} className={index === 0 ? 'bg-green-100' : ''}>
                <td className="p-4 font-bold">
                  {index + 1} {index === 0 && '🏆'}
                </td>
                <td className="p-4">{res.model_name}</td>
                <td className="p-4 font-semibold">{res.metrics.mape.toFixed(2)}%</td>
                <td className="p-4">{res.metrics.mae.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}