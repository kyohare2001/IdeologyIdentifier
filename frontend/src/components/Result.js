// src/components/Result.js
import React from 'react';

const Result = ({ data }) => {
  return (
    <div>
      <h3>結果:</h3>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
};

export default Result;
