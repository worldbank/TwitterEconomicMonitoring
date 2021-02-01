# Twitter tutorials

## Introduction
The rapid escalation of the COVID-19 crisis has emphasized the need to extract real-time policy insights from big data sources to compensate for the limitations of other data sources. In this project, we provide training material to educate practitioners on how to generate indicators out of Twitter data on crucial issues associated with the COVID-19 crisis with a focus on unemployment, public sentiment, and misinformation, with practical examples focusing on in Brazil, Mexico, and Pakistan.

## Twitter as a complementary data source

The booming use of social media platforms, such as Twitter, made individuals’ daily preoccupations and interests available to researchers. Compared to traditional public-intent data, social media measures, by design, can identify shifts in public opinion earlier and provide a more granular picture of heterogeneity in the population. It can also inform and enhance the targeting of surveys and bring a new lens for understanding public opinion on economic policy. On top of their informational value, these new data sources have the advantage of being easily accessible. In the case of Twitter, the data is accessible to all users with a Developer account.

Yet, an important challenge when working with Twitter data is the lack of representativeness of the Twitter population. Being on Twitter requires being literate, having a good Internet connection and an email address. This restricts the potential share of the population with a Twitter account to a relatively richer, younger share of the population. Even if individuals have access to these resources and use social media networks for example, the data produced by these networks is not necessarily representative of all of its users. According to Twitter, in 2011, 40% of the network’s active users would sign in just to read messages from other users. Some users may not even be humans, with between 9% and 15% of 2017 Twitter active users being bots (Varol et al., 2017). 

One solution to this challenge is to combine demographic inference of Twitter users and post-stratification to build more representative samples. One solution to get user demographics is to match users with existing datasets containing individual socioeconomic information. For instance, Grinberg et al. (2019) match Twitter accounts with U.S. registered voters using their name. When such a dataset as the U.S. voting registry is not available, which is the case for most of the rest of the world, demographics, such as age, gender or whether the account belong to an organization, can be inferred based on user information (Nguyen et al., 2013; Chamberlain et al., 2017; Wang et al., 2019). In this learning material, we include one notebook on demographic inference, and more specifically gender inference, as a first step to address this challenge. 
 

## Content
This repository contains the following:
- A `notebooks` folder containing the Jupyter notebooks in `ipynb` format and related files
  - `1-download-from-twitter-api.ipynb`: details how to download tweets from the Twitter API using the module `tweepy`
  - `2-machine-translation.ipynb`: shows how to use state-of-the-art translation models from the Hugging Face model hub
  - `3-sentiment-analysis.ipynb`: performs sentiment analysis on Pakistani tweets with Hedonometer
  - `4-build-unemployment-index.ipynb`: builds an unemployment index from tweets for Mexico 
  - `5-misinformation-analysis.ipynb`: quantifies misinformation in COVID-19-reltaed tweets by looking for links whose domains are listed as fake news by [Newsguard](https://www.newsguardtech.com/coronavirus-misinformation-tracking-center/)
  - `6-gender-inference`: infers gender of Brazilian Twitter users 
  - An `outputs` folder containing graphs outputted by the notebooks
- `README.md`: the present file
  
  
## Requirements
- The notebooks are written in Python 3. You therefore need a minimum knowledge of Python and famous Python modules such as `pandas` to understand these tutorials.
- There are no compulsory package requirements as all notebooks can be run on the cloud in Google Colab. To open a notebook in Google Colab, simply click on the ![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg) icon at the top of that notebook. In case you prefer to run the notebooks locally, specific package requirements are indicated at the top of each notebook.

## References

Dodds, P., Clark, E., Desu, S., Frank, M., Reagan, A., Williams, J., Mitchell, L., Harris, K., Kloumann, I., Bagrow, J., Megerdoomian, K., McMahon, M., Tivnan, B., & Danforth, C.. (2014). Human language reveals a universal positivity bias.

Thomas Wolf, Lysandre Debut, Victor Sanh, Julien Chaumond, Clement Delangue, Anthony Moi, Pierric Cistac, Tim Rault, Rémi Louf, Morgan Funtowicz, Joe Davison, Sam Shleifer, Patrick von Platen, Clara Ma, Yacine Jernite, Julien Plu, Canwen Xu, Teven Le Scao, Sylvain Gugger, Mariama Drame, Quentin Lhoest, & Alexander M. Rush (2020). Transformers: State-of-the-Art Natural Language Processing. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: System Demonstrations (pp. 38–45). Association for Computational Linguistics.

Roesslein, J. (2020). Tweepy: Twitter for Python!URL: https://github.com/tweepy/tweepy.

Varol, O., Ferrara, E., Davis, C., Menczer, F., & Flammini, A. (2017, May). Online human-bot interactions: Detection, estimation, and characterization. In Proceedings of the International AAAI Conference on Web and Social Media (Vol. 11, No. 1).

Grinberg, N., Joseph, K., Friedland, L., Swire-Thompson, B., & Lazer, D. (2019). Fake news on Twitter during the 2016 US presidential election. Science, 363(6425), 374-378.

Nguyen, D., Gravel, R., Trieschnigg, D., & Meder, T. (2013, June). " How Old Do You Think I Am?" A Study of Language and Age in Twitter. In Proceedings of the International AAAI Conference on Web and Social Media (Vol. 7, No. 1).

Chamberlain, B. P., Humby, C., & Deisenroth, M. P. (2017, September). Probabilistic inference of twitter users’ age based on what they follow. In Joint European Conference on Machine Learning and Knowledge Discovery in Databases (pp. 191-203). Springer, Cham.

Wang, Z., Hale, S., Adelani, D. I., Grabowicz, P., Hartman, T., Flöck, F., & Jurgens, D. (2019, May). Demographic inference and representative population estimates from multilingual social media data. In The World Wide Web Conference (pp. 2056-2067).
