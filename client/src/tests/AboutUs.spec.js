import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import AboutUs from "../AboutUs";

describe("<AboutUs />", () => {
  it("should display title and content", () => {
    render(<AboutUs />);
    expect(screen.getByText("About")).toBeInTheDocument();
  });
});
