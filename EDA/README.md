# 📁 EDA – Exploratory Data Analysis of [ExeBench Dataset](https://huggingface.co/datasets/jordiae/exebench)

> This folder contains scripts for performing **exploratory data analysis** (EDA) on the dataset of C functions and their corresponding assembly representations used for the machine learning decompilation project.

## What is EDA?

Exploratory Data Analysis (EDA) is an approach to analyzing datasets to summarize their main characteristics, often using visual methods. In simpler terms, it's like being a detective for your data. You're not trying to prove a specific hypothesis (that comes later with more formal modeling or statistical testing). Instead, you're exploring the data with an open mind to:

* **Understand its structure:** What kind of data do you have? How many variables? What are their types (numerical, categorical, etc.)?
* **Identify patterns and trends:** Are there any obvious relationships between variables? Do you see any clusters or groupings?
* **Detect outliers and anomalies:** Are there any unusual data points that stand out?
* **Check for data quality issues:** Are there missing values? Inconsistent formatting? Errors in the data?
* **Formulate hypotheses:** Based on your initial observations, what interesting questions could you investigate further?
* **Gain intuition about the data:** Develop a deeper understanding of the underlying processes that might have generated the data.

EDA is often an iterative process. You might start with a broad overview and then zoom in on specific aspects as you uncover interesting findings. It involves a combination of statistical summaries and graphical techniques.

### Why is EDA Useful for Understanding a Dataset?

Working with a new dataset without performing EDA is like trying to build a house without looking at the blueprints or inspecting the materials. You might be able to put something together, but you're likely to encounter problems down the line. Here's why EDA is crucial for understanding a dataset:

* **Uncovers Hidden Insights:** EDA can reveal patterns, relationships, and anomalies that might not be apparent from simply looking at raw data or summary statistics. Visualizations, in particular, can make complex relationships easier to grasp.

* **Improves Data Quality:** By identifying missing values, outliers, and inconsistencies early on, you can take appropriate steps to clean and preprocess the data. This ensures that any subsequent analysis or modeling is based on reliable information.

* **Guides Feature Engineering:** Understanding the relationships between variables can inspire ideas for creating new features that might improve the performance of machine learning models or provide more meaningful insights.

* **Informs Model Selection:** The characteristics of your data, such as its distribution, the presence of outliers, or the relationships between variables, can influence the choice of appropriate statistical models or machine learning algorithms.

* **Validates Assumptions:** Many statistical techniques and machine learning models make certain assumptions about the data (e.g., normality, linearity). EDA helps you check if these assumptions are likely to be met.

* **Communicates Findings Effectively:** Visualizations created during EDA can be powerful tools for communicating your understanding of the data to others, whether they are technical experts or non-technical stakeholders.

* **Reduces the Risk of Errors:** By thoroughly exploring the data, you're less likely to make mistakes in your analysis or build flawed models based on a misunderstanding of the underlying data.

**In essence, EDA helps you become intimately familiar with your data. It transforms a collection of numbers and text into a story you can understand and use to answer meaningful questions or build effective solutions.** By investing time in EDA, you lay a solid foundation for more rigorous analysis and ultimately achieve more reliable and insightful results.

Absolutely, partner! Here's a `README.md` for the `EDA/` folder of your ML project on **decompiling C functions from assembly**, listing important analyses to guide your exploratory data analysis. It includes what you've already done (lines of code) and suggests additional valuable directions.

---

## 📌 Current and Planned Analyses

### ✅ `lines_of_code_analysis.py`

* Extracts function definitions from compressed `.jsonl.zst` files
* Calculates number of lines of code per function
* Plots:

  * Histogram of line counts
  * Box plot
  * Cumulative distribution function (CDF)

---

## 🔍 Suggested Future Analyses

> Each of these should have its own script and visualization, and can be used to inform preprocessing, filtering, or model design.

### 1. `token_count_analysis.py`

* Count number of tokens per function (via `tokenize` or `tree-sitter`)
* Useful for understanding model input length
* Visualizations: histogram, CDF

### 2. `cyclomatic_complexity_analysis.py`

* Estimate cyclomatic complexity of each C function
* Helps identify how complex the control flow is
* Tool: `lizard`, `radon`, or a custom parser

### 3. `identifier_entropy_analysis.py`

* Measure the diversity and frequency of identifiers (e.g., variable names)
* Useful for understanding naming patterns, obfuscation, or boilerplate

### 4. `assembly_size_analysis.py`

* Compare C function length vs. corresponding assembly instruction count
* Insight into binary expansion rate
* Could help in learning compression mapping

### 5. `function_type_distribution.py`

* Classify functions by type (e.g., I/O, math, control, string)
* Count and visualize their distribution

### 6. `syntax_structure_analysis.py`

* Analyze frequency of specific syntax patterns (e.g., if, for, while, switch)
* Good for feature engineering

### 7. `comment_density_analysis.py`

* If comments are included, compute ratio of comment lines to code lines
* Insight into documentation or code quality

### 8. `outlier_detection.py`

* Detect functions with extreme values in line count, token count, etc.
* Helps clean or filter noisy training examples

### 9. `duplicate_function_analysis.py`

* Identify near-duplicate or identical functions (e.g., via hashing or Levenshtein)
* Useful for deduplication or data leakage detection

---

## 📦 EDA folder Structure

```plaintext
EDA/
├── README.md
└── line_of_code
    └── line_of_code.py
```

---

## 📈 Tools and Libraries Recommended

* `matplotlib`, `seaborn` – for visualization
* `numpy`, `pandas` – for data manipulation
* `lizard` – for code complexity metrics
* `tree-sitter`, `pycparser` – for code parsing
* `difflib`, `hashlib` – for similarity detection

## Setup
Apart from the libraries mentioned above, you may need to download the dataset, instructions for which can be found in the `examples/README.md` file.


