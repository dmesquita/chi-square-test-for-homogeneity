# Chi-square test for homogeneity

This code uses the [gitter-history dataset from freeCodeCamp open data](https://github.com/freeCodeCamp/open-data/tree/master/gitter-history) to answer this question: **is there a different mention pattern in  different cities?** 

To extract the mentions we use the Matcher class from spaCy and for the chi-square test we use R.
## Files
| File | Description |
|--|--|
| extraction_rules.py | Matcher patterns |
| extract_data.py | Creates a json file indicating if a message has a mention or not |
| create_sample.py | Creates a json file with [menssage, mention, sent_at, city] | 
| Explore data and create sample.ipynb | Creates a json file with messages sent between 2015–08–16 and 2016–08–16 (one year of messages) |
| chi_squared_test.r | Executes the chi-square test |



