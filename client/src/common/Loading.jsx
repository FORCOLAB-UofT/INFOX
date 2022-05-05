import React from "react";
import CircularProgress from "@mui/material/CircularProgress";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";

// TODO: Make it appear only if it will take more than 0.5 seconds to load
const Loading = ({ loadingMessage }) => {
  return (
    <Grid
      container
      direction="column"
      alignItems="center"
      justifyContent="center"
      style={{ minHeight: "100%" }}
    >
      <CircularProgress />
      <Box>
        {loadingMessage ? (
          <Typography variant="h6">{loadingMessage}</Typography>
        ) : null}
      </Box>
    </Grid>
  );
};

Loading.defaultProps = {
  loadingMessage: null,
};

export default Loading;
