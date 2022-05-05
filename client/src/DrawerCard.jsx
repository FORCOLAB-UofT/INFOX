import React, { useState } from "react";
import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper";
import ButtonBase from "@mui/material/ButtonBase";
import { PRIMARY, TERTIARY } from "./common/constants";
import { useNavigate } from "react-router-dom";

const DrawerCard = ({ title, description, link, onCloseDrawer }) => {
  const [color, setColor] = useState("white");
  const navigate = useNavigate();
  return (
    <Box padding={1}>
      <ButtonBase
        onClick={() => {
          onCloseDrawer();
          navigate(link);
        }}
      >
        <Card
          variant="outlined"
          style={{ backgroundColor: color }}
          onMouseOver={() => {
            setColor(TERTIARY);
          }}
          onMouseLeave={() => {
            setColor("white");
          }}
        >
          <CardContent>
            <Box textAlign="left" width={400}>
              <Typography variant="h6" color={PRIMARY}>
                <b>{title}</b>
              </Typography>
              <Typography sx={{ mb: 1.5 }} color="text.secondary">
                {description}
              </Typography>
            </Box>
          </CardContent>
        </Card>
      </ButtonBase>
    </Box>
  );
};

export default DrawerCard;
