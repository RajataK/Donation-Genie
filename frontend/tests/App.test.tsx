import { render, screen, waitFor } from "@testing-library/react";
import App from "../src/App";

describe("App", () => {
  it("renders without crashing", async () => {
    render(<App />);
    await waitFor(() => {
      expect(screen.getByText(/donation genie/i)).toBeInTheDocument();
    });
  });
});
