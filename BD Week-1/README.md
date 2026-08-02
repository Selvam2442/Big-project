# Sample Superstore - Data Analysis

## 📌 Overview
This project performs Exploratory Data Analysis (EDA) on the Sample Superstore dataset. It is designed to demonstrate data cleaning, feature engineering, and professional-grade data visualization techniques. The accompanying Jupyter Notebook has been heavily enhanced to provide a clean, readable, and presentation-ready workflow.

## 🚀 Features
- **Data Cleaning & Preprocessing:** Handles missing values and ensures correct data types (e.g., datetime conversions).
- **Feature Engineering:** Derives new actionable metrics such as `Delivery Days` from order and shipping dates.
- **Enhanced Visualizations:** Utilizes `seaborn` and `matplotlib` to create polished, modern charts with dynamic data labels, custom color palettes, and decluttered axes.
- **Styled DataFrames:** Implements pandas styling (e.g., background gradients, inline bar charts) for better tabular data presentation directly within the notebook.

## 🛠️ Tech Stack
- **Language:** Python 3
- **Libraries:**
  - `pandas` (Data manipulation and analysis)
  - `numpy` (Numerical operations)
  - `matplotlib` & `seaborn` (Data visualization)

## 📂 Project Structure
```text
├── samplesuperstore.csv                  # The raw dataset (ensure this is in your working directory)
├── Superstore_Analysis_Enhanced.ipynb    # The main Jupyter Notebook containing the analysis
└── README.md                             # Project documentation
```

## ⚙️ Installation & Usage
1. Clone the repository or download the project files.
2. Ensure you have Python installed, along with Jupyter Notebook or JupyterLab.
3. Install the required dependencies using pip:
   ```bash
   pip install pandas numpy matplotlib seaborn jupyter
   ```
4. Place the `samplesuperstore.csv` dataset in the same directory as the notebook (or adjust the path within the notebook if placed elsewhere).
5. Launch Jupyter Notebook and open the file:
   ```bash
   jupyter notebook Superstore_Analysis_Enhanced.ipynb
   ```
6. Run the cells sequentially to view the analysis and interactive visualizations.
