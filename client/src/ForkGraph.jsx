
import React, { useState, forwardRef, useEffect, useCallback } from "react";
import { useParams } from "react-router-dom";
import * as d3 from 'd3';
import { getRepoForks } from "./repository";
import Loading from "./common/Loading"
import ForkRank from "./ForkRank";

// const territories = ["External", "Far West", "Great Lakes"]

// const data = [
//   {territory: "External", quarter: "Q1 2013", profit: 41119.6},
//   {territory: "External", quarter: "Q2 2013", profit: 36771.95},
//   {territory: "External", quarter: "Q3 2013", profit: 45251.75},
//   {territory: "External", quarter: "Q4 2013", profit: 17989.05},
//   {territory: "External", quarter: "Q1 2014", profit: 25182.9},
//   {territory: "External", quarter: "Q2 2014", profit: 54538.25},
//   {territory: "External", quarter: "Q3 2014", profit: 22339.65},
//   {territory: "External", quarter: "Q4 2014", profit: 26487.8},
//   {territory: "Far West", quarter: "Q1 2013", profit: 278130.95},
//   {territory: "Far West", quarter: "Q2 2013", profit: 355180.3},
//   {territory: "Far West", quarter: "Q3 2013", profit: 277655.1},
//   {territory: "Far West", quarter: "Q4 2013", profit: 339116.05},
//   {territory: "Far West", quarter: "Q1 2014", profit: 358637.15},
//   {territory: "Far West", quarter: "Q2 2014", profit: 378244.35},
//   {territory: "Far West", quarter: "Q3 2014", profit: 360947.75},
//   {territory: "Far West", quarter: "Q4 2014", profit: 313951.6},
//   {territory: "Great Lakes", quarter: "Q1 2013", profit: 280034.45},
//   {territory: "Great Lakes", quarter: "Q2 2013", profit: 319310.55},
//   {territory: "Great Lakes", quarter: "Q3 2013", profit: 332849.1},
//   {territory: "Great Lakes", quarter: "Q4 2013", profit: 270933.85},
//   {territory: "Great Lakes", quarter: "Q1 2014", profit: 302933.6},
//   {territory: "Great Lakes", quarter: "Q2 2014", profit: 378663.75},
//   {territory: "Great Lakes", quarter: "Q3 2014", profit: 308821.75},
//   {territory: "Great Lakes", quarter: "Q4 2014", profit: 343936.35},
// ]

// const quarters =  ["Q1 2013", "Q2 2013", "Q3 2013", "Q4 2013", "Q1 2014", "Q2 2014", "Q3 2014", "Q4 2014"]


const ForkGraph = () => {

  const { repo1, repo2 } = useParams();
  const [fork, setFork] = useState(null);
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
        ith_week_dic["quarter"] = j
        ith_week_dic["profit"] = commit_list[j]
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
  console.log("forks list response", response.data.forks);
  setFork(response.data.forks);
  setData(getDataList(response.data.forks))
  setForkNames(getForkNames(response.data.forks))
}, []);

  useEffect(() => {
    const repo = repo1 + "/" + repo2;
    fetchForks(repo);
  }, [fetchForks]);
    
  return (
    // data && fork_names ? <ForkRank></ForkRank> : <Loading></Loading>
      
    data && fork_names ? <ForkRank data={data} territories={fork_names}></ForkRank> : <Loading></Loading>
  );
}

export default ForkGraph;