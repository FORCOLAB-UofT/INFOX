import { Button, Card, Link, Paper, Typography } from "@mui/material";
import { Box, height } from "@mui/system";
import React from "react";
import Image from "./static/img/network.jpg"
import Image1 from "./static/img/overview.png"
import Image2 from "./static/img/tagging.png"

const styles = {
  paperContainer: {
    height: 650,
    width: '100%',
    backgroundImage: `url(${Image})`,
    backgroundSize: 'cover',
    backgroundPositionX: 'center',

  },
  boxContainer: {
    width: "20%",
    backgroundImage: `url(${Image1})`,
    backgroundSize: 'contain',
    backgroundPositionX: 'center',
    backgroundRepeat: 'no-repeat'
  },
  boxContainer1: {
    width: "30%",
    backgroundImage: `url(${Image2})`,
    backgroundSize: 'contain',
    backgroundPositionX: 'center',
    backgroundRepeat: 'no-repeat'
  },

  flexCenteredColumns: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
  },

  flexSpaceEvenRows: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'space-evenly',
  }
};

const Home = () => {
  return (
    <Box sx={{ display: "flex", justifyContent: "center", flexDirection: "column", alignItems: "center" }}>
      <Box variant="elevated" style={styles.paperContainer}>
        <Box variant="elevated" style={styles.flexCenteredColumns} sx={{ background: "rgba(0, 0, 0, 0.6)", height: 650 }}>
          <Typography variant="h1" color="white" textAlign="center">INFOX <sub>beta</sub></Typography>
          <Typography variant="h2" color="white" textAlign="center">Insights into Forks</Typography>
          <br></br>
          <br></br>
          <br></br>
          <Typography variant="body1" color="white" textAlign="center">Overwhelmed with the activities in forks of a project?
          </Typography>

          <Typography variant="body1" color="white" textAlign="center">Which forks are active?
          </Typography>

          <Typography variant="body1" color="white" textAlign="center">Which contain interesting ideas?
          </Typography>

          <Typography variant="body1" color="white" textAlign="center">Which contain already finished features to build upon, rather than reimplement?
          </Typography>

        </Box>
      </Box>
      <Card style={styles.flexSpaceEvenRows} sx={{ padding: 2, marginTop: 2 }}>
        <Box style={styles.boxContainer}></Box>
        <Typography variant="h4" width="30%">Concise Overview of a Project's Forks<Typography variant="body1" paragraph>
          Explore a compact list of all forks highlighting key insights, rather than scrolling forever in
          a network graph. We sift all forks and summarize changes with statistics and representative
          keywords. Sort forks by activity volume and recency or search for keywords.

        </Typography></Typography>
      </Card>

      <Card style={styles.flexSpaceEvenRows} sx={{ padding: 2, marginTop: 2 }}>
        <Typography variant="h4" width="20%">Label and Monitor Forks<Typography variant="body1" paragraph>Identify and
          label forks with interesting activities, for example to scout for ideas and pull requests.
          Monitor interesting forks to keep up with changes.
          Track the activity of an entire community on GitHub. Get started by signing in with your
          GitHub account.

        </Typography></Typography>
        <Box style={styles.boxContainer1}></Box>
      </Card>
      <Card style={styles.flexSpaceEvenRows} sx={{ padding: 2, marginTop: 2 }}>
        <Typography variant="h4" sx={{ width: "67%", }}>Research and Contribution <Typography variant="body1" paragraph>INFOX comes out
          of an NSF-funded research project at Carnegie Mellon University, exploring how to improve
          collaboration and coordination in open-source software development. INFOX is open source
          and hosted for the community. We would love to hear your ideas and feedback. Explore the
          <Link target="_blank" href="https://github.com/FancyCoder0/INFOX"> source</Link> or <Link target="_blank" href="https://github.com/FancyCoder0/INFOX/issues">open an issue.</Link> </Typography>

        </Typography>
      </Card>

      <Card variant="elevated" sx={{ display: "flex", marginTop: 1, width: "100%", justifyContent: "space-evenly" }}>
        <Button variant="text" target="_blank" href="http://forks-insight.com/about">Contact Us</Button>
        <Button variant="text" target="_blank" href="https://github.com/FancyCoder0/INFOX">INFOX on GitHub</Button>
        <Button variant="text" target="_blank" href="https://github.com/FancyCoder0/INFOX/issues">Open An Issue</Button>
      </Card>
    </Box>
  );
};

export default Home;
