# Getting Started with Snowpark for Machine Learning on SageMaker

## Overview

In this guide, we will perform data preperation and machine learning tasks to train a model to predict machine failure using Sagemaker, Snowpark for Python and scikit-learn. By the end of the session, you will have built a model in Sagemaker and deployed it to Snowflake.

## Step-By-Step Guide

For prerequisites, environment setup, step-by-step guide and instructions, please refer to the [QuickStart Guide](https://quickstarts.snowflake.com/guide/getting_started_with_snowpark_for_machine_learning_on_sagemaker/#0).


## Additional Commands required to execute in your SageMaker Terminals 

## SageMaker System Terminal
### Git clone repo
$ git clone  https://github.com/sfc-gh-jlim/sfguide-getting-started-snowpark-python-sagemaker.git

## Snowflake Snowpark & Python 3.8
$ conda create --name py38_env --override-channels -c https://repo.anaconda.com/pkgs/snowflake python=3.8 pandas snowflake-snowpark-python notebook scikit-learn matplotlib plotly

### Streamlit (pip install is required after conda install)
$ pip install streamlit

### Install Plotly (If we have any issues from the conda install)
$ pip install plotly==5.14.1

## SageMaker Image Terminal
### Snowflake Snowpark & Python 3.8
$ conda create --name py38_env --override-channels -c https://repo.anaconda.com/pkgs/snowflake python=3.8 pandas snowflake-snowpark-python notebook scikit-learn matplotlib cachetools

### Run your streamlit app in your SageMaker Image Terminal
$ cd sfguide-getting-started-snowpark-python-sagemaker

$ streamlit run app.py

### Access your streamlit app through SageMaker Jupyter Proxy
Your streamlit app can be access at the following url, take note of your own SageMaker Domain URL:

https://your_sage_maker_domain.studio.us-east-1.sagemaker.aws/jupyter/default/proxy/8501/
