// Inspired by MUI documentation: https://mui.com/components/tables/
import React, { useState, forwardRef, useEffect, useCallback } from "react";
import { useParams } from "react-router-dom";
import PropTypes from "prop-types";
import { alpha } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TablePagination from "@mui/material/TablePagination";
import TableRow from "@mui/material/TableRow";
import TableSortLabel from "@mui/material/TableSortLabel";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper";
import Checkbox from "@mui/material/Checkbox";
import IconButton from "@mui/material/IconButton";
import Tooltip from "@mui/material/Tooltip";
import DeleteIcon from "@mui/icons-material/Delete";
import FilterListIcon from "@mui/icons-material/FilterList";
import { visuallyHidden } from "@mui/utils";
import { Link } from "react-router-dom";
import AddShoppingCartIcon from "@mui/icons-material/AddShoppingCart";
import { useRecoilState } from "recoil";
import { Button, Snackbar } from "@mui/material";
import MuiAlert from "@mui/material/Alert";
import Stack from "@mui/material/Stack";
import { differenceWith, intersectionWith, isEqual } from "lodash";
import { getRepoForks } from "./repository";
import Loading from "./common/Loading"
import SearchAndFilter from "./common/SearchAndFilter";

const Alert = forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

function createData(
  fork_name,
  num_changed_files,
  num_changed_lines,
  total_commit_number,
  key_words,
  last_committed_time,
  created_time
) {

  // console.log("key words received:", key_words)
  let parsed_words = []
  for (let i = 0; i < key_words.length && i < 20; i++) {
    parsed_words.push(key_words[i].concat(", "));
  }
  // console.log("Parsed words:", parsed_words)

  return {
    fork_name,
    num_changed_files,
    num_changed_lines,
    total_commit_number,
    parsed_words,
    last_committed_time,
    created_time,
  };
}

function descendingComparator(a, b, orderBy) {
  if (b[orderBy] < a[orderBy]) {
    return -1;
  }
  if (b[orderBy] > a[orderBy]) {
    return 1;
  }
  return 0;
}

function getComparator(order, orderBy) {
  return order === "desc"
    ? (a, b) => descendingComparator(a, b, orderBy)
    : (a, b) => -descendingComparator(a, b, orderBy);
}

// This method is created for cross-browser compatibility, if you don't
// need to support IE11, you can use Array.prototype.sort() directly
function stableSort(array, comparator) {
  const stabilizedThis = array.map((el, index) => [el, index]);
  stabilizedThis.sort((a, b) => {
    const order = comparator(a[0], b[0]);
    if (order !== 0) {
      return order;
    }
    return a[1] - b[1];
  });
  return stabilizedThis.map((el) => el[0]);
}

const headCells = [
  {
    id: "fork_name",
    numeric: false,
    disablePadding: true,
    label: "Fork",
  },
  {
    id: "num_changed_files",
    numeric: false,
    disablePadding: false,
    label: "# Changed Files",
  },
  {
    id: "num_changed_lines",
    numeric: false,
    disablePadding: false,
    label: "# Changed Lines",
  },
  {
    id: "total_commit_number",
    numeric: false,
    disablePadding: false,
    label: "# Commits",
  },
  {
    id: "keywords",
    numeric: false,
    disablePadding: false,
    label: "Keywords",
  },
  {
    id: "last_committed_time",
    numeric: false,
    disablePadding: false,
    label: "Last Commit Time",
  }, {
    id: "created_time",
    numeric: false,
    disablePadding: false,
    label: "Creation Date",
  },
];

function EnhancedTableHead(props) {
  const {
    onSelectAllClick,
    order,
    orderBy,
    numSelected,
    rowCount,
    onRequestSort,
  } = props;
  const createSortHandler = (property) => (event) => {
    onRequestSort(event, property);
  };

  return (
    <TableHead>
      <TableRow>
        <TableCell padding="checkbox">
          <Checkbox
            color="primary"
            indeterminate={numSelected > 0 && numSelected < rowCount}
            checked={rowCount > 0 && numSelected === rowCount}
            onChange={onSelectAllClick}
            inputProps={{
              "aria-label": "select all desserts",
            }}
          />
        </TableCell>
        {headCells.map((headCell) => (
          <TableCell
            key={headCell.id}
            align={headCell.numeric ? "right" : "left"}
            padding={headCell.disablePadding ? "none" : "normal"}
            sortDirection={orderBy === headCell.id ? order : false}
          >
            <TableSortLabel
              active={orderBy === headCell.id}
              direction={orderBy === headCell.id ? order : "asc"}
              onClick={createSortHandler(headCell.id)}
            >
              {headCell.label}
              {orderBy === headCell.id ? (
                <Box component="span" sx={visuallyHidden}>
                  {order === "desc" ? "sorted descending" : "sorted ascending"}
                </Box>
              ) : null}
            </TableSortLabel>
          </TableCell>
        ))}
      </TableRow>
    </TableHead>
  );
}

