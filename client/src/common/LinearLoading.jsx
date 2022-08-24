import React from "react";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import LinearProgress, { LinearProgressProps } from '@mui/material/LinearProgress';

function LinearProgressWithLabel({value}) {
  return (
    <Box sx={{ display: 'flex', alignItems: 'center' }}>
      <Box sx={{ width: '100%', mr: 1 }}>
        <LinearProgress variant="determinate" />
      </Box>
      <Box sx={{ minWidth: 35 }}>
        <Typography variant="body2" color="text.secondary">{`${Math.round(
          value,
        )}%`}</Typography>
      </Box>
    </Box>
  );
}

const LinearLoading = ({ 
  loadingMessage, 
  progress 
}) => {
  return (
    <Grid
      container
      direction="column"
      alignItems="center"
      justifyContent="center"
      style={{ minHeight: "100%", paddingTop: 50}}
    >
      <LinearProgressWithLabel value={progress}/>
      <Box>
        {loadingMessage ? (
          <Typography variant="h6">{loadingMessage}</Typography>
        ) : null}
      </Box>
    </Grid>
  );
};

LinearLoading.defaultProps = {
  loadingMessage: null,
};

export default LinearLoading;