import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import {
    Box,
    Button,
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

const Filter = ({ filters, setFilters, setSearch, externalKeyword, externalFileName }) => {
    const [anchorEl, setAnchorEl] = useState(null);
    const [checkedFilter, setCheckedFilter] = useState(null);
    const [checkedFilterValues, setCheckedFilterValues] = useState([]);
    const [addedFilters, setAddedFilters] = useState([]);
    const [searchTerm, setSearchTerm] = useState("");

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
            key: checkedFilter.key,
        }));

        const newSelected = differenceWith(filtersSelected, addedFilters, isEqual);

        setAddedFilters([...addedFilters, ...newSelected]);
    };

    const onClickRemoveFilter = (filter, value) => {
        setAddedFilters(
            addedFilters.filter(
                (item) => !(item.display === filter && item.value === value)
            )
        );
    };

    useEffect(() => {
        if (externalFileName) {
            setAddedFilters([...addedFilters, ...externalFileName]);
            console.log("External file name:", externalFileName)
        }
    }, [externalFileName]);

    useEffect(() => {
        if (externalKeyword) {
            setAddedFilters([...addedFilters, ...externalKeyword]);
            console.log("External keyword name", externalKeyword)
        }
    }, [externalKeyword]);

    useEffect(() => {
        setFilters(addedFilters);
    }, [addedFilters, setFilters]);

    useEffect(() => {
        setSearch(searchTerm);
    }, [searchTerm, setSearch]);

    const FilterBubble = ({ filter, value }) => {
        // TODO: Even out padding on both sides of the bubble
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
                    {/* <Typography variant="h5">Add a filter</Typography> */}
                </Grid>
                <Grid item>
                    {/* <TextField
                        onChange={(e) => {
                            setSearchTerm(e.target.value);
                        }}
                        placeholder="Search"
                        InputProps={{
                            startAdornment: (
                                <InputAdornment position="start">
                                    <SearchIcon />
                                </InputAdornment>
                            ),
                        }}
                    /> */}
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
                        <Box
                            sx={{ border: 4 }}
                            style={{ borderColor: SECONDARY }}
                            padding={1}
                        >
                            <Box paddingBottom={1}>
                                <Typography variant="h5">Filter by</Typography>
                            </Box>
                            <Grid container spacing={1} padding={1}>
                                <Grid item border={1} style={{ borderColor: SECONDARY }}>
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
                                    </Box>
                                </Grid>
                                <Grid
                                    item
                                    paddingRight={1}
                                    border={1}
                                    style={{ borderColor: SECONDARY }}
                                >
                                    {!checkedFilter ? (
                                        <Box paddingTop={1}>
                                            <Typography>
                                                Select a filter from the left side
                                            </Typography>
                                        </Box>
                                    ) : (
                                        <Box
                                            paddingRight={1}
                                            style={{ overflow: "auto", maxHeight: "200px" }}
                                        >
                                            {checkedFilter.values.map((value) => (
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
                                            ))}
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
                <Grid container direction="row" spacing={1} marginLeft={2} marginTop={1} marginBottom={1}>
                    {addedFilters.map((filt) => (
                        <FilterBubble
                            filter={filt.display}
                            value={filt.value}
                            key={`${filt.display}+${filt.value}`}
                        />
                    ))}
                </Grid>
            </Grid>
        </Box>
    );
};

Filter.propTypes = {
    filters: PropTypes.object,
    setFilters: PropTypes.func,
    setSearch: PropTypes.func,
};

export default Filter;
