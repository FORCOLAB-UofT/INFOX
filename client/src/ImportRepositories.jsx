import React, { useEffect, useCallback, useState } from "react";
import { Box, Typography } from "@mui/material";
import isEmpty from "lodash/isEmpty";
import { getUserImportRepositories } from "./repository";
import { LOADING_HEIGHT } from "./common/constants";
import Loading from "./common/Loading";
import Title from "./common/Title";
import SearchAndFilter from "./common/SearchAndFilter";
import ImportRepositoryCard from "./ImportRepositoryCard";
import Button from "@mui/material/Button";
import { PRIMARY, SECONDARY } from "./common/constants";

const ImportRepositories = () => {
  const [importRepositories, setImportRepositories] = useState(null);
  console.log(importRepositories);
  const [isLoading, setIsLoading] = useState(true);
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
    console.log("res", response);

    setIsLoading(false);
  }, []);

  useEffect(() => {
    fetchImportRepositories();
  }, [fetchImportRepositories]);

  useEffect(() => {
    const filteredRepos = [];
    let hasBeenFiltered = false;

    if (
      !!importRepositories &&
      !isEmpty(filtersWithValues) &&
      !isEmpty(filters)
    ) {
      importRepositories.forEach((repo) => {
        let matches = false;
        if (!isEmpty(filters)) {
          hasBeenFiltered = true;
          filters.forEach((filt) => {
            if (repo[filt.key] === filt.value) {
              matches = true;
            }
          });
        }

        if (search !== "" && matches) {
          hasBeenFiltered = true;
          if (!repo.repo.includes(search)) {
            matches = false;
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
  }, [filters, search]);

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
                    repo={repo}
                    language={language}
                    description={description}
                    timesForked={timesForked}
                  />
                )
              )}
            </Box>
          </Box>
        </Box>
      )}
      <Box style={{ textAlign: "right" }}>
        <Button variant="contained" style={{ background: PRIMARY }}>
          Follow
        </Button>
      </Box>
    </Box>
  );
};

export default ImportRepositories;
