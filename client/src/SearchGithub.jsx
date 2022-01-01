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
import { postSearchGithub, getUserFollowedRepositories } from "./repository";

const Alert = React.forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

const SearchGithub = () => {
  const rows = [
    {
      language: "C++",
      full_name: "tensorflow/tensorflow",
      forks: 82444,
      updated: "2020-08-21 16:03(UTC)",
    },
    {
      language: "JavaScript",
      full_name: "twbs/bootstrap",
      forks: 71700,
      updated: "2021-01-17 22:26(UTC)",
    },
    {
      language: "JavaScript",
      full_name: "nightscout/cgm-remote-monitor",
      forks: 42548,
      updated: "2020-07-25 21:12(UTC)",
    },
    {
      language: "C++",
      full_name: "opencv/opencv",
      forks: 41764,
      updated: "2020-12-23 06:49(UTC)",
    },
    {
      language: "C",
      full_name: "torvalds/linux",
      forks: 33035,
      updated: "2020-08-19 09:24(UTC)",
    },
    {
      language: "Java",
      full_name: "spring-projects",
      forks: 31207,
      updated: "2020-08-27 05:24(UTC)",
    },
  ];

  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);
  const [searchValue, setSearchValue] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  const [error, setError] = useState(null);
  const [searchResults, setSearchResults] = useState(null);
  const [followMsg, setFollowMsg] = useState(null);
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [followedRepos, setFollowedRepos] = useState(null);

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

  useEffect(() => {
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
                            name={result.full_name}
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
        <Table>
          <TableHead></TableHead>
          <TableBody>
            {rows
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map((row) => {
                return (
                  <SearchGithubRow
                    name={row.full_name}
                    forks={row.forks}
                    language={row.language}
                    updated={row.updated}
                  ></SearchGithubRow>
                );
              })}
          </TableBody>
          <TableFooter>
            <TableRow>
              <TablePagination
                rowsPerPageOptions={[5, 10, 15]}
                count={rows.length}
                rowsPerPage={rowsPerPage}
                page={page}
                onPageChange={handleChangePage}
                onRowsPerPageChange={handleChangeRowsPerPage}
              />
            </TableRow>
          </TableFooter>
        </Table>
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
