import React, { useEffect, useCallback, useState } from "react";
import { Box, Typography } from "@mui/material";
import isEmpty from "lodash/isEmpty";
import { getUserFollowedRepositories, getUserImportRepositories } from "./repository";
import { LOADING_HEIGHT } from "./common/constants";
import Loading from "./common/Loading";
import Title from "./common/Title";
import SearchAndFilter from "./common/SearchAndFilter";
import ImportRepositoryCard from "./ImportRepositoryCard";
import Stack from "@mui/material/Stack";
import Snackbar from "@mui/material/Snackbar";
import MuiAlert from "@mui/material/Alert";

const Alert = React.forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

const ImportRepositories = () => {
  const [followMsg, setFollowMsg] = useState(null);
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [importRepositories, setImportRepositories] = useState(null);
  const [followedRepositories, setFollowedRepositories] = useState(null);
  console.log(importRepositories);
  const [isLoading, setIsLoading] = useState(true);
  const [isFetchingImport, setIsFetchingImport] = useState(true);
  const [isFetchingFollowed, setIsFetchingFollowed] = useState(true);
  const [filtersWithValues, setFiltersWithValues] = useState(null);
  const [filters, setFilters] = useState([]);
  const [search, setSearch] = useState("");
  const [filteredRepositories, setFilteredRepositories] =
    useState(importRepositories);
  console.log("filters", filters);
  console.log("search", search);
  console.log("filterswihvalues", filtersWithValues);

  const fetchImportRepositories = useCallback(async () => {
    const response = await getUserImportRepositories();

    setImportRepositories(response.data.importRepositories);
    console.log("imported projects", response);

    setIsFetchingImport(false);
  }, []);

  const fetchFollowedRepositories = useCallback(async () => {
    const response = await getUserFollowedRepositories();
    console.log("followed projects", response);

    setFollowedRepositories(response.data);
    console.log("res", response);

    setIsFetchingFollowed(false);
  }, []);

  useEffect(() => {
    if (!isFetchingImport && !isFetchingFollowed) {
      setIsLoading(false);
    }
  }, [isFetchingFollowed, isFetchingImport]);

  useEffect(() => {
    fetchImportRepositories();
  }, [fetchImportRepositories]);

  useEffect(() => {
    fetchFollowedRepositories();
  }, [fetchFollowedRepositories]);

  useEffect(() => {
    const filteredRepos = [];
    let hasBeenFiltered = false;

    if (!!importRepositories && !isEmpty(filtersWithValues)) {
      importRepositories.forEach((repo) => {
        let matches = false;

        if (!isEmpty(filters)) {
          hasBeenFiltered = true;
          filters.forEach((filt) => {
            if (repo[filt.key] === filt.value) {
              matches = true;
            }
          });
        } else {
          matches = true;
        }

        if (search !== "") {
          hasBeenFiltered = true;
          if (!repo.repo.includes(search)) {
            matches = false;
          } else {
            matches = true;
          }
        }

        if (matches) {
          filteredRepos.push(repo);
        }
      });

      setFilteredRepositories(filteredRepos);
    } else {
      setFilteredRepositories(importRepositories);
    }
  }, [filters, search, importRepositories]);

  useEffect(() => {
    if (!isEmpty(importRepositories)) {
      const initialFilters = {
        language: {
          key: "language",
          display: "Language",
          type: "string",
          values: [],
        },
        timesForked: {
          key: "timesForked",
          display: "Times Forked",
          type: "numeric",
          values: [],
        },
      };
      importRepositories.forEach(({ language, timesForked }) => {
        if (!initialFilters.language.values.some((item) => item === language)) {
          initialFilters.language.values.push(language);
        }
        if (
          !initialFilters.timesForked.values.some(
            (item) => item === timesForked
          )
        ) {
          initialFilters.timesForked.values.push(timesForked);
        }
      });

      setFiltersWithValues(initialFilters);
    }
  }, [importRepositories]);

  return (
    <Box>
      {isLoading ? (
        <Box height={LOADING_HEIGHT}>
          <Loading />
        </Box>
      ) : (
        <Box width="100%">
          <Title text="Import Repositories" />
          <Box paddingLeft="4px">
            {!isEmpty(importRepositories) ? (
              <>
                <Box>
                  <SearchAndFilter
                    filters={filtersWithValues}
                    setFilters={(data) => {
                      setFilters(data);
                    }}
                    setSearch={(data) => {
                      setSearch(data);
                    }}
                  />
                </Box>
                <Box>
                  {filteredRepositories?.map(
                    ({ repo, language, description, updated, timesForked }) => (
                      <ImportRepositoryCard
                        key={repo}
                        name={repo}
                        language={language}
                        description={description}
                        timesForked={timesForked}
                        onFollow={(data) => {
                          setFollowMsg(data.msg);
                          setOpenSnackbar(true);
                          setFollowedRepositories([...followedRepositories, data.repo]);
                        }}
                        onRemoveRepo={(value) => {
                          setFollowedRepositories(
                            followedRepositories.filter(
                              (repo) => repo.repo !== value
                            )
                          );
                        }}
                        followedRepos={followedRepositories}
                      />
                    )
                  )}
                </Box>
              </>
            ) : (
              <>
                <Box>
                  <Typography variant="h5" textAlign="center">No public repositories found in account.</Typography>
                </Box>
              </>
            )}
          </Box>
        </Box>
      )}
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

export default ImportRepositories;