EnhancedTableHead.propTypes = {
  numSelected: PropTypes.number.isRequired,
  onRequestSort: PropTypes.func.isRequired,
  onSelectAllClick: PropTypes.func.isRequired,
  order: PropTypes.oneOf(["asc", "desc"]).isRequired,
  orderBy: PropTypes.string.isRequired,
  rowCount: PropTypes.number.isRequired,
};

const EnhancedTableToolbar = (props) => {
  const { numSelected } = props;

  return (
    <Toolbar
      sx={{
        pl: { sm: 2 },
        pr: { xs: 1, sm: 1 },
        ...(numSelected > 0 && {
          bgcolor: (theme) =>
            alpha(
              theme.palette.primary.main,
              theme.palette.action.activatedOpacity
            ),
        }),
      }}
    >
      {numSelected > 0 ? (
        <Typography
          sx={{ flex: "1 1 100%" }}
          color="inherit"
          variant="subtitle1"
          component="div"
        >
          {numSelected} selected

        </Typography>
      ) : (
        <Typography
          sx={{ flex: "1 1 100%" }}
          variant="h6"
          id="tableTitle"
          component="div"
        >
          Search Results

        </Typography>

      )}

      {numSelected > 0 ? (
        <>
          <Tooltip title="Delete">
            <IconButton onClick={props.onDelete}>
              <DeleteIcon />
            </IconButton>
          </Tooltip>

        </>
      ) : (
        <Tooltip title="Filter list">
          <IconButton>
            <FilterListIcon />
          </IconButton>
        </Tooltip>
      )}
    </Toolbar>
  );
};

EnhancedTableToolbar.propTypes = {
  numSelected: PropTypes.number.isRequired,
  onDelete: PropTypes.func.isRequired,
};

