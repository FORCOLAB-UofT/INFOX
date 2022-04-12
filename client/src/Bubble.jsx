import React from "react";
import {
    Box,
    Button,
    TextField,
    Grid,
    Checkbox,
    Typography,
    Select,
    MenuItem,
    FormControl,
    InputLabel,
    IconButton,
  } from "@mui/material";

import AddIcon from "@mui/icons-material/Add";
import SearchIcon from "@mui/icons-material/Search";
import CancelIcon from "@mui/icons-material/Cancel";
import InputAdornment from "@mui/material/InputAdornment";
import { SECONDARY, TERTIARY } from "./common/constants";
import isEmpty from "lodash/isEmpty";
import differenceWith from "lodash/differenceWith";
import { isEqual } from "lodash";


const Bubble = ({onClickRemoveFilter,value}) => {

    return (
        <Grid item>
          <Box
            sx={{ border: 4, borderRadius: 12 }}
            style={{ borderColor: SECONDARY, background: TERTIARY }}
            padding={1}
          >
            <Grid container direction="row" alignItems="center">
              <Grid item>
                <IconButton
                  onClick={() => {
                    onClickRemoveFilter(value);
                  }}
                >
                  <CancelIcon />
                </IconButton>
              </Grid>
              <Grid item>
                <Box fontWeight="bold">
                  <Typography>
                    {value}
                  </Typography>
                </Box>
              </Grid>
            </Grid>
          </Box>
        </Grid>
      );
}



export default Bubble;