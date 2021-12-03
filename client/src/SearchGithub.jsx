import React, { useState } from "react";
import Box from '@mui/material/Box';
import { Button, Grid, TextField, Typography, Link, Card, TableHead, TableRow, TableCell, Table, TableBody, TableFooter, TablePagination } from "@mui/material";
import { textAlign } from "@mui/system";
import TablePaginationActions from "@mui/material/TablePagination/TablePaginationActions";

const SearchGithub = () => {
  
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
          <TableRow>
              <TableCell>
                <Card sx={{padding:1}}>
                  <Link target="_blank" to="">tensorflow/tensorflow</Link>
                  <Typography>Language: C++ Forked on GitHub: 82444 Updated at: 2020-08-21 16:03(UTC)</Typography>
                </Card>
              </TableCell>
              <TableCell>
                <Button variant="outlined">Follow</Button>
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell>
                <Card sx={{padding:1}}>
                  <Link target="_blank" to="">twbs/bootstrap</Link>
                  <Typography>Language: JavaScript Forked on GitHub: 71700 Updated at: 2021-01-17 22:26(UTC)</Typography>
                </Card>
              </TableCell>
              <TableCell>
                <Button variant="outlined">Follow</Button>
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell>
                <Card sx={{padding:1}}>
                  <Link target="_blank" to="">nightscout/cgm-remote-monitor</Link>
                  <Typography>Language: JavaScript Forked on GitHub: 42548 Updated at: 2020-07-25 21:12(UTC) </Typography>
                </Card>
              </TableCell>
              <TableCell>
                <Button variant="outlined">Follow</Button>
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell>
                <Card sx={{padding:1}}>
                  <Link target="_blank" to="">opencv/opencv</Link>
                  <Typography>Language: C++ Forked on GitHub: 41764 Updated at: 2020-12-23 06:49(UTC) </Typography>
                </Card>
              </TableCell>
              <TableCell>
                <Button variant="outlined">Follow</Button>
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell>
                <Card sx={{padding:1}}>
                  <Link target="_blank" to="">torvalds/linux</Link>
                  <Typography>Language: C Forked on GitHub: 33035 Updated at: 2020-08-19 09:24(UTC)</Typography>
                </Card>
              </TableCell>
              <TableCell>
                <Button variant="outlined">Follow</Button>
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell>
                <Card sx={{padding:1}}>
                  <Link target="_blank" to="">spring-projects/spring-boot</Link>
                  <Typography>Language: Java Forked on GitHub: 31207 Updated at: 2020-08-27 05:24(UTC)</Typography>
                </Card>
              </TableCell>
              <TableCell>
                <Button variant="outlined">Follow</Button>
              </TableCell>
            </TableRow>
        </TableBody>
        <TableFooter>
          <TableRow>
            <TablePagination 
              rowsPerPageOptions={[5, 10, 15]}
              count={6}
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
