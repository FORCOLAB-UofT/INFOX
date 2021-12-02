import React, { useEffect, useCallback, useState } from "react";
import { Box } from "@mui/material";
import { getUserFollowedRepositories } from "./repository";
import { LOADING_HEIGHT } from "./common/constants";
import Loading from "./common/Loading";
import Title from "./common/Title";

const FollowedRespositories = () => {
  const [followedRepositories, setFollowedRepositories] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchFollowedRepositories = useCallback(async () => {
    const response = await getUserFollowedRepositories();

    setFollowedRepositories(response.data.followedRepositories);
    console.log("res", response);

    setIsLoading(false);
  }, []);

  useEffect(() => {
    fetchFollowedRepositories();
  }, [fetchFollowedRepositories]);

  return (
    <Box>
      {isLoading ? (
        <Box height={LOADING_HEIGHT}>
          <Loading />
        </Box>
      ) : (
        <Box width="100%">
          <Title text="Followed Repositories" />
        </Box>
      )}
    </Box>
  );
};

export default FollowedRespositories;
