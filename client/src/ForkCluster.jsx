import React, { useState } from "react";
import { getForkClustering } from "./repository";
import { ResponsiveNetworkCanvas } from "@nivo/network";
import {
  Box,
  Button,
  TextField,
  Grid,
  Checkbox,
  Typography,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from "@mui/material";
import Loading from "./common/Loading";

const ForkCluster = () => {
  const [data, setData] = useState(null);
  const [annotations, setAnnotations] = useState(null);
  const [searchText, setSearchText] = useState("");
  const [loading, setLoading] = useState(false);
  const [analyzeCode, setAnalyzeCode] = useState(true);
  const [analyzeFiles, setAnalyzeFiles] = useState(true);
  const [analyzeCommits, setAnalyzeCommits] = useState(true);
  const [clusterNumber, setClusterNumber] = useState(10);

  const onClickSearch = async (event) => {
    event.preventDefault();
    setLoading(true);

    const searchInfo = {
      repo: searchText,
      analyzeCode: analyzeCode,
      analyzeFiles: analyzeFiles,
      analyzeCommits: analyzeCommits,
      clusterNumber: clusterNumber,
    };

    const response = await getForkClustering(searchInfo);
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
            <Grid item marginTop={1}>
              <Grid container>
                <Grid item>
                  <Grid container>
                    <Grid item>
                      <Checkbox
                        checked={analyzeCode}
                        onChange={(e) => {
                          setAnalyzeCode(e.target.checked);
                        }}
                      />
                    </Grid>
                    <Grid item marginTop={1}>
                      <Typography>Analyze Code Changes</Typography>
                    </Grid>
                  </Grid>
                </Grid>
                <Grid item>
                  <Grid container>
                    <Grid item>
                      <Checkbox
                        checked={analyzeFiles}
                        onChange={(e) => {
                          setAnalyzeFiles(e.target.checked);
                        }}
                      />
                    </Grid>
                    <Grid item marginTop={1}>
                      <Typography>Analyze Files Changed</Typography>
                    </Grid>
                  </Grid>
                </Grid>
                <Grid item>
                  <Grid container>
                    <Grid item>
                      <Checkbox
                        checked={analyzeCommits}
                        onChange={(e) => {
                          setAnalyzeCommits(e.target.checked);
                        }}
                      />
                    </Grid>
                    <Grid item marginTop={1}>
                      <Typography>Analyze Commit Messages</Typography>
                    </Grid>
                  </Grid>
                </Grid>
              </Grid>
            </Grid>
            <Grid item xs={1} marginTop={1} paddingLeft={1}>
              <FormControl fullWidth>
                <InputLabel id="clusterNumber">Clusters</InputLabel>
                <Select
                  id="clusterNumber"
                  label="Clusters"
                  value={clusterNumber}
                  onChange={(e) => {
                    setClusterNumber(e.target.value);
                  }}
                >
                  <MenuItem value={5}>Five</MenuItem>
                  <MenuItem value={10}>Ten</MenuItem>
                  <MenuItem value={15}>Fifteen</MenuItem>
                  <MenuItem value={20}>Twenty</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </form>
      </Box>

      {loading ? (
        <Box height="80vh">
          <Loading loadingMessage="Please wait. This may take a few minutes." />
        </Box>
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
