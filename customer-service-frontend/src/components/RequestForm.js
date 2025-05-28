import React, { useState } from 'react';

function RequestForm() {
  const [message, setMessage] = useState('');
  const [email, setEmail] = useState('');
  /* const [department, setDepartment] = useState(''); */
  const [status, setStatus] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = { message, email/* , department  */};

    try {
      const res = await fetch('http://localhost:5000/api/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': 'mysecureapikey123'
        },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        setStatus('Request submitted successfully!');
        setMessage('');
        setEmail('');
       /*  setDepartment(''); */
      } else {
        setStatus('Error submitting request.');
      }
    } catch (err) {
      console.error(err);
      setStatus('Error connecting to server.');
    }
  };

  return (
    <div style={{ maxWidth: '500px', margin: '2rem auto', fontFamily: 'Arial' }}>
      <h2>Submit a Request</h2>
      <form onSubmit={handleSubmit}>
        <label>Message</label>
        <textarea value={message} onChange={e => setMessage(e.target.value)} required />

        <label>Email</label>
        <input type="email" value={email} onChange={e => setEmail(e.target.value)} required />

{/*         <label>Department</label>
        <input value={department} onChange={e => setDepartment(e.target.value)} required /> */}

        <button type="submit">Send</button>
      </form>
      {status && <p>{status}</p>}
    </div>
  );
}

export default RequestForm;
