import React, { useState } from "react";
import Box from "@mui/material/Box";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import Typography from "@mui/material/Typography";
import CloseIcon from "@mui/icons-material/Close";
import IconButton from "@mui/material/IconButton";
import Button from "@mui/material/Button";
import GitHubIcon from "@mui/icons-material/GitHub";
import { useNavigate } from "react-router-dom";
import Grid from "@mui/material/Grid";
import { DARK } from "./common/constants";

const LoginModal = () => {
  const navigate = useNavigate();

  const onClose = () => {
    navigate("/");
  };

  return (
    <Box>
      <Dialog
        open={true}
        variant="outlined"
        onClose={onClose}
        maxWidth="xs"
        BackdropProps={{
          style: { backgroundColor: "#212121", opacity: 0.9 },
        }}
      >
        <DialogTitle>
          <Typography variant="h5" color={DARK}>
            Please Log In
          </Typography>
          <IconButton
            aria-label="close"
            onClick={onClose}
            sx={{
              position: "absolute",
              right: 8,
              top: 8,
              color: (theme) => theme.palette.grey[500],
            }}
          >
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent>
          <Box paddingBottom={2}>
            <Typography>
              Please login /or sign up using your Github account to access the
              full list of features!
            </Typography>
          </Box>
          <Grid
            container
            direction="column"
            alignItems="center"
            justifyContent="center"
          >
            <Button
              style={{ background: "#424242", color: "white" }}
              variant="contained"
              onClick={() => {
                window.location.href =
                  "https://github.com/login/oauth/authorize?scope=user:email&client_id=2d8e058ac0d5cf153c9e";
              }}
            >
              <Box paddingRight={1}>
                <GitHubIcon />
              </Box>
              Log in with Github
            </Button>
          </Grid>
        </DialogContent>
      </Dialog>
    </Box>
  );
};

export default LoginModal;
