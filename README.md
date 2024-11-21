# AI/ML Repository Insights and Forecast

## Overview

This project analyzes and predicts trends in popular AI/ML-related repositories hosted on GitHub. By leveraging the GitHub API and statistical modeling techniques, it provides insights into the current top AI/ML repositories and forecasts the repositories likely to gain popularity in the next six months. Key features include:

- **Top Repository Analysis**: Fetching and displaying the most popular repositories based on GitHub stars and watchers.
- **Prediction Modeling**: Using logarithmic growth and exponential smoothing to predict future repository trends.
- **Data Visualization**: Bubble charts with interactive annotations for clear presentation of trends.

---

## Features

1. **Top Repository Analysis**:
   - Fetches repositories related to AI/ML, including terms like `machine-learning`, `deep-learning`, `AI`, `ML`, etc.
   - Analyzes repositories for key metrics such as stars, watchers, and language.
   - Excludes repositories using HTML as their primary language.

2. **Trend Prediction**:
   - Simulates star history using logarithmic growth models.
   - Applies exponential smoothing to predict star and watcher growth for repositories.
   - Highlights repositories expected to gain traction in the next six months.

3. **Data Visualization**:
   - **Bubble Chart for Popular Repositories**: Highlights relationships between watchers and stars.
   - **Bubble Chart for Predicted Repositories**: Displays repositories predicted to emerge as popular.
   - Clickable, annotated data points for easy access to repository URLs.

---

## Requirements

- Python 3.8+
- Libraries:
  - `requests`
  - `pandas`
  - `datetime`
  - `numpy`
  - `statsmodels`
  - `math`
  - `plotly`

---

## Setup

### Prerequisites

1. **GitHub API Token**:
   - Generate a [GitHub Personal Access Token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token) and replace it in the `Authorization` header.

2. **Install Required Libraries**:
   Run the following command to install the dependencies:
   ```bash
   pip install requests pandas statsmodels plotly
   ```

### Run the Project

1. Clone the repository and navigate to the project directory:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Run the script:
   ```bash
   python ai_ml_repo_insights.py
   ```

3. The results will be saved as CSV files:
   - `top_10_ai_ml_repos.csv`
   - `predicted_top_10_ai_ml_repos.csv`

4. Interactive visualizations will open in your default browser.

---

## Output Files

- **Top 10 AI/ML Repositories**:
  Details of the most popular repositories based on stars and watchers.

- **Predicted Top 10 AI/ML Repositories**:
  Forecasted trends for emerging AI/ML repositories.

---

## Visualization

The script generates two bubble charts:

1. **Top 10 Most Popular AI/ML Repositories**:
   - X-axis: Watchers (view count)
   - Y-axis: Stars
   - Bubble size: Star count (scaled)

2. **Top 10 Predicted AI/ML Repositories**:
   - X-axis: Predicted Watchers (6 months)
   - Y-axis: Predicted Stars (6 months)
   - Bubble size: Predicted star count (scaled)

Each data point includes a clickable link to the repository.

---

## Example Usage

- **Researchers**: Identify leading AI/ML repositories.
- **Developers**: Discover upcoming repositories for collaboration or learning.
- **Businesses**: Analyze GitHub trends to understand AI/ML technology adoption.

---

## Future Improvements

- Extend prediction model to incorporate additional metrics like issue activity or pull request frequency.
- Integrate more advanced time series models such as Prophet.
- Provide real-time updates using GitHub webhooks.

---

## Contributing

Contributions are welcome! Please submit a pull request or create an issue for suggestions.

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.
