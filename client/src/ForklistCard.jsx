import React, { useEffect, useCallback, useState } from "react";
import PropTypes from "prop-types";
import {
  Box,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Typography,
  Grid,
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import { SECONDARY, TERTIARY } from "./common/constants";
import { getRepoForks } from "./repository";
import { Button } from "@mui/material";

const ForklistCard = ({
  name,
  numChangedFiles,
  numChangedLines,
  totalCommits,
}) => {
  const [expanded, setExpanded] = useState(true);

  return (
    <Box paddingTop={2}>
      <Accordion expanded={expanded}>
        <AccordionSummary
          onClick={() => {
            setExpanded(!expanded);
          }}
          style={{ background: SECONDARY }}
          expandIcon={<ExpandMoreIcon sx={{ color: "white" }} />}
        >
          <Grid container direction="row" alignItems="center">
            <Grid item xs={11}>
              <Typography color="white">{name}</Typography>
            </Grid>
            <Grid item xs={1}>
              <Box style={{ textAlign: "right" }}>
                <Button />
              </Box>
            </Grid>
          </Grid>
        </AccordionSummary>
        <AccordionDetails style={{ background: TERTIARY }}>
          <Box>
            <Grid container>
              <Grid item xs={4}>
                <Typography>
                  Number of Changed Files: {numChangedFiles}
                </Typography>
              </Grid>
              <Grid item xs={4} style={{ textAlign: "center" }}>
                <Typography>
                  Number of Changed Lines: {numChangedLines}
                </Typography>
              </Grid>
              <Grid item xs={4} style={{ textAlign: "center" }}>
                <Typography>Number of Commits: {totalCommits}</Typography>
              </Grid>
            </Grid>
          </Box>
          <Box>
            <Grid container>
              <Grid item xs={6}>
                <Typography>Tags: </Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography>Key Words:</Typography>
              </Grid>
            </Grid>
          </Box>
        </AccordionDetails>
      </Accordion>
    </Box>
  );
};

export default ForklistCard;
