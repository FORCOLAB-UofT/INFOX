import React, { useState } from "react";
import { getForkClustering } from "./repository";
import { ResponsiveNetworkCanvas } from "@nivo/network";
import { Box, Button, TextField, Grid } from "@mui/material";
import Loading from "./common/Loading";

const ForkCluster = () => {
  const [data, setData] = useState(null);
  const [annotations, setAnnotations] = useState(null);
  const [searchText, setSearchText] = useState("");
  const [loading, setLoading] = useState(false);

  const onClickSearch = async (event) => {
    event.preventDefault();
    setLoading(true);
    const response = await getForkClustering(searchText);
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
          noteY: 30,
          offset: 2,
          noteTextOffset: 3,
        });
      }
    });
    setAnnotations(ann);
    setLoading(false);
  };

  return (
    <Box>
      <Box>
        <form onSubmit={onClickSearch}>
          <Grid container alignItems="center" paddingBottom={1}>
            <Grid item paddingRight={1}>
              <TextField
                variant="standard"
                label="Repository"
                value={searchText}
                onChange={(event) => {
                  setSearchText(event.target.value);
                }}
              />
            </Grid>
            <Grid item marginTop={1}>
              <Button variant="contained" type="submit">
                Search
              </Button>
            </Grid>
          </Grid>
        </form>

        <button
          onClick={async () => {
            const response = await getForkClustering("home-assistant/core");
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
                  noteY: 30,
                  offset: 2,
                  noteTextOffset: 3,
                });
              }
            });
            setAnnotations(ann);
          }}
        >
          here
        </button>
      </Box>

      {loading ? (
        <Loading loadingMessage="Please wait. This may take a few minutes." />
      ) : data ? (
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
            centeringStrength={0.4}
            repulsivity={300}
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
            annotations={annotations}
          />
        </div>
      ) : null}
    </Box>
  );
};

export default ForkCluster;
