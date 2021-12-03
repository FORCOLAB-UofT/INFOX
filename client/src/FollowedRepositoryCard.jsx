import React, { useState } from "react";
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

const FollowedRepositoryCard = ({
  repo,
  description,
  language,
  timesForked,
  updated,
}) => {
  return (
    <Box paddingY={1}>
      <Accordion>
        <AccordionSummary
          style={{ background: SECONDARY }}
          expandIcon={<ExpandMoreIcon sx={{ color: "white" }} />}
        >
          <Typography color="white">{repo}</Typography>
        </AccordionSummary>
        <AccordionDetails style={{ background: TERTIARY }}>
          <Grid container>
            <Grid item xs={4}>
              <Typography>Language: {language}</Typography>
            </Grid>
            <Grid item xs={4} style={{ textAlign: "center" }}>
              <Typography>Times Forked: {timesForked}</Typography>
            </Grid>
            <Grid item xs={4} style={{ textAlign: "right" }}>
              <Typography>Last Updated: {updated}</Typography>
            </Grid>
          </Grid>
          <Typography>Project Description: {description}</Typography>
        </AccordionDetails>
      </Accordion>
    </Box>
  );
};

FollowedRepositoryCard.propTypes = {
  repo: PropTypes.string,
  description: PropTypes.string,
  language: PropTypes.string,
  timesForked: PropTypes.number,
  lastUpdated: PropTypes.string,
};

export default FollowedRepositoryCard;
