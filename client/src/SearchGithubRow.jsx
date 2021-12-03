import React from "react";
import Box from '@mui/material/Box';
import { Button, TextField, Typography, Link, Card, TableHead, TableRow, TableCell, Table, TableBody, TableFooter, TablePagination } from "@mui/material";

const SearchGithubRow = ({name, link, description}) => {


    return (
        <TableRow>
            <TableCell>
            <Card sx={{padding:1}}>
                <Link target="_blank" to={link}>{name}</Link>
                <Typography>{description}</Typography>
            </Card>
            </TableCell>
            <TableCell>
            <Button variant="outlined">Follow</Button>
            </TableCell>
        </TableRow>
    );

};

export default SearchGithubRow;
