# The Return Power of Stock Analyst Report: Definition, Factor and Strategy

This repository provides the data and codes for the paper entitled "The Return Power of Stock Analyst Report: Definition, Factor and Strategy". As you may see, there are mainly three files in this repository. 

- **codes file** includes all the `Python` codes for data processing and `Stata` codes for empirical analysis. 
- **data file** contains data of analyst reports as well as other supplemental data, such as stock list, broker list and star analyst list. 
- **result file** contains some results that were not fully displayed in the paper, including the t-test results of return power over 90 days after release of analyst reports, and the recommended portfolios predicted through vavrious models, such as regression model, tree models and neural networks. 


## Notes
- When using the codes, you may first `clone` the repository and then implement it in the `Python 3.9` and `Stata 17` environment. 
- If you want to fastly replicate the empirical analysis, please directly use the data `report_data.dta` and conduct the regression following the Stata code `stata_regression.do`. 
- If you want to test the prediction performance of trading strategy and validate the profitabiltiy, please conduct the Python code files of `model_prediction.py` and `back_testing.py`.
- If you have questions, please feel free to file an issue in this repository.