const EnhancedTable = ({ data }) => {
  console.log("data", data);
  const rows = [];

  data.forEach((value) => {
    rows.push(
      createData(
        value.fork_name,
        value.num_changed_files ?? 0,
        value.num_changed_lines ?? 0,
        value.total_commit_number ?? 0,
        value.key_words,
        value.last_committed_time,
        value.created_time
      )
    );
  });
  const [order, setOrder] = useState("asc");
  const [orderBy, setOrderBy] = useState("num_changed_files");
  const [selected, setSelected] = useState([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);
  const [visibleRows, setVisibleRows] = useState(rows);
  const [commonKeywords, setCommonKeywords] = useState([]);
  const [displayCompare, setDisplayCompare] = useState(false);

  const handleRequestSort = (event, property) => {
    const isAsc = orderBy === property && order === "asc";
    setOrder(isAsc ? "desc" : "asc");
    setOrderBy(property);
  };

  const handleSelectAllClick = (event) => {
    if (event.target.checked) {
      const newSelecteds = visibleRows.map((row) => row);
      setSelected(newSelecteds);
      return;
    }
    setSelected([]);
  };

  const handleClick = (event, row) => {
    const selectedIndex = selected.indexOf(row);
    let newSelected = [];

    if (selectedIndex === -1) {
      newSelected = newSelected.concat(selected, row);
    } else if (selectedIndex === 0) {
      newSelected = newSelected.concat(selected.slice(1));
    } else if (selectedIndex === selected.length - 1) {
      newSelected = newSelected.concat(selected.slice(0, -1));
    } else if (selectedIndex > 0) {
      newSelected = newSelected.concat(
        selected.slice(0, selectedIndex),
        selected.slice(selectedIndex + 1)
      );
    }

    setSelected(newSelected);
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleDelete = () => {
    const filteredRows = visibleRows.filter(
      (element) => !selected.includes(element)
    );
    setVisibleRows(filteredRows);
    setSelected([]);
  };

  const handleCompareButton = () => {
    console.log("Selected forks:", selected)

    let comparisonKeywords = [];
    for (let i = 0; i < selected.length; i++) {
      let words = selected[i]["parsed_words"];
      comparisonKeywords.push(words);
    }

    let commonKeywordsTemp = [];
    for (let i = 1; i < comparisonKeywords.length; i++) {
      commonKeywordsTemp = comparisonKeywords[0].filter(x => comparisonKeywords[i].includes(x));
    }
    console.log("Common keywords:", commonKeywords);
    setCommonKeywords(commonKeywordsTemp);
    setDisplayCompare(true);
  };

  const isSelected = (fork) => selected.indexOf(fork) !== -1;

  // Avoid a layout jump when reaching the last page with empty rows.
  const emptyRows =
    page > 0 ? Math.max(0, (1 + page) * rowsPerPage - visibleRows.length) : 0;

  return (
    <Box sx={{ width: "100%" }}>
      <Paper sx={{ width: "100%", mb: 2 }}>

        <EnhancedTableToolbar
          numSelected={selected.length}
          onDelete={handleDelete}
        />
        {selected.length > 0 && <Button onClick={handleCompareButton}>Compare Selected Forks</Button>}

        <TableContainer>
          <Table
            sx={{ minWidth: 750 }}
            aria-labelledby="tableTitle"
            size="medium"
          >
            <EnhancedTableHead
              numSelected={selected.length}
              order={order}
              orderBy={orderBy}
              onSelectAllClick={handleSelectAllClick}
              onRequestSort={handleRequestSort}
              rowCount={visibleRows.length}
            />
            <TableBody>
              {/* if you don't need to support IE11, you can replace the `stableSort` call with:
                 rows.slice().sort(getComparator(order, orderBy)) */}
              {stableSort(visibleRows, getComparator(order, orderBy))
                .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                .map((row, index) => {
                  const isItemSelected = isSelected(row);
                  const labelId = `enhanced-table-checkbox-${index}`;

                  return (
                    <TableRow
                      hover
                      onClick={(event) => handleClick(event, row)}
                      role="checkbox"
                      aria-checked={isItemSelected}
                      tabIndex={-1}
                      key={row.fork_name}
                      selected={isItemSelected}
                    >
                      <TableCell padding="checkbox">
                        <Checkbox
                          color="primary"
                          checked={isItemSelected}
                          inputProps={{
                            "aria-labelledby": labelId,
                          }}
                        />
                      </TableCell>
                      <TableCell
                        component="th"
                        id={labelId}
                        scope="row"
                        padding="none"
                      >
                        {row.fork_name}
                      </TableCell>
                      <TableCell align="left">
                        {row.num_changed_files}
                      </TableCell>
                      <TableCell align="left">
                        {row.num_changed_lines}
                      </TableCell>
                      <TableCell align="left">
                        {row.total_commit_number}
                      </TableCell>
                      <TableCell align="left">
                        {row.parsed_words}
                      </TableCell>
                      <TableCell align="left">
                        {row.last_committed_time}
                      </TableCell>
                      <TableCell align="left">
                        {row.created_time}
                      </TableCell>
                    </TableRow>
                  );
                })}
              {emptyRows > 0 && (
                <TableRow
                  style={{
                    height: 53 * emptyRows,
                  }}
                >
                  <TableCell colSpan={6} />
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          rowsPerPageOptions={[5, 10, 25]}
          component="div"
          count={visibleRows.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </Paper>
      {displayCompare && commonKeywords.length > 0 && <Paper sx={{ width: "20%", padding: 1 }}>
        <Typography variant="h6">Common Words from Selected Forks</Typography>
        <Typography paragraph>{commonKeywords}</Typography>
      </Paper>}
    </Box>
  );
};

const ForkList = () => {
  const { repo1, repo2 } = useParams();
  const [data, setData] = useState(null);

  const fetchForks = useCallback(async (repo) => {
    const response = await getRepoForks(repo);
    console.log("Fetching forks list for ", repo)
    console.log("forks list response", response);
    setData(response.data.forks);
  }, []);

  useEffect(() => {
    const repo = repo1 + "/" + repo2;
    fetchForks(repo);
  }, [fetchForks]);

  return (
    <>{data ? <EnhancedTable data={data} /> : <Loading></Loading>}</>
  );
};

export default ForkList;
