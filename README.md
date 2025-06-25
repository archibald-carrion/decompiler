# **Sauron Decompiler**


<p align="center">
    <img src="doc/sauron_logo.svg" alt="Sauron Decompiler Logo" width="200"/>
</p>

This repository houses the development of the Sauron Decompiler, a machine learning-powered project dedicated to the challenging task of decompiling binary executables back into human-readable C source code. Like the mythical phoenix rising from ashes, this project aims to reconstruct the original form and logic from its compiled representation.

**Key Components:**

* **Exhaustive EDA:** Dive deep into the characteristics of the ExeBench dataset through comprehensive Exploratory Data Analysis. Uncover patterns, distributions, and insights within the binary code and its corresponding C source.
* **Rigorous Data Cleaning:** Implement robust data cleaning pipelines to ensure the quality and integrity of the used dataset, preparing it for effective machine learning model training.
* **The Decompilation Objective:** The core goal is to train and evaluate machine learning models capable of accurately translating binary code snippets from the ExeBench dataset back into semantically equivalent C code.

**Project Goal:**

To push the boundaries of automated decompilation using cutting-edge machine learning techniques, providing a valuable tool for reverse engineering, security analysis, and understanding compiled software.

## **Table of Contents**


## Methodology
During the development of the Phoenix Decompiler, we will follow the CRISP-DM (Cross-Industry Standard Process for Data Mining) methodology. This structured approach will guide us through the various stages of the project, ensuring a systematic and thorough exploration of the dataset and the decompilation process.

''' mermaid

graph TD;
    A[Business Understanding] --> B[Data Understanding];
    B --> C[Data Preparation];
    C --> D[Modeling];
    D --> E[Evaluation];
    E --> F[Deployment];
    F -->|Iterate| A;
    E -->|Refine Data| B;
    D -->|Optimize| C;

'''