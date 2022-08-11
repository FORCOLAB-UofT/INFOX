
import React, { useState, forwardRef, useEffect, useCallback } from "react";
import { useParams } from "react-router-dom";
import * as d3 from 'd3';
import { getRepoForks } from "./repository";
import Loading from "./common/Loading"
import ForkRank from "./ForkRank";

const ForkGraph = () => {

  const { repo1, repo2 } = useParams();
  const [data, setData] = useState(null);
  const [fork_names, setForkNames] = useState(null);

  const getDataList = (forks_list) => {
    //EXTRACT TOP TEN
    let datalist = []
    for (let i = 0; i < forks_list.length && i < 10; i++) {
      let fork = forks_list[i]
      console.log(fork)
      let commit_list = fork["commit_freq"]
      for (let j = 0; j < commit_list.length; j++) {
        let ith_week_dic = {}
        ith_week_dic["week"] = j
        ith_week_dic["commits"] = commit_list[j]
        ith_week_dic["territory"] = fork["fork_name"]
        datalist.push(ith_week_dic)
      }
    }
    return datalist
}

const getForkNames = (forks_list) => {
  let fork_names = []
  for (let i = 0; i < forks_list.length && i < 10; i++) {
    fork_names.push(forks_list[i]["fork_name"])
  }
  return fork_names
}

const fetchForks = useCallback(async (repo) => {
  console.log('repo1',repo1);
  console.log('repo2', repo2);
  const response = await getRepoForks(repo);
  console.log("Fetching forks list for ", repo)
  setData(getDataList(response.data.forks))
  setForkNames(getForkNames(response.data.forks))
}, []);

  useEffect(() => {
    const repo = repo1 + "/" + repo2;
    fetchForks(repo);
  }, [fetchForks]);
    
  return (
    data && fork_names ? <ForkRank data={data} fork_names={fork_names}></ForkRank> : <Loading></Loading>
  );
}

export default ForkGraph;