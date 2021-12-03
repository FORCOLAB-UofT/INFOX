import React, { useState } from "react";
import Box from '@mui/material/Box';
import { Button, TextField, Typography, Link, Card, TableHead, TableRow, TableCell, Table, TableBody, TableFooter, TablePagination } from "@mui/material";
import SearchGithubRow from "./SearchGithubRow";


const SearchGithub = () => {
  

  const rows = [["tensorflow/tensorflow","", "Language: C++ Forked on GitHub: 82444 Updated at: 2020-08-21 16:03(UTC)"], 
  ["twbs/bootstrap", "", "Language: JavaScript Forked on GitHub: 71700 Updated at: 2021-01-17 22:26(UTC)"], 
  ["nightscout/cgm-remote-monitor", "", "Language: JavaScript Forked on GitHub: 42548 Updated at: 2020-07-25 21:12(UTC)"], 
  ["opencv/opencv", "", "Language: C++ Forked on GitHub: 41764 Updated at: 2020-12-23 06:49(UTC)"], 
  ["torvalds/linux", "", "Language: C Forked on GitHub: 33035 Updated at: 2020-08-19 09:24(UTC)"], 
  ["spring-projects", "", "Language: Java Forked on GitHub: 31207 Updated at: 2020-08-27 05:24(UTC)"]];

  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);
  
  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };
  
  return (
  <Box sx={{display:'flex', flexDirection:"column"}}>
    <Box sx={{display:'flex', flexDirection:"column", borderBottom:1, padding:3}}>
      <Typography variant="h5" sx={{marginTop:1}}>Search on GitHub</Typography>
      <Typography variant="body1" sx={{marginTop:1}}>Input the full name of the repository (author/repo)</Typography>
      <TextField label="Repository"></TextField>
      <Button variant="contained" sx={{width:200, marginTop:2}}>Search & Follow</Button>
    </Box>
    <Box sx={{display:'flex', flexDirection:"column", padding:3}}>
      <Typography variant="h5">Frequently Analyzed Repos on INFOX</Typography>
      <Table>
        <TableHead>
        </TableHead>
        <TableBody>
          {rows.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
            .map((row) => {
              return (
                <SearchGithubRow name={row[0]} link={row[1]} description={row[2]}></SearchGithubRow>
              );
            })
          }
        </TableBody>
        <TableFooter>
          <TableRow>
            <TablePagination 
              rowsPerPageOptions={[5, 10, 15]}
              count={rows.length}
              rowsPerPage={rowsPerPage}
              page={page}
              onPageChange={handleChangePage}
              onRowsPerPageChange={handleChangeRowsPerPage}
            />
          </TableRow>
        </TableFooter>
      </Table>
    </Box>
  </Box>
  );
};

export default SearchGithub;
