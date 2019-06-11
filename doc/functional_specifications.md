# Functional Specifications

### Background
The participation rate in marathons is increasing year by year, rendering a huge market of runners preparing for them. The worldwide growth from 2008 to 2018 was +49.43%. Women are picking up faster than men with a growth of +56.83% while men’s participation rate has increased +46.91%. The Abbott World Marathon Majors is a championship-style competition for marathon runners that started in 2006. A points based competition founded on six major city marathon races, the series currently comprises annual races for the cities of Tokyo, Boston, London, Berlin, Chicago and New York City, with about a million dollars worth in prize money associated with it. While preparing for these marathons around the world, athletes often want to know where their current preparation stands, record their progress and measure it and identify what areas they need to work more on. A novice runner may be struggling with finishing a given distance milestone, while a trained runner might be working on finishing in a fixed time.


This project is a dashboard intended to help runners train better for upcoming marathons in the Abbott World Marathon Majors. We have taken the finishers data from all the mentioned Marathons (except Tokyo) over years 2013-2017. The tool gives runner an idea of where they currently stand as compared to runners in previous years for one or all of these marathons. It gives a demographic comparison to the user based on their age and gender. It also gives information on running techniques and fatigue zones, to improve the runner's ability to perform better.

### User profile
Primarily, this tool is targeted towards users preparing for major marathons globally and want to understand where they stand per their current preparation relative to runners from previous years. Users are not expected to bring any computing or programming background to use this product; only have to feed in the summary statistics corresponding to their run. The UI is to be intuitive enough that the user understands how to interact with the tool. The primary user base is:
##### The Novice Runner:

The runner has just started preparing for long run marathons and wants to track their performance, time it and better their run time. Their target is finishing the marathon.

##### The Trained Runner:

The runner is an experienced marathon runner and wants to use the tool to improve their standing among the top performers in the marathons. They want to understand where they lie relative to others following their running strategy, which time splits they want to improve in, and what their fatigue zones are.

### Data sources

* Boston marathon dataset for years 2015-17 ([link](https://www.kaggle.com/rojour/boston-results))
* Boston marathon dataset for years 2013-15 ([link](https://github.com/llimllib/bostonmarathon))
* NYC marathon dataset for years 2013-17 ([link](https://github.com/andreanr/NYC-Marathon/tree/master/data/clean))
* Chicago marathon dataset for years 2013-17 ([link](http://chicago-history.r.mikatiming.de/2015/))
* London marathon dataset for years 2013-17 ([link](http://results-2017.virginmoneylondonmarathon.com/2017/))
* Berlin marathon dataset for years 2013-17 ([link](http://results.scc-events.com/2016/))

### Use cases
##### Use Case 1

User 1 is a novice marathon runner who completes a run and keeps track of time taken to achieve basic distance milestones (like 5k,10k,15k, etc. splits) during that run. Once the distance milestone has been selected by the user in the tool, and the age and gender has been selected, the user is able to see a their performance in their demography for the chosen milestone relative to the past runners. The tool also enables the user to know where the user’s fatigue zone during the run. This user is more interested in knowing where he lies with respect to the average performance of a runner in the marathon. They also want to understand whether their split ratio strategy was improving and how their pace was.

##### Use Case 2

User2 is a seasoned marathon runner who has just finished a 40k run. The user tracks the time it took to complete the milestones enroute and enters values in the dashboard. The tool displays how the user’s current ranking would vary across milestones given the user’s current run in their demography (age, gender). It gives them information about their split ratio standing and the area of fatigue they need to work on. They are more interested in comparison with a more competitive crowd, like the top 10 percentile and wants to observe whether their pace was constant or if they were following their split ratio strategy well.
