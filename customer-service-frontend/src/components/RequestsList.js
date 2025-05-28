import React, { useEffect, useState } from 'react';

function RequestsList() {
  const [requests, setRequests] = useState([]);
  const [error, setError] = useState(null);

  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const requestsPerPage = 5;

  useEffect(() => {
    const fetchRequests = async () => {
      try {
        const res = await fetch('http://localhost:5000/requests', {
          headers: {
            'x-api-key': 'mysecureapikey123'
          }
        });
        if (!res.ok) throw new Error('Failed to fetch requests');
        const data = await res.json();
        setRequests(data);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchRequests();
  }, []);

  // Pagination logic
  const totalPages = Math.ceil(requests.length / requestsPerPage);
  const startIndex = (currentPage - 1) * requestsPerPage;
  const currentRequests = requests.slice(startIndex, startIndex + requestsPerPage);

  const goToNextPage = () => setCurrentPage((prev) => Math.min(prev + 1, totalPages));
  const goToPrevPage = () => setCurrentPage((prev) => Math.max(prev - 1, 1));

  if (error) return <p>{error}</p>;

  return (
    <div style={{ maxWidth: '600px', margin: '2rem auto', fontFamily: 'Arial' }}>
      <h2>All Requests</h2>

      <ul>
        {currentRequests.map((req, index) => (
          <li key={index} style={{ marginBottom: '1rem', borderBottom: '1px solid #ccc', paddingBottom: '1rem' }}>
            <p><strong>Email:</strong> {req.email}</p>
            <p><strong>Message:</strong> {req.message}</p>
            <p><strong>Department:</strong> {req.department}</p>
            <p><strong>Status:</strong> {req.status}</p>
            <p><strong>Timestamp:</strong> {req.timestamp}</p>
          </li>
        ))}
      </ul>

      {/* Pagination Controls */}
      {requests.length > requestsPerPage && (
        <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '1rem' }}>
          <button onClick={goToPrevPage} disabled={currentPage === 1}>
            ← Previous
          </button>
          <span>Page {currentPage} of {totalPages}</span>
          <button onClick={goToNextPage} disabled={currentPage === totalPages}>
            Next →
          </button>
        </div>
      )}
    </div>
  );
}

export default RequestsList;
