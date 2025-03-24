// src/components/UserInput.js
import React, { useState } from 'react';

const UserInput = ({ onSubmit }) => {
  const [userId, setUserId] = useState('');

  const handleSubmit = () => {
    if (userId.trim()) {
      onSubmit(userId);
    }
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Enter User ID"
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
      />
      <button onClick={handleSubmit}>結果</button>
    </div>
  );
};

export default UserInput;
