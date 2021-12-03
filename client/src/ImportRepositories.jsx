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
  const [filteredRepositories, setFilteredRepositories] = useState(importRepositories);
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

    if (!!importRepositories && !isEmpty(filtersWithValues)) {
      importRepositories.forEach((repo) => {
        let matches = true;
        if (!isEmpty(filters)) {
          hasBeenFiltered = true;
          filters.forEach((filt) => {
            if (repo[filt.key] !== filt.value) {
              matches = false;
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
        updated: {
          key: "updated",
          display: "Last Updated",
          type: "date",
          values: [],
        },
      };
      importRepositories.forEach(({ language, timesForked, updated }) => {
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
        if (!initialFilters.updated.values.some((item) => item === updated)) {
          initialFilters.updated.values.push(updated);
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
                    updated={updated}
                    timesForked={timesForked}
                  />
                )
              )}
            </Box>
          </Box>
        </Box>
      )}
      <Box style={{textAlign:"right"}}>
         <Button variant="contained" style={{background: PRIMARY}}>Follow</Button>
      </Box>
    </Box>
  );
};

export default ImportRepositories;
// import React, { useEffect, useCallback, useState } from "react";
// import { Box, Grid, Checkbox, ListItem } from "@mui/material";
// import { getUserImportedRepositories } from "./repository";
// import { LOADING_HEIGHT } from "./common/constants";
// import Loading from "./common/Loading";
// import Accordion from "@mui/material/Accordion";
// import AccordionSummary from "@mui/material/AccordionSummary";
// import AccordionDetails from "@mui/material/AccordionDetails";
// import Typography from "@mui/material/Typography";
// import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
// import Stack from "@mui/material/Stack";
// import Button from "@mui/material/Button";

// const ImportRepositories = () => {
//   const [importedRepositories, setImportedRepositories] = useState(null);
//   const [isLoading, setIsLoading] = useState(true);

//   const fetchImportedRepositories = useCallback(async () => {
//     const response = await getUserImportedRepositories();

//     setImportedRepositories(response.data.importRepositories);
//     console.log("res", response);

//     setIsLoading(false);
//   }, []);

//   useEffect(() => {
//     fetchImportedRepositories();
//   }, [fetchImportedRepositories]);

//   return (
//     <Box>
//       {isLoading ? (
//         <Box height={LOADING_HEIGHT}>
//           <Loading />
//         </Box>
//       ) : (
//         <Box>
//           {importedRepositories.map((item) => (
//             <Accordion key={item.repo}>
//               <AccordionSummary
//                 expandIcon={<ExpandMoreIcon />}
//                 aria-controls="panel1a-content"
//                 id="panel1a-header"
//               >
//                 <Grid item xs={1}>
//                   <Checkbox
//                     value="checkedB"
//                     color="primary"
//                     onClick={(e) => e.stopPropagation()}
//                   />
//                 </Grid>
//                 <Grid item xs={2}>
//                   <Typography className="repoName">{item.repo}</Typography>
//                 </Grid>
//               </AccordionSummary>
//               <AccordionDetails>
//                 <Typography>
//                   Description: {item.description} <br />
//                   Language: {item.language} <br />
//                   Times this repository was forked: {item.timesForked} <br />
//                   Updated: {item.updated}
//                 </Typography>
//               </AccordionDetails>
//             </Accordion>
//           ))}
//         </Box>
//       )}
//       <Box style={{textAlign:"right"}}>
//         <Button variant="contained">Follow</Button>
//       </Box>
//     </Box>
//   );
// };

// export default ImportRepositories;
