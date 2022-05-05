import React, { useState } from "react";
import { getForkClustering } from "./repository";
import { ResponsiveNetworkCanvas } from "@nivo/network";
import ReactWordcloud from "react-wordcloud";
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
import FilterBubble from "./common/SearchAndFilter";
import { isEmpty, words } from "lodash";
import Bubble from "./Bubble";

const options = {
  colors: ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"],
  enableTooltip: true,
  deterministic: false,
  fontSizes: [20, 100],
  fontStyle: "normal",
  fontWeight: "normal",
  padding: 1,
  rotations: 3,
  rotationAngles: [0],
  scale: "sqrt",
  spiral: "archimedean",
  transitionDuration: 1000,
};

const ForkCluster = () => {
  const [data, setData] = useState(null);
  const [annotations, setAnnotations] = useState(null);
  const [searchText, setSearchText] = useState("");
  const [loading, setLoading] = useState(false);
  const [analyzeCode, setAnalyzeCode] = useState(true);
  const [analyzeFiles, setAnalyzeFiles] = useState(true);
  const [analyzeCommits, setAnalyzeCommits] = useState(true);
  const [clusterNumber, setClusterNumber] = useState(10);
  const [userInputWords, setUserInputWords] = useState([]);
  const [userInputEx, setUserInputEx] = useState("");
  const [wordcloudWords, setWordcloudWords] = useState({});
  const [error, setError] = useState(false);

  const onClickSearch = async (event) => {
    event.preventDefault();
    setLoading(true);

    const searchInfo = {
      repo: searchText,
      analyzeCode: analyzeCode,
      analyzeFiles: analyzeFiles,
      analyzeCommits: analyzeCommits,
      clusterNumber: clusterNumber,
      userInputWords: userInputWords,
    };

    try {
      const response = await getForkClustering(searchInfo);
      console.log("resp", response);

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
      let wordcloud_words = {};
      wordcloud_words = response.data.wordcloud.map((x) => ({
        text: x.slice(0)[0],
        value: x.slice(-1)[0].length,
      }));
      setWordcloudWords(wordcloud_words);
      setError(false);
    } catch {
      setError(true);
    }
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
          <Box>
            <Grid container>
              <Grid item paddingRight={1}>
                <TextField
                  variant="standard"
                  label="Exclude Key Words"
                  value={userInputEx}
                  onChange={(event) => {
                    setUserInputEx(event.target.value);
                  }}
                />
              </Grid>
              <Grid item marginTop={1}>
                <Button
                  variant="contained"
                  type="submit"
                  onClick={(event) => {
                    setUserInputWords([...userInputWords, userInputEx]);
                    setUserInputEx("");
                  }}
                >
                  Add
                </Button>
              </Grid>
              <Grid container>
                {!isEmpty(userInputWords) ? (
                  <Grid container>
                    {userInputWords.map((value) => {
                      return (
                        <Bubble
                          value={value}
                          onClickRemoveFilter={() => {
                            setUserInputWords(
                              userInputWords.filter((word) => word !== value)
                            );
                          }}
                        />
                      );
                    })}
                  </Grid>
                ) : null}
              </Grid>
            </Grid>
          </Box>
        </form>
      </Box>

      {loading ? (
        <Box height="80vh">
          <Loading loadingMessage="Please wait. This may take a few minutes." />
        </Box>
      ) : error ? (
        <Box>
          We started clustering this repository! This might take a while so try again in a few minutes.
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
          <Grid>
            <ReactWordcloud options={options} words={wordcloudWords} />
          </Grid>
        </div>
      ) : null}
    </Box>
  );
};

export default ForkCluster;
