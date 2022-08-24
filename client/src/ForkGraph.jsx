
import React, { useState, forwardRef, useEffect, useCallback } from "react";
import Select from 'react-select';
import { useParams } from "react-router-dom";
import * as d3 from 'd3';
import { getRepoForks } from "./repository";
import { getActiveForksNum } from "./repository";
import { postProgress } from "./repository";
import LinearLoading from "./common/LinearLoading"
import ForkRank from "./ForkRank";

const ForkGraph = () => {

  const options = [
    { value: 'weekly', label: 'Weekly commits within last year' },
    { value: 'daily', label: 'Daily commits within last month' },
  ];
  
  const { repo1, repo2 } = useParams();
  const [data, setData] = useState(null);
  const [selection, setSelectionState] = useState("weekly");
  const [interval, setIntervalState] = useState(null);
  const [forkNames, setForkNames] = useState(null);
  const [forkList, setForkList] = useState(null);
  const [activeForksNum, setActiveForksNum] = useState(0);
  const [progress, setProgress] = useState(0);
  const [counter, setCounter] = useState(0);

  const getDataList = (forks_list) => {
    //EXTRACT TOP TEN
    let datalist = []
    for (let i = 0; i < forks_list.length; i++) {
      let fork = forks_list[i]
      console.log(fork)
      let commit_list = fork["weekly_commit_freq"]
      for (let j = 0; j < commit_list.length; j++) {
        let ith_week_dic = {}
        ith_week_dic["week"] = j
        ith_week_dic["commits"] = commit_list[j]
        ith_week_dic["fork_name"] = fork["fork_name"]
        datalist.push(ith_week_dic)
      }
    }
    return datalist
}

const getDailyCommit = (forks_list) => {
  //EXTRACT TOP TEN
  let datalist = []
  for (let i = 0; i < forks_list.length; i++) {
    let fork = forks_list[i]
    let commit_list;
    if (Object.keys(fork["hourly_commit_freq"]).length === 0){
      commit_list = [{"days": new Array(7).fill(0)},
      {"days": new Array(7).fill(0)},
      {"days": new Array(7).fill(0)},
      {"days": new Array(7).fill(0)}]
    } else {
      commit_list = fork["hourly_commit_freq"].slice(-4)
    }
    let index = 0;
    for (let j = 0; j < 4; j++) {
      for(let k = 0 ; k < 7; k++){
        let ith_week_dic = {}
        ith_week_dic["week"] = index
        ith_week_dic["commits"] = commit_list[j]["days"][k]
        ith_week_dic["fork_name"] = fork["fork_name"]
        index += 1
        datalist.push(ith_week_dic)
      }
    }
  }
  return datalist
}

const updateData = (selection) => {
  switch(selection) {
    case 'weekly':
      setIntervalState(Array.from(Array(52).keys()))
      setData(getDataList(forkList))
      break;
    case 'daily':
      setIntervalState(Array.from(Array(28).keys()));
      setData(getDailyCommit(forkList));
      break;
    default:
      // code block
  }
}

const handleChange = (selectedOption) => {
    setSelectionState(selectedOption);
    console.log(`Option selected:`, selectedOption);
    updateData(selectedOption['value'])
    console.log(data)
    console.log(interval)
};

const getForkNames = (forks_list) => {
  let forkNames = []
  // for (let i = 0; i < forks_list.length && i < 10; i++) {
  for (let i = 0; i < forks_list.length; i++) {
    forkNames.push(forks_list[i]["fork_name"])
  }
  return forkNames
}

const fetchForks = useCallback(async (repo) => {
  console.log('repo1',repo1);
  console.log('repo2', repo2);

  //get total num of forks needs to be fetched
  const active_fork_num = await getActiveForksNum(repo);
  console.log("Active forks number is ", active_fork_num.data)
  setActiveForksNum(active_fork_num.data)

  let total_list = []
  let counter = 0
  while (counter < active_fork_num.data) {
      let res = await postProgress(repo, counter);
      console.log(res.data.forks[0])
      total_list.push(res.data.forks[0])
      counter += 1
      setCounter(counter)
      console.log(counter)
      setProgress(counter/active_fork_num.data * 100)
      console.log(progress)
  }
  console.log(total_list)

  // const response2 = await getProgress(repo);
  // console.log("Fetching nnnnnnn for ", response2)
  // const response = await getRepoForks(repo);
  // console.log("Fetching forks list for ", repo)
  // setForkList(response.data.forks);
  setForkList(total_list);
  // let data = getDailyCommit(response.data.forks)
  let data = getDailyCommit(total_list)
  let interval = Array.from(Array(28).keys());
  console.log(data)
  setIntervalState(interval)
  setData(data)
  setForkNames(getForkNames(total_list))
}, []);

  useEffect(() => {
    const repo = repo1 + "/" + repo2;
    fetchForks(repo);
  }, [fetchForks]);
    
  return (
    data && forkNames ? 
    <div>
      <Select
        value={selection}
        onChange={handleChange}
        options={options}
      />
      <ForkRank data={data} forkNames={forkNames} interval={interval}></ForkRank>
    </div>
   : <LinearLoading 
    loadingMessage={"There are " + activeForksNum + " active forks in total, currently " + counter+ " analyzed."}
    progress={progress}>

    </LinearLoading>
  );
}

export default ForkGraph;