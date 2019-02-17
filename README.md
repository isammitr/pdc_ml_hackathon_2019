# PDC ML Hackathon 2019

Submitted by Sammit Ranade and Mihir Pargaonkar

## Data Cleaning and PreProcessing

- Checking was done to detect null values, after manual observations it was found that "None" or "" empty strings were present.
- Hence, such values were replaced by NaNs
- Different python functions like value_counts(), head(), info(), describe() were used to look further into the dataset.
- HTML tags and other RE characters like the newline(\n) character were present, thus such other strings have also been cleaned.
- After converting to NaNs, the an assessment was made to find out the outlier columns.
A benchmark of 20% has been decided since the columns with missing values less than 20% can be accepted to use in the further analysis.
- The Column wise as well Row wise checking of the missing/unknown values has been done.
- But the rows have not been dropped since they were having very less missing values present.


### Data Engineering
- A new feature has been created 'new_feature_category' which contains probable petition categories based on the '<mark>' tag used in features like 'highlight description'

## Data Visualization
- Instead of using any ETL tools, the strong visualization libraries in python have been used viz. seaborn and matplotlib
- Heatmaps, Histograms, Correlation Matrix have been used.


## Machine Learning Models
- Naive Bayes for classifying the petition_category
- SVM for predicting if the petition_is_victory is TRUE or FALSE

## Insights

- It can be inferred from the correlation heatmap that, as the progress of a petition increases, the chances of that petition being a victory also increases.
- If the primary target of the petition is a person, it is not necessary that the petition will be successfully passed or not.
- Primary target publicly visible and petition primary target type seem to be highly correlated as it can be seen with the example that if the target is a 'Group', it is publicly visible else if the target is a 'Politician', the name is not publicly visible(excluding some cases like Donald Trump)

## Deployment

- For ipynb file - jupyter notebook
- For html file - any web browser

### Version

v2

## Authors

* **Sammit Ranade** - *Student* - [LinkedIn](www.linkedin.com/in/sammitr19)
* **Mihir Pargaonkar** - *Student* - [LinkedIn](https://www.linkedin.com/in/mihir-pargaonkar-010849167/)

## Acknowledgments

* Websites such as stackoverflow.com, geeksforgeeks.com, sklearn-official-docs, were used for reference.
* Thank you to the organizing and mangement team at Clairvoyant, Pune for conducting this Hackathon.
