import React, { useState, useEffect, useCallback } from "react";
import Box from "@mui/material/Box";
import {
  Button,
  TextField,
  Typography,
  TableHead,
  TableRow,
  Table,
  TableBody,
  TableFooter,
  TablePagination,
  Grid,
  CircularProgress,
} from "@mui/material";
import Snackbar from "@mui/material/Snackbar";
import MuiAlert from "@mui/material/Alert";
import Stack from "@mui/material/Stack";
import SearchGithubRow from "./SearchGithubRow";
import { postSearchGithub, getUserFollowedRepositories, fetchFreqForkRepos } from "./repository";
import { useNavigate } from "react-router";

const Alert = React.forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

const SearchGithub = () => {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);
  const [searchValue, setSearchValue] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  const [isSearching_freq, setIsSearching_freq] = useState(false);
  const [error, setError] = useState(null);
  const [searchResults, setSearchResults] = useState(null);
  const [followMsg, setFollowMsg] = useState(null);
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [followedRepos, setFollowedRepos] = useState(null);
  const [freqRepos, setfreqRepos] = useState([]);
  const [starRepos, setstarRepos] = useState([]);
  const [isSearching_star, setIsSearching_star] = useState(false);

  const navigate = useNavigate();

  const navigateToFork = (repo) => {
    console.log("repo nav", repo);
    navigate(`/forks/${repo}`, { replace: true });
  };

  const freqReposFunc = async (searchValues) => {
    setIsSearching_freq(true);
    var results = [];
    for (var i = 0; i < searchValues.length; i++) {
      var resp = await postSearchGithub(searchValues[i]);
      var temp = resp.data.slice(0, 1);
      results = results.concat(temp);
    }
    setfreqRepos(results);
    setIsSearching_freq(false);
  };

  const starReposFunc = async (searchValues) => {
    setIsSearching_star(true);
    var results = [];
    for (var i = 0; i < searchValues.length; i++) {
      var resp = await postSearchGithub(searchValues[i]);
      var temp = resp.data.slice(0, 1);
      results = results.concat(temp);
    }
    setstarRepos(results);
    setIsSearching_star(false);
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const onClickSearch = async (event) => {
    event.preventDefault();
    if (searchValue.length === 0) {
      setError("Please enter a value!");
      return;
    } else {
      setError(null);
    }

    setIsSearching(true);
    console.log("values", searchValue);
    const resp = await postSearchGithub(searchValue);
    console.log("resp", resp);
    setSearchResults(resp.data);
    setIsSearching(false);
  };

  const fetchUserFollowedRepos = useCallback(async () => {
    const res = await getUserFollowedRepositories();
    setFollowedRepos(res.data);
  }, []);

  const init_state = async () => {
    if (!isSearching) {
      const repos = [];
      const star_repos = [];
      const topForksDB = `https://api.github.com/search/repositories?q=forks:%3E0&sort=forks&per_page=5`;
      const topStarsDB = `https://api.github.com/search/repositories?q=forks:%3E0&sort=stars&per_page=5`;
      const fetchRepos = await fetchFreqForkRepos(topForksDB);
      const fetchStarRepos = await fetchFreqForkRepos(topStarsDB);
      for(let i = 0; i < fetchRepos.length; i++) {
        repos.push(fetchRepos[i].full_name);
        star_repos.push(fetchStarRepos[i].full_name);
      }
      freqReposFunc(repos);
      starReposFunc(star_repos);
    }
  };

  useEffect(() => {
    init_state();
    fetchUserFollowedRepos();
  }, [fetchUserFollowedRepos]);

  return (
    <Box sx={{ display: "flex", flexDirection: "column" }}>
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          borderBottom: 1,
          padding: 3,
        }}
      >
        <Typography variant="h5" sx={{ marginTop: 1 }}>
          Search on GitHub
        </Typography>
        <form onSubmit={onClickSearch}>
          <Grid container alignItems="center" paddingBottom={1}>
            <Grid item paddingRight={1}>
              <TextField
                variant="standard"
                label="Repository"
                value={searchValue}
                onChange={(event) => {
                  setSearchValue(event.target.value);
                }}
              ></TextField>
            </Grid>
            <Grid item marginTop={1}>
              <Button variant="contained" type="submit">
                Search
              </Button>
            </Grid>
          </Grid>
        </form>
        {error && (
          <Typography variant="caption" color="red">
            {error}
          </Typography>
        )}
        <Box>
          {isSearching ? (
            <Grid
              container
              direction="column"
              alignItems="center"
              justifyContent="center"
            >
              <CircularProgress />
            </Grid>
          ) : (
            <Box>
              {searchResults ? (
                <Box>
                  <Table>
                    <TableHead />
                    <TableBody>
                      {searchResults.map((result) => {
                        return (
                          <SearchGithubRow
                            name={<a style={{cursor: "pointer"}} onClick={() => {
                              console.log("repo nav", result.full_name);
                              navigateToFork(result.full_name)}
                            }>{result.full_name}</a>}
                            language={result.language}
                            forks={result.forks}
                            updated={result.updated_at}
                            onFollow={(data) => {
                              setFollowMsg(data.msg);
                              setOpenSnackbar(true);
                              setFollowedRepos([...followedRepos, data.repo]);
                            }}
                            followedRepos={followedRepos}
                            onRemoveRepo={(value) => {
                              setFollowedRepos(
                                followedRepos.filter(
                                  (repo) => repo.repo !== value
                                )
                              );
                            }}
                          />
                        );
                      })}
                    </TableBody>
                  </Table>
                </Box>
              ) : null}
            </Box>
          )}
        </Box>
      </Box>
      <Box sx={{ display: "flex", flexDirection: "column", padding: 3 }}>
        <Typography variant="h5">Frequently Analyzed Repos on INFOX</Typography>
        {isSearching_freq ? (
          <Grid
            container
            direction="column"
            alignItems="center"
            justifyContent="center"
          >
            <CircularProgress />
          </Grid>
        ) : (
          <Box>
            {freqRepos ? (
              <Box>
                <Table>
                  <TableHead />
                  <TableBody>
                    {freqRepos.map((result) => {
                      return (
                        <SearchGithubRow
                          name={<a style={{cursor: "pointer"}} onClick={() => {
                            console.log("repo nav", result.full_name);
                            navigateToFork(`${result.full_name}`)}
                          }>{result.full_name}</a>}
                          language={result.language}
                          forks={result.forks}
                          updated={result.updated_at}
                          onFollow={(data) => {
                            setFollowMsg(data.msg);
                            setOpenSnackbar(true);
                            setFollowedRepos([...followedRepos, data.repo]);
                          }}
                          followedRepos={followedRepos}
                          onRemoveRepo={(value) => {
                            setFollowedRepos(
                              followedRepos.filter(
                                (repo) => repo.repo !== value
                              )
                            );
                          }}
                        />
                      );
                    })}
                  </TableBody>
                </Table>
              </Box>
            ) : null}
          </Box>
        )}
      </Box>

      <Box sx={{ display: "flex", flexDirection: "column", padding: 3 }}>
        <Typography variant="h5">Starred Repos</Typography>
        {isSearching_star ? (
          <Grid
            container
            direction="column"
            alignItems="center"
            justifyContent="center"
          >
            <CircularProgress />
          </Grid>
        ) : (
          <Box>
            {starRepos ? (
              <Box>
                <Table>
                  <TableHead />
                  <TableBody>
                    {starRepos.map((result) => {
                      return (
                        <SearchGithubRow
                          name={<a style={{cursor: "pointer"}} onClick={() => {
                            console.log("repo nav", result.full_name);
                            navigateToFork(`${result.full_name}`)}
                          }>{result.full_name}</a>}
                          language={result.language}
                          forks={result.forks}
                          updated={result.updated_at}
                          onFollow={(data) => {
                            setFollowMsg(data.msg);
                            setOpenSnackbar(true);
                            setFollowedRepos([...followedRepos, data.repo]);
                          }}
                          followedRepos={followedRepos}
                          onRemoveRepo={(value) => {
                            setFollowedRepos(
                              followedRepos.filter(
                                (repo) => repo.repo !== value
                              )
                            );
                          }}
                        />
                      );
                    })}
                  </TableBody>
                </Table>
              </Box>
            ) : null}
          </Box>
        )}
      </Box>

      <Stack spacing={2} sx={{ width: "100%" }}>
        <Snackbar
          open={openSnackbar}
          autoHideDuration={6000}
          onClose={(event, reason) => {
            if (reason === "clickaway") {
              return;
            }

            setOpenSnackbar(false);
          }}
        >
          <Alert
            onClose={(event, reason) => {
              if (reason === "clickaway") {
                return;
              }

              setOpenSnackbar(false);
            }}
            severity="success"
            sx={{ width: "100%" }}
          >
            {followMsg}
          </Alert>
        </Snackbar>
      </Stack>
    </Box>
  );
};

export default SearchGithub;
