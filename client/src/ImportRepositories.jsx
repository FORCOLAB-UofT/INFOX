import React, { useEffect, useCallback, useState } from "react";
import { Box, Grid, Checkbox, ListItem } from "@mui/material";
import { getUserImportedRepositories } from "./repository";
import { LOADING_HEIGHT } from "./common/constants";
import Loading from "./common/Loading";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import Typography from "@mui/material/Typography";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";

const ImportRepositories = () => {
  const [importedRepositories, setImportedRepositories] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchImportedRepositories = useCallback(async () => {
    const response = await getUserImportedRepositories();

    setImportedRepositories(response.data.importRepositories);
    console.log("res", response);

    setIsLoading(false);
  }, []);

  useEffect(() => {
    fetchImportedRepositories();
  }, [fetchImportedRepositories]);

  return (
    <Box>
      {isLoading ? (
        <Box height={LOADING_HEIGHT}>
          <Loading />
        </Box>
      ) : (
        <Box>
          {importedRepositories.map((item) => (
            <Accordion key={item.repo}>
              <AccordionSummary
                expandIcon={<ExpandMoreIcon />}
                aria-controls="panel1a-content"
                id="panel1a-header"
              >
                <Grid item xs={1}>
                  <Checkbox
                    value="checkedB"
                    color="primary"
                    onClick={(e) => e.stopPropagation()}
                  />
                </Grid>
                <Grid item xs={2}>
                  <Typography className="repoName">{item.repo}</Typography>
                </Grid>
              </AccordionSummary>
              <AccordionDetails>
                <Typography>
                  Description: {item.description} <br />
                  Language: {item.language} <br />
                  Times this repository was forked: {item.timesForked} <br />
                  Updated: {item.updated}
                </Typography>
              </AccordionDetails>
            </Accordion>
          ))}
        </Box>
      )}
      <Box style={{textAlign:"right"}}>
        <Button variant="contained">Follow</Button>
      </Box>
    </Box>
  );
};

export default ImportRepositories;
