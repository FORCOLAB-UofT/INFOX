import axios from "axios";

// TODO: convert the links to be based on prod environment or development, or implement a proxy
export const getUserFollowedRepositories = async () => {
  const response = await axios.get("http://localhost:5000/flask/followed");
  return response;
};

export const getUserImportRepositories = async () => {
  const response = await axios.get("http://localhost:5000/flask/import");
  return response;
};
