import "@testing-library/jest-dom";
import { render, screen, fireEvent } from "@testing-library/react";
import { createServer } from "miragejs";
import ImportRepositories from "../ImportRepositories";

describe("<ImportRepositories />", () => {
  beforeAll(() => {
    let server = createServer({
      routes() {
        this.get("http://localhost:5000/flask/followed", () => {
          return [
            {
              language: "Python",
              description:
                "Zulip server and web app for powerful open source team chat",
              timesForked: 5027,
              repo: "zulip/zulip",
              updated: "01/09/2022",
            },
          ];
        });

        this.get("http://localhost:5000/flask/import", () => {
          return {
            importRepositories: [
              {
                repo: "user/PersonalWebsite",
                description: "my website description",
                language: "HTML",
                timesForked: 10,
              },
              {
                repo: "user/PersonalProject",
                description: null,
                language: "Python",
                timesForked: 0,
              },
              {
                repo: "user/SpotifyFetcher",
                description: "Gets popular spotify artists and tracks",
                language: "Python",
                timesForked: 32124,
              },
              {
                repo: "user/data-science-course",
                description: null,
                language: "Python",
                timesForked: 0,
              },
              {
                repo: "user/programming-lab",
                description: "Javascript programming lab",
                language: "Javascript",
                timesForked: 0,
              },
            ],
          };
        });

        this.post("http://localhost:5000/flask/follow", (schema, request) => {
          let attrs = JSON.parse(request.requestBody);
          return {
            msg: "The repo is already in INFOX. Followed successfully!",
            repo: {
              repo: "user/PersonalWebsite",
              description: "my website description",
              language: "HTML",
              timesForked: 10,
            },
          };
        });

        this.delete("http://localhost:5000/flask/followed", () => {
          return true;
        });
      },
    });
  });

  it("should display user repositories", async () => {
    render(<ImportRepositories />);
    await screen.findByText("user/PersonalWebsite");

    // Test existence of repo names
    expect(screen.queryByText("user/PersonalWebsite")).toBeInTheDocument();
    expect(screen.queryByText("user/PersonalProject")).toBeInTheDocument();
    expect(screen.queryByText("user/SpotifyFetcher")).toBeInTheDocument();
    expect(screen.queryByText("user/data-science-course")).toBeInTheDocument();
    expect(screen.queryByText("user/programming-lab")).toBeInTheDocument();

    // Test project descriptions
    expect(
      screen.queryByText("Project Description: my website description")
    ).toBeInTheDocument();
    expect(
      screen.queryByText(
        "Project Description: Gets popular spotify artists and tracks"
      )
    ).toBeInTheDocument();
    expect(
      screen.queryByText("Project Description: Javascript programming lab")
    ).toBeInTheDocument();

    // Test project forked amounts
    expect(screen.queryByText("Times Forked: 10")).toBeInTheDocument();
    expect(screen.queryByText("Times Forked: 32124")).toBeInTheDocument();
    expect(screen.queryAllByText("Times Forked: 0")).toHaveLength(3);

    // Test project languages
    expect(screen.queryByText("Language: HTML")).toBeInTheDocument();
    expect(screen.queryByText("Language: Javascript")).toBeInTheDocument();
    expect(screen.queryAllByText("Language: Python")).toHaveLength(3);
  });

  it("should follow and remove repository", async () => {
    render(<ImportRepositories />);
    await screen.findByText("user/PersonalWebsite");
    fireEvent.click(screen.getAllByText("Follow")[0]);
    expect(screen.queryByText("Following...")).toBeInTheDocument();
    await screen.findByText("Remove");
    fireEvent.click(screen.getByText("Remove"));
    expect(screen.queryByText("Remove")).not.toBeInTheDocument();
  });
});
