import React, { useState } from "react";
import {
  Button,
  Typography,
  Link,
  Card,
  TableRow,
  TableCell,
  Grid,
} from "@mui/material";
import { postFollowRepository } from "./repository";

const SearchGithubRow = ({ name, language, forks, updated, onFollow }) => {
  const [isLoading, setIsLoading] = useState(false);

  return (
    <TableRow>
      <TableCell>
        <Card sx={{ padding: 1 }}>
          <Link target="_blank" to="">
            {name}
          </Link>
          <Grid container spacing={1}>
            <Grid item xs={4}>
              Language: {language}
            </Grid>
            <Grid item xs={4}>
              Forked on Github: {forks}
            </Grid>
            <Grid item xs={4}>
              Updated at: {updated}
            </Grid>
          </Grid>
          <Typography></Typography>
        </Card>
      </TableCell>
      <TableCell>
        <Button
          variant="outlined"
          onClick={async () => {
            setIsLoading(true);
            const res = await postFollowRepository(name);
            console.log("res", res);
            onFollow(res.data);
            setIsLoading(false);
          }}
        >
          {isLoading ? "Following..." : "Follow"}
        </Button>
      </TableCell>
    </TableRow>
  );
};

export default SearchGithubRow;
