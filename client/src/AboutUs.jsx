import React from "react";
import { Box, Typography, Card } from "@mui/material";
import Link from '@mui/material/Link';
import Button from '@mui/material/Button';

const AboutUs = () => {

    return (
        <Box sx={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
            <Card sx={{ padding: 2, marginBottom: 1, marginTop: 1, width: 95 + "%" }}>
                <Typography variant="h4">About</Typography>
                <Typography paragraph variant="body1">INFOX comes out of a research project at
                    Carnegie Mellon University, in collaboration with researchers from the IT University
                    Copenhagen, Peking University, and the University of Passau, exploring how to improve
                    ollaboration and coordination in open-source and variant-rich software development.
                </Typography>
                <Typography paragraph variant="body1">
                    Given the overwhelming numbers of forks in many popular repositories,
                    we observed redundant development and lost contributions at scale and heard
                    from interviewed developers that they were interested in activities in forks
                    but overwhelmed by the sheer scale of the task and the lack of adequate tools.
                    INFOX set out to understand activities in forks and provide insights to
                    interested observers of a project and all its forks. The current beta release
                    focuses on simple analytics, but we plan many more functions as we move along.
                </Typography>
                <Typography paragraph variant="body1">
                    INFOX is open source (MIT license) and <Link href="https://github.com/FancyCoder0/INFOX">hosted on GitHub.</Link> Forks and pull requests are
                    welcome of course. :)
                </Typography>
            </Card>
            <Card sx={{ padding: 2, marginBottom: 1, width: 95 + "%" }}>
                <Typography variant="h4">People</Typography>
                <Typography variant="body1"><Link href="http://luyaoren.com/">Luyao Ren</Link></Typography>
                <Typography variant="body1"><Link href="https://www.cs.cmu.edu/~shuruiz/">Shurui Zhou</Link></Typography>
                <Typography variant="body1"><Link href="https://www.cs.cmu.edu/~ckaestne/">Christian Kästner</Link></Typography>
                <Typography variant="body1"><Link href="http://www.itu.dk/people/wasowski/">Andrzej Wąsowski</Link></Typography>
            </Card>
            <Card sx={{ padding: 2, width: 95 + "%" }}>
                <Typography variant="h4">Publication</Typography>
                <Typography variant="body1"><Link href="http://luyaoren.com/">L. Ren</Link>,
                    <Link href="https://www.cs.cmu.edu/~shuruiz/"> S. Zhou</Link>,
                    <Link href="https://www.cs.cmu.edu/~ckaestne/"> C. Kästner</Link>,
                    and <Link href="http://www.itu.dk/people/wasowski/">A. Wąsowski</Link>.
                    <b>Identifying Redundancies in Fork-based Development. </b>In Proceedings of the 27th IEEE
                    International Conference on Software Analysis, Evolution and Reengineering (SANER)
                    [ <Link href="https://www.cs.cmu.edu/~ckaestne/pdf/saner19.pdf">paper </Link>]
                </Typography>
                <Typography variant="body1"><Link href="http://luyaoren.com/">L. Ren</Link>
                    , <Link href="https://www.cs.cmu.edu/~shuruiz/"> S. Zhou</Link>
                    , and <Link href="https://www.cs.cmu.edu/~ckaestne/"> C. Kästner</Link>
                    . <b>Poster: Forks Insight:
                        Providing an Overview of GitHub Forks. </b>In Proceedings of the 40th International
                    Conference on Software Engineering (ICSE) [ poster ] [ paper ]</Typography>
                <Typography variant="body1"><Link href="https://www.cs.cmu.edu/~shuruiz/"> S. Zhou</Link>
                    , <Link href="http://www.itu.dk/people/scas/webpage/index.html">Ș. Stănciulescu</Link>
                    , <Link href="https://www.infosun.fim.uni-passau.de/spl/people-lessenich.php">O. Leßenich</Link>
                    , <Link href="http://sei.pku.edu.cn/~xiongyf04/">Y. Xiong</Link>,
                    <Link href="http://www.itu.dk/people/wasowski/">A. Wąsowski</Link>
                    , and <Link href="https://www.cs.cmu.edu/~ckaestne/"> C. Kästner</Link>
                    . <b>Identifying Features in Forks.</b>
                    In Proceedings of the 40th International Conference on Software Engineering (ICSE),
                    New York, NY: ACM Press, May 2018. Acceptance rate: 21 % (105/502). [ pdf ]
                </Typography>
            </Card>
            <Card sx={{display:"flex", marginTop:1, width:50+"%", justifyContent:"space-evenly"}}>
                <Button variant="text" target="_blank" href="http://forks-insight.com/about">Contact Us</Button>
                <Button variant="text" target="_blank" href="https://github.com/FancyCoder0/INFOX">INFOX on GitHub</Button>
                <Button variant="text" target="_blank" href="https://github.com/FancyCoder0/INFOX/issues">Open An Issue</Button>
            </Card>
        </Box>
    );
};

export default AboutUs;