import axios from "axios";

// TODO: convert the links to be based on prod environment or development, or implement a proxy
export const getUserFollowedRepositories = async () => {
  const response = await axios({
    method: "GET",
    url: "flask/followed",
    headers: {
      Authorization: "Bearer " + localStorage.getItem("access_token"),
    },
  });

  return response;
};

export const getTotalForksNumber = async (value) => {
  const response = await axios({
    method: "GET",
    url: `http://localhost:3000/flask/forklist?repo=${value}`,
    headers: {
      Authorization: "Bearer " + localStorage.getItem("access_token"),
    },
  });
  return response;
};

export const getRepoForks = async (value, i) => {
  const response = await axios({
    method: "POST",
    url: `http://localhost:3000/flask/forklist`,
    headers: {
      Authorization: "Bearer " + localStorage.getItem("access_token"),
    },
    data: { repo: value, index: i },
  });
  return response;
};

export const getActiveForksNum = async (value) => {
  const response = await axios({
    method: "GET",
    url: `http://localhost:3000/flask/progress?repo=${value}`,
    headers: {
      Authorization: "Bearer " + localStorage.getItem("access_token"),
    },
  });
  return response;
};

export const postProgress = async (value, i) => {
  const response = await axios({
    method: "POST",
    url: `http://localhost:3000/flask/progress`,
    headers: {
      Authorization: "Bearer " + localStorage.getItem("access_token"),
    },
    data: { repo: value, index: i },
  });
  return response;
};

export const getUserImportRepositories = async () => {
  const response = await axios({
    method: "GET",
    url: "flask/import",
    headers: {
      Authorization: "Bearer " + localStorage.getItem("access_token"),
    },
  });
  return response;
};

export const postUserLogin = async (values) => {
  const response = await axios.post("flask/auth", {
    code: values,
  });

  return response;
};

export const getUserLogin = async () => {
  const response = await axios({
    method: "GET",
    url: "flask/auth",
    headers: {
      Authorization: "Bearer " + localStorage.getItem("access_token"),
    },
  });

  return response;
};

// get 5 among the top forked repos on github
export const fetchFreqForkRepos = async (apiEndpoint) => {
  return await fetch(apiEndpoint).then((res) => res.json()).then((data) => data["items"]);
  // return await axios.get(apiEndpoint).then((res) => res.json()).then((data) => data["items"]); // axios fields not filled, could fix later to use axios rather than fetch
};

export const postSearchGithub = async (value) => {
  const response = await axios({
    method: "POST",
    url: "flask/search",
    headers: {
      Authorization: "Bearer " + localStorage.getItem("access_token"),
    },
    data: { repo: value },
  });

  return response;
};

export const postFollowRepository = async (value) => {
  const response = await axios({
    method: "POST",
    url: "flask/follow",
    headers: {
      Authorization: "Bearer " + localStorage.getItem("access_token"),
    },
    data: { repo: value },
  });

  return response;
};

export const deleteUserRepository = async (value) => {
  const response = await axios({
    method: "DELETE",
    url: "flask/followed",
    headers: {
      Authorization: "Bearer " + localStorage.getItem("access_token"),
    },
    data: { repo: value },
  });

  return response;
};

export const getForkClustering = async ({
  repo,
  analyzeCode,
  analyzeFiles,
  analyzeCommits,
  clusterNumber,
  updatedData,
  userInputWords,
}) => {
  const response = await axios({
    method: "GET",
    url: `flask/cluster?repo=${repo}&analyzeCode=${analyzeCode}&analyzeFiles=${analyzeFiles}&analyzeCommits=${analyzeCommits}&clusterNumber=${clusterNumber}&updateData=${updatedData}&userInputWords=${userInputWords}`,
    headers: {
      Authorization: "Bearer " + localStorage.getItem("access_token"),
    },
  });
  return response;
};
