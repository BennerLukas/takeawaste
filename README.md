<div align="center">

<img src="doc/logo.png" alt="Logo" width="400" align="center"/>
<br>
<br>
<br>
<br>

[![GitHub issues](https://img.shields.io/github/issues/BennerLukas/takeawaste)](https://github.com/BennerLukas/takeawaste/issues)
[![GitHub forks](https://img.shields.io/github/forks/BennerLukas/takeawaste)](https://github.com/BennerLukas/takeawaste/network)
[![GitHub stars](https://img.shields.io/github/stars/BennerLukas/takeawaste)](https://github.com/BennerLukas/takeawaste/stargazers)
[![GitHub license](https://img.shields.io/github/license/BennerLukas/takeawaste)](https://github.com/BennerLukas/takeawaste/blob/main/LICENSE)

</div>


## Preparation for manual execution
- Create an Anaconda Environment for Python version 3.7
- Install the requirements.txt
- load your [data](https://www.kaggle.com/datasets/henslersoftware/19560-indian-takeaway-orders) in the 'data' directory and adapt the metadata.json if needed.

## Setup
- Create a MySQL Database Server. Easily with docker:
```bash 
docker run --name takeawaste -p 3306:3306 -e MYSQL_ROOT_PASSWORD=1234 -d mysql:latest
```

- Run the takeawaste.py file

## The Team
- [Ayman Madhour](https://github.com/Madhour)
- [Lukas Benner](https://github.com/BennerLukas)
- [Marius Kiskemper](https://github.com/Marius2311)
- [Marvin Vielmeyer](https://github.com/MarvV8)
- [Oliver Wieder](https://github.com/OWDSC)
- [Fabian Creutz](https://github.com/yellowsh29)

## The Idea
There is no denying that the world has a food waste problem.
According to the United Nations Environment Programme, 1.3 billion tonnes of food are wasted every year, which corresponds to about one third of food produced.
This is a problem because not only is this wasted food also a huge waste of resources, but it also takes a toll on the environment.
Food waste is a major contributor to greenhouse gas emissions. When food waste decomposes in landfills, it emits methane, a powerful greenhouse gas.

The approach taken in this project aims to raise awareness of the food waste problem that is associated with the food service industry. The vast amount of data available to takeaway platforms on food consumption and behavior is a not thoroughly exploited goldmine for reducing waste.
Based on takeaway data, a forecasting system is developed that estimates the requests per dish and gives a recommendation for action to the restaurant owner.

For more information, read the [whitepaper](doc/TakeAwaste-Paper.pdf) or [presentation](doc/TakeAwaste.pdf).
