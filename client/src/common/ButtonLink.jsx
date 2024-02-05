import React from "react";
import Button from "@mui/material/Button";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";

const ButtonLink = ({ to, linkText, color, startIcon }) => {
  return (
    <Link to={to} style={{ textDecoration: "none", color }}>
      <Button color={color} startIcon={startIcon}>
        {linkText}
      </Button>
    </Link>
  );
};

ButtonLink.propTypes = {
  to: PropTypes.string,
  linkText: PropTypes.string,
  color: PropTypes.string,
  startIcon: PropTypes.element || null,
};

export default ButtonLink;
