import React from "react";
import { getForkClustering } from "./repository";

const ForkCluster = () => {
  return (
    <div>
      <button
        onClick={() => {
          getForkClustering("d3/d3");
        }}
      >
        here
      </button>
    </div>
  );
};

export default ForkCluster;
