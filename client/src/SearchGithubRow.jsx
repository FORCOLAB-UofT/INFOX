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
import { postFollowRepository, deleteUserRepository } from "./repository";

const SearchGithubRow = ({
  name,
  language,
  forks,
  updated,
  onFollow,
  onRemoveRepo,
  followedRepos,
}) => {
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
        {!followedRepos?.some((repo) => repo.repo === name) ? (
          <Button
            variant="outlined"
            onClick={async () => {
              setIsLoading(true);
              const res = await postFollowRepository(name);
              console.log("res", res);
              onFollow(res.data);
              setIsLoading(false);
            }}
            disabled={isLoading}
          >
            {isLoading ? "Following..." : "Follow"}
          </Button>
        ) : (
          <Button
            variant="contained"
            color="error"
            onClick={() => {
              deleteUserRepository(name);
              onRemoveRepo(name);
            }}
          >
            Remove
          </Button>
        )}
      </TableCell>
    </TableRow>
  );
};

export default SearchGithubRow;
