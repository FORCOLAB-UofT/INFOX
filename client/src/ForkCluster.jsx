import React, { useState } from "react";
import { getForkClustering } from "./repository";
import { ResponsiveNetworkCanvas } from "@nivo/network";
import { Box } from "@mui/material";

const ForkCluster = () => {
  const [data, setData] = useState(null);
  const [annotations, setAnnotations] = useState(null);

  return (
    <div>
      <div>
        <button
          onClick={async () => {
            const response = await getForkClustering(
              "freeCodeCamp/freeCodeCamp"
            );
            console.log(response);
            setData(response.data);

            let ann = [];
            response.data.nodes.forEach((node) => {
              if (node.height === 1) {
                ann.push({
                  type: "circle",
                  match: {
                    id: node.id,
                  },
                  note: node.id,
                  noteX: 10,
                  noteY: 10,
                  offset: 2,
                  noteTextOffset: 1,
                });
              }
            });
            setAnnotations(ann);
          }}
        >
          here
        </button>
      </div>

      {data ? (
        <div
          style={{
            height: "100vh",
          }}
        >
          <ResponsiveNetworkCanvas
            data={data}
            margin={{ top: 0, right: 0, bottom: 0, left: 0 }}
            linkDistance={function (e) {
              return e.distance;
            }}
            centeringStrength={0.8}
            repulsivity={120}
            iterations={260}
            nodeColor={function (e) {
              return e.color;
            }}
            nodeBorderWidth={1}
            nodeBorderColor={{
              from: "color",
              modifiers: [["darker", 0.8]],
            }}
            linkThickness={function (n) {
              return 2 + 2 * n.target.data.height;
            }}
          />
        </div>
      ) : null}
    </div>
  );
};

export default ForkCluster;
