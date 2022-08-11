import React from "react";
import * as d3 from 'd3';

const ForkRank = ({
    data,
    fork_names
  }) => {

      const ref = React.useRef();

      const weeks =  Array.from(Array(52).keys());
    
      React.useEffect(() => {
          const height = 1000;
          const width = 1500;
          const padding = 25;
          const margin = {left: 105, right: 105, top: 20, bottom: 50};

        const svg = d3.select(ref.current);
        // const svg = d3.select('.plot-area');

        // draw dashed line
        const seq = (start, length) => 
            Array.apply(null, {length: length}).map((d, i) => i + start);
          
        
        const bx = d3.scalePoint()
                .domain(seq(0, weeks.length))
                .range([0, width - margin.left - margin.right - padding * 2])
        
        
        //2. chart
        const ti = new Map(fork_names.map((territory, i) => [territory, i]));
        const qi = new Map(weeks.map((week, i) => [week, i]));  
                   
        const matrix = Array.from(ti, () => new Array(weeks.length).fill(null));  
              for (const {territory, week, commits} of data) 
                     matrix[ti.get(territory)][qi.get(week)] = {rank: 0, commits: +commits, next: null};
                   
                   matrix.forEach((d) => {
                       for (let i = 0; i<d.length - 1; i++) 
                         d[i].next = d[i + 1];
                   });
                   
                   weeks.forEach((d, i) => {
                     const array = [];
                     matrix.forEach((d) => array.push(d[i]));
                     array.sort((a, b) => b.commits - a.commits);
                     array.forEach((d, j) => d.rank = j);
                   });

        //before step 2
        // get ranking           
        const chartData =  matrix;
        const len = weeks.length - 1;
        const ranking = chartData.map((d, i) => ({territory: fork_names[i], first: d[0].rank, last: d[len].rank}));
        // get color
        const color = d3.scaleOrdinal(d3.schemeTableau10)
                        .domain(seq(0, ranking.length))
    
        const left = ranking.sort((a, b) => a.first - b.first).map((d) => d.territory);
        const right = ranking.sort((a, b) => a.last - b.last).map((d) => d.territory);

        const strokeWidth = d3.scaleOrdinal()
                        .domain(["default", "transit", "compact"])
                        .range([5, bumpRadius * 2 + 2, 2]);
        const drawingStyle = 'default';
        const bumpRadius = 13
        const by = d3.scalePoint()
        .domain(seq(0, ranking.length))
        .range([margin.top, height - margin.bottom - padding])

        function restore() {
          series.transition().duration(500)
            .attr("fill", s => color(s[0].rank)).attr("stroke", s => color(s[0].rank));    
          restoreTicks(leftY);
          restoreTicks(rightY);
          
          function restoreTicks(axis) {
            axis.selectAll(".tick text")
              .transition().duration(500)
              .attr("font-weight", "normal").attr("fill", "black");
          }
        }

        function highlight(e, d) {       
          this.parentNode.appendChild(this);
          series.filter(s => s !== d)
            .transition().duration(500)
            .attr("fill", "#ddd").attr("stroke", "#ddd");
          markTick(leftY, 0);
          markTick(rightY,  weeks.length - 1);
          
          function markTick(axis, pos) {
            axis.selectAll(".tick text").filter((s, i) => i === d[pos].rank)
              .transition().duration(500)
              .attr("font-weight", "bold")
              .attr("fill", color(d[0].rank));
          }
      }
   
        //dashed line
          svg.append("g")
          .attr("transform", `translate(${margin.left + padding},0)`)
          .selectAll("path")
          .data(seq(0, weeks.length))
          .join("path")
          .attr("stroke", "#ccc")
          .attr("stroke-width", 2)
          .attr("stroke-dasharray", "5,5")
          .attr("d", d => d3.line()([[bx(d), 0], [bx(d), height - margin.bottom]]));

          const series = svg.selectAll(".series")
          .data(chartData)
          .join("g")
          .attr("class", "series")
          .attr("opacity", 1)
          .attr("fill", d => color(d[0].rank))
          .attr("stroke", d => color(d[0].rank))
          .attr("transform", `translate(${margin.left + padding},0)`)
          .on("mouseover", highlight)
          .on("mouseout", restore);

          
        

          series.selectAll("path")
          .data(d => d)
          .join("path")
          .attr("stroke-width", strokeWidth(drawingStyle))
          .attr("d", (d, i) => { 
            if (d.next) 
              return d3.line()([[bx(i), by(d.rank)], [bx(i + 1), by(d.next.rank)]]);
          })

          const title = g => g.append("title")
                        .text((d, i) => `${d.territory} - ${weeks[i]}\nRank: ${d.commits.rank + 1}\nProfit: ${d.commits.commits}`)

          const bumps = series.selectAll("g")
          .data((d, i) => d.map(v => ({territory: fork_names[i], commits: v, first: d[0].rank})))
          .join("g")
          .attr("transform", (d, i) => `translate(${bx(i)},${by(d.commits.rank)})`)
          //.call(g => g.append("title").text((d, i) => `${d.territory} - ${weeks[i]}\n${toCurrency(d.commits.commits)}`)); 
          .call(title);

        const ax = d3.scalePoint()
                     .domain(weeks)
                     .range([margin.left + padding, width - margin.right - padding]);

        const y = d3.scalePoint()  
        .range([margin.top, height - margin.bottom - padding]);
        
        const compact = drawingStyle === "compact";
        bumps.append("circle").attr("r", compact ? 5 : bumpRadius);
        bumps.append("text")
            .attr("dy", compact ? "-0.75em" : "0.35em")
            .attr("fill", compact ? null : "white")
            .attr("stroke", "none")
            .attr("text-anchor", "middle")    
            .style("font-weight", "bold")
            .style("font-size", "14px")
            .text(d => d.commits.rank + 1); 
        
        
        
        const drawAxis = (g, x, y, axis, domain) => {
            g.attr("transform", `translate(${x},${y})`)
                .call(axis)
                .selectAll(".tick text")
                .attr("font-size", "12px");
                
            if (!domain) g.select(".domain").remove();
        }
    
        

        //Axis
        svg.append("g").call(g => drawAxis(g, 0, height - margin.top - margin.bottom + padding, d3.axisBottom(ax), true));
        const leftY = svg.append("g").call(g => drawAxis(g, margin.left, 0, d3.axisLeft(y.domain(left))));
        const rightY = svg.append("g").call(g => drawAxis(g, width - margin.right, 0, d3.axisRight(y.domain(right)))); 
             
        },
        [data.length]
      );
    
      return (
        <svg
          ref={ref}
          style={{
            height: 1000,
            width:  1500,
            marginRight: "0px",
            marginLeft: "0px",
          }}
        >
          <g className="plot-area" />
        </svg>
      );
}
export default ForkRank;