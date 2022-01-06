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
  Button,
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import { PRIMARY, SECONDARY, TERTIARY, REMOVE } from "./common/constants";
import { postFollowRepository, deleteUserRepository } from "./repository";

const ImportRepositoryCard = ({ name, description, language, timesForked, followedRepos, onFollow, onRemoveRepo }) => {

  const [isLoading, setIsLoading] = useState(false);
  return (
    <Box paddingY={1}>
      <Accordion>
        <AccordionSummary
          style={{ background: SECONDARY }}
          expandIcon={<ExpandMoreIcon sx={{ color: "white" }} />}
        >
          <Grid container direction="row" alignItems="center">
            
            <Grid item xs={11}>
              <Typography color="white">{name}</Typography>
            </Grid>
            <Grid item xs={1}>
              {!followedRepos?.some((repo) => repo.repo === name) ? (
                <Button
                  variant="outlined"
                  onClick={async (event) => {
                    event.stopPropagation();
                    setIsLoading(true);
                    const res = await postFollowRepository(name);
                    console.log("res", res);
                    onFollow(res.data);
                    setIsLoading(false);
                  }}
                  style={{ color: PRIMARY, background: REMOVE }}
                  disabled={isLoading}
                >
                  {isLoading ? "Following..." : "Follow"}
                </Button>
              ) : (
                <Button
                  variant="contained"
                  color="error"
                  onClick={(event) => {
                    event.stopPropagation();
                    deleteUserRepository(name);
                    onRemoveRepo(name);
                  }}
                >
                  Remove
                </Button>
              )}
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
