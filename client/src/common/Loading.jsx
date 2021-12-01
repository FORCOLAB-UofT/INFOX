import React from "react";
import CircularProgress from "@mui/material/CircularProgress";
import Grid from "@mui/material/Grid";

// TODO: Make it appear only if it will take more than 0.5 seconds to load
const Loading = () => {
  return (
    <Grid
      container
      direction="column"
      alignItems="center"
      justifyContent="center"
      style={{ minHeight: "100%" }}
    >
      <CircularProgress />
    </Grid>
  );
};

export default Loading;
