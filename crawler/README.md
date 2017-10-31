# INFOX/crawler

How to run: 
> git clone git@github.com:FancyCoder0/INFOX.git
>
> cd INFOX
>
> python run.py

The results are stored in ./result. There is an example of result in ./data/result.

You can also set config.conf and run manually.

The crawler part & analyser part are separated, you can run individually.

crawler.py is to get the information of the project and the forks of it. Now, the data is storing in local.

analyser.py is to do analysis from local data and show the result.

compare_changes_crawler.py is used for comparing the diff bewteen two repos.

Now, it only supports this languages: C, C++.

