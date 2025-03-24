// src/components/Graph3D.js
import React from 'react';
import Plot from 'react-plotly.js';

const Graph3D = ({ graphData }) => {
  // graphDataはPlotly用のデータ構造と想定
  return (
    <Plot
      data={graphData.data}
      layout={graphData.layout}
      style={{ width: "100%", height: "400px" }}
    />
  );
};

export default Graph3D;
