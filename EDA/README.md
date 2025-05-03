# Exploratory Data Analysis (EDA) of [ExeBench Dataset](https://huggingface.co/datasets/jordiae/exebench)

## What is EDA?

Exploratory Data Analysis (EDA) is an approach to analyzing datasets to summarize their main characteristics, often using visual methods. In simpler terms, it's like being a detective for your data. You're not trying to prove a specific hypothesis (that comes later with more formal modeling or statistical testing). Instead, you're exploring the data with an open mind to:

* **Understand its structure:** What kind of data do you have? How many variables? What are their types (numerical, categorical, etc.)?
* **Identify patterns and trends:** Are there any obvious relationships between variables? Do you see any clusters or groupings?
* **Detect outliers and anomalies:** Are there any unusual data points that stand out?
* **Check for data quality issues:** Are there missing values? Inconsistent formatting? Errors in the data?
* **Formulate hypotheses:** Based on your initial observations, what interesting questions could you investigate further?
* **Gain intuition about the data:** Develop a deeper understanding of the underlying processes that might have generated the data.

EDA is often an iterative process. You might start with a broad overview and then zoom in on specific aspects as you uncover interesting findings. It involves a combination of statistical summaries and graphical techniques.

## Why is EDA Useful for Understanding a Dataset?

Working with a new dataset without performing EDA is like trying to build a house without looking at the blueprints or inspecting the materials. You might be able to put something together, but you're likely to encounter problems down the line. Here's why EDA is crucial for understanding a dataset:

* **Uncovers Hidden Insights:** EDA can reveal patterns, relationships, and anomalies that might not be apparent from simply looking at raw data or summary statistics. Visualizations, in particular, can make complex relationships easier to grasp.

* **Improves Data Quality:** By identifying missing values, outliers, and inconsistencies early on, you can take appropriate steps to clean and preprocess the data. This ensures that any subsequent analysis or modeling is based on reliable information.

* **Guides Feature Engineering:** Understanding the relationships between variables can inspire ideas for creating new features that might improve the performance of machine learning models or provide more meaningful insights.

* **Informs Model Selection:** The characteristics of your data, such as its distribution, the presence of outliers, or the relationships between variables, can influence the choice of appropriate statistical models or machine learning algorithms.

* **Validates Assumptions:** Many statistical techniques and machine learning models make certain assumptions about the data (e.g., normality, linearity). EDA helps you check if these assumptions are likely to be met.

* **Communicates Findings Effectively:** Visualizations created during EDA can be powerful tools for communicating your understanding of the data to others, whether they are technical experts or non-technical stakeholders.

* **Reduces the Risk of Errors:** By thoroughly exploring the data, you're less likely to make mistakes in your analysis or build flawed models based on a misunderstanding of the underlying data.

**In essence, EDA helps you become intimately familiar with your data. It transforms a collection of numbers and text into a story you can understand and use to answer meaningful questions or build effective solutions.** By investing time in EDA, you lay a solid foundation for more rigorous analysis and ultimately achieve more reliable and insightful results.

## EDA of ExeBench Dataset
### Line of code (LOC) Distribution
Note: for the moment we are only analyzing the 'data/train_synth_compilable/data_0_time1677787985_default.jsonl.zst' file. In the future we must analyze all the files in the dataset.
Also, the graph are not very informative, it should be improved before actually using it.
