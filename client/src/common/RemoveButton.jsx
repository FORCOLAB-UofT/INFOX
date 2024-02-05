import React from "react";
import Button from "@mui/material/Button";
import { PRIMARY, REMOVE } from "./constants";

const RemoveButton = ({ onClickRemove }) => {
  return (
    <Button
      style={{ color: PRIMARY, background: REMOVE }}
      onClick={(e) => {
        onClickRemove(e);
      }}
    >
      Remove
    </Button>
  );
};

export default RemoveButton;
