import React, { useState } from "react";
import PropTypes from "prop-types";
import {
  Box,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Typography,
  Grid,
  Checkbox,
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import { PRIMARY, SECONDARY, TERTIARY } from "./common/constants";

const ImportRepositoryCard = ({ repo, description, language, timesForked }) => {
  return (
    <Box paddingY={1}>
      <Accordion>
        <AccordionSummary
          style={{ background: SECONDARY }}
          expandIcon={<ExpandMoreIcon sx={{ color: "white" }} />}
        >
          <Grid container direction="row" alignItems="center">
            <Grid item>
              <Checkbox
                style={{ width: "20px", padding: 0, color: "white" }}
                value="checkedB"
                color="primary"
                onClick={(e) => e.stopPropagation()}
                labelStyle={{ color: PRIMARY }}
              />
            </Grid>
            <Grid item sx={{ marginLeft: 1 }}>
              <Typography color="white">{repo}</Typography>
            </Grid>
          </Grid>
        </AccordionSummary>
        <AccordionDetails style={{ background: TERTIARY }}>
          <Grid container>
            <Grid item xs={4}>
              {" "}
              <Typography>Project Description: {description}</Typography>
            </Grid>
            <Grid item xs={4} style={{ textAlign: "center" }}>
              <Typography>Language: {language}</Typography>
            </Grid>
            <Grid item xs={4} style={{ textAlign: "right" }}>
              <Typography>Times Forked: {timesForked}</Typography>
            </Grid>
          </Grid>
        </AccordionDetails>
      </Accordion>
    </Box>
  );
};

ImportRepositoryCard.propTypes = {
  repo: PropTypes.string,
  description: PropTypes.string,
  language: PropTypes.string,
  timesForked: PropTypes.number,
};

export default ImportRepositoryCard;
