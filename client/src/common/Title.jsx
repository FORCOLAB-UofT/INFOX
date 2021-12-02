import React from "react";
import PropTypes from "prop-types";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import { DARK } from "./constants";

const Title = ({ text }) => {
  return (
    <Grid container direction="column" alignItems="center">
      <Grid item>
        <Box fontStyle="italic">
          <Typography variant="h3" color={DARK}>
            {text}
          </Typography>
        </Box>
      </Grid>
    </Grid>
  );
};

Title.propTypes = {
  text: PropTypes.string,
};

export default Title;
