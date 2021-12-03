import React, { useState } from "react";
import PropTypes from "prop-types";
import {
  Box,
  Button,
  Divider,
  Typography,
  TextField,
  Grid,
  ButtonBase,
  Popover,
  Checkbox,
  IconButton,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import SearchIcon from "@mui/icons-material/Search";
import CancelIcon from "@mui/icons-material/Cancel";
import InputAdornment from "@mui/material/InputAdornment";
import { SECONDARY, TERTIARY } from "./constants";
import isEmpty from "lodash/isEmpty";
import differenceWith from "lodash/differenceWith";
import { isEqual } from "lodash";

const SearchAndFilter = ({ filters }) => {
  const [anchorEl, setAnchorEl] = useState(null);
  const [checkedFilter, setCheckedFilter] = useState(null);
  const [checkedFilterValues, setCheckedFilterValues] = useState([]);
  const [addedFilters, setAddedFilters] = useState([]);

  console.log("filters", filters);
  console.log("added filters", addedFilters);

  const onClickAddFilter = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClosePopover = () => {
    setAnchorEl(null);
  };

  const onClickFilterName = (filter) => {
    setCheckedFilterValues([]);
    if (checkedFilter && checkedFilter.display === filter.display) {
      setCheckedFilter(null);
    } else {
      setCheckedFilter(filter);
    }
  };

  const onClickFilterValue = (filterValue) => {
    if (checkedFilterValues.some((item) => item === filterValue)) {
      const filteredArray = checkedFilterValues.filter(
        (item) => item !== filterValue
      );
      setCheckedFilterValues(filteredArray);
    } else {
      setCheckedFilterValues([...checkedFilterValues, filterValue]);
    }
  };

  const onClickAddFilters = () => {
    const filtersSelected = checkedFilterValues.map((item) => ({
      display: checkedFilter.display,
      value: item,
      type: checkedFilter.type,
    }));

    const newSelected = differenceWith(filtersSelected, addedFilters, isEqual);

    setAddedFilters([...addedFilters, ...newSelected]);
  };

  const onClickRemoveFilter = (filter, value) => {
    console.log("filter, value", filter, value);
    setAddedFilters(
      addedFilters.filter(
        (item) => !(item.display === filter && item.value === value)
      )
    );
  };

  const FilterBubble = ({ filter, value }) => {
    return (
      <Grid item>
        <Box
          sx={{ border: 4, borderRadius: 12 }}
          style={{ borderColor: SECONDARY, background: TERTIARY }}
        >
          <Grid container direction="row" alignItems="center">
            <Grid item>
              <IconButton
                onClick={() => {
                  onClickRemoveFilter(filter, value);
                }}
              >
                <CancelIcon />
              </IconButton>
            </Grid>
            <Grid item>
              <Box fontWeight="bold">
                <Typography>
                  {filter}: {value}
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </Box>
      </Grid>
    );
  };

  return (
    <Box>
      <Grid
        container
        direction="row"
        justifyContent="flex-start"
        alignItems="center"
        spacing={1}
      >
        <Grid item>
          <Typography variant="h5">Search by name</Typography>
        </Grid>
        <Grid item>
          <TextField
            placeholder="Search"
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
          />
        </Grid>
        <Grid item>
          <Box
            sx={{ border: 4, borderRadius: 12 }}
            style={{ borderColor: SECONDARY, background: TERTIARY }}
            padding={1}
          >
            <ButtonBase onClick={onClickAddFilter}>
              <Grid container direction="row" alignItems="center">
                <Grid item>
                  <AddIcon />
                </Grid>
                <Grid item>
                  <Box fontWeight="bold">
                    <Typography>Add Filter</Typography>
                  </Box>
                </Grid>
              </Grid>
            </ButtonBase>
          </Box>
          <Popover
            anchorEl={anchorEl}
            open={!!anchorEl}
            id={!!anchorEl ? "simple-popover" : undefined}
            onClose={handleClosePopover}
            anchorOrigin={{
              vertical: "bottom",
              horizontal: "left",
            }}
          >
            <Box sx={{ border: 4 }} style={{ borderColor: SECONDARY }}>
              <Box fontStyle="italic">
                <Typography>Filter by</Typography>
              </Box>
              <Grid container spacing={1}>
                <Grid item>
                  <Box sx={{ display: "flex" }}>
                    <Box
                      paddingRight={1}
                      style={{ overflow: "auto", maxHeight: "200px" }}
                    >
                      {Object.values(filters).map((filter) => (
                        <Grid
                          container
                          direction="row"
                          alignItems="center"
                          key={filter.display}
                        >
                          <Grid item>
                            <Checkbox
                              onChange={() => {
                                onClickFilterName(filter);
                              }}
                              checked={
                                checkedFilter?.display === filter.display
                              }
                            />
                          </Grid>
                          <Grid item>
                            <Typography>{filter.display}</Typography>
                          </Grid>
                        </Grid>
                      ))}
                    </Box>
                    <Divider orientation="vertical" flexItem />
                  </Box>
                </Grid>
                <Grid item>
                  {!checkedFilter ? (
                    <Box>Select a filter from the left side</Box>
                  ) : (
                    <Box
                      paddingRight={1}
                      style={{ overflow: "auto", maxHeight: "200px" }}
                    >
                      {checkedFilter.type === "string"
                        ? checkedFilter.values.map((value) => (
                            <Grid
                              container
                              direction="row"
                              alignItems="center"
                              key={value}
                            >
                              <Grid item>
                                <Checkbox
                                  onChange={() => {
                                    onClickFilterValue(value);
                                  }}
                                  checked={checkedFilterValues.some(
                                    (item) => item === value
                                  )}
                                />
                              </Grid>
                              <Grid item>
                                <Typography>{value}</Typography>
                              </Grid>
                            </Grid>
                          ))
                        : "WAIT"}
                    </Box>
                  )}
                </Grid>
              </Grid>
              <Box>
                <Button
                  variant="contained"
                  disabled={isEmpty(checkedFilterValues)}
                  onClick={onClickAddFilters}
                >
                  Add Filters
                </Button>
              </Box>
            </Box>
          </Popover>
        </Grid>
        <Grid container direction="row" spacing={1}>
          {addedFilters.map((filt) => (
            <FilterBubble filter={filt.display} value={filt.value} />
          ))}
        </Grid>
      </Grid>
    </Box>
  );
};

SearchAndFilter.propTypes = {
  filters: PropTypes.object,
};

export default SearchAndFilter;
