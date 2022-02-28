import React, { useEffect, useCallback, useState } from "react";
import PropTypes from "prop-types";
import {
  Box,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Typography,
  Grid,
  Table,
  TableHead,
  TableBody
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import { SECONDARY, TERTIARY } from "./common/constants";
import { getRepoForks } from "./repository";
import { Button } from "@mui/material";
import { useRecoilValue, useSetRecoilState } from "recoil";
import { repoState } from "./recoil/atoms";
import ForklistCard from "./ForklistCard";

const Forklist = () => {

  const setRepo = useSetRecoilState(repoState);
  const repo = useRecoilValue(repoState);
  const [forklist, setForklist] = useState(null)

  const fetchRepoForks = useCallback(async () => {
    console.log("Repo: ", repo)
    const res = await getRepoForks(repo);
    console.log("Fork list api GET response: ", res)
    setForklist(res.data);
    console.log("Fork list: ", forklist)
    
  }, []);

  useEffect(() => {
    fetchRepoForks();
  }, [fetchRepoForks]);
  return (
    <Box>
      <Table>
        <TableHead />
        <TableBody>
          {forklist?.forks.map( fork => {
            return (
              <ForklistCard
                name={fork.fork_name}
                numChangedFiles={fork.num_changed_files}
                numChangedLines={fork.num_changed_lines}
              />
            );
          })}
        </TableBody>
      </Table>
    </Box>
  );
};

export default Forklist;
