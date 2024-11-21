import requests
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import math
import plotly.express as px

# Step 1: Define GitHub API base URL and headers
github_api_url = "https://api.github.com/search/repositories"
headers = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': 'Bearer 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'  # Replace with your GitHub token
}

# Step 2: Define AI/ML-related search query
query = "machine-learning OR deep-learning OR artificial-intelligence OR data-science OR AI OR ML"
params = {
    'q': query,  
    'sort': 'stars',  
    'order': 'desc',
    'per_page': 30,  
    'page': 1  
}

repositories = []
current_page = 1
max_pages = 10  

# Step 3: Paginate through multiple pages of results
while current_page <= max_pages:
    params['page'] = current_page
    response = requests.get(github_api_url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        repos = data['items']
        
        if not repos:  
            break
        
        repositories.extend(repos)  
        current_page += 1
    else:
        print(f"Failed to fetch data from page {current_page}: {response.status_code}")
        break

# Step 4: Create a list of repository details with an additional "Last Updated" column
repo_list = []
for repo in repositories:
    if repo['language'] == 'HTML':  # Exclude repositories with language set to HTML
        continue
    repo_details = requests.get(f"https://api.github.com/repos/{repo['full_name']}", headers=headers).json()
    repo_list.append({
        'Name': repo['name'],
        'Full Name': repo['full_name'],
        'Stars': repo['stargazers_count'],
        'Watchers': repo_details.get('subscribers_count', 0),  
        'Language': repo['language'],
        'Description': repo['description'],
        'URL': repo['html_url'],
        'Last Updated': repo['updated_at'],
        'Created At': repo['created_at']
    })

# Convert the list to a DataFrame
df = pd.DataFrame(repo_list)

# Step 5: Get the top 10 most popular AI/ML repos (exclude HTML)
top_10_df = df.sort_values(by='Stars', ascending=False).head(10)
popular_repos = top_10_df['Full Name'].tolist()

# Step 6: Simulate star history using Logarithmic Growth and apply Exponential Smoothing
predicted_repo_list = []
current_date = datetime.now()
one_year_ago = current_date - timedelta(days=365)

for repo in repositories:
    if repo['full_name'] in popular_repos:
        continue

    created_at = datetime.strptime(repo['created_at'], '%Y-%m-%dT%H:%M:%SZ')
    if created_at < one_year_ago:
        continue

    repo_details = requests.get(f"https://api.github.com/repos/{repo['full_name']}", headers=headers).json()
    days_since_creation = (current_date - created_at).days

    if days_since_creation == 0:
        days_since_creation = 1

    alpha = repo['stargazers_count'] / math.log(days_since_creation + 1)
    historical_star_data = [alpha * math.log(day + 1) + np.random.normal(0, alpha * 0.01)
                            for day in range(1, days_since_creation + 1)]

    model = ExponentialSmoothing(historical_star_data, trend="add", seasonal=None).fit(smoothing_level=0.8, smoothing_trend=0.2)
    future_star_predictions = model.forecast(steps=180)
    predicted_stars = future_star_predictions[-1]

    alpha_watchers = repo_details.get('subscribers_count', 0) / math.log(days_since_creation + 1)
    predicted_watchers = alpha_watchers * math.log(days_since_creation + 181)

    predicted_repo_list.append({
        'Name': repo['name'],
        'Stars': repo['stargazers_count'],
        'Watchers': repo_details.get('subscribers_count', 0),  
        'Predicted Watchers (6 months)': int(predicted_watchers),  
        'Predicted Stars (6 months)': int(predicted_stars),
        'Language': repo['language'],
        'Description': repo['description'],
        'Last Updated': repo['updated_at'],
        'URL': repo['html_url']
    })

# Convert the predicted list to a DataFrame
predicted_df = pd.DataFrame(predicted_repo_list)

# Sort by predicted star count in descending order
predicted_top_10_df = predicted_df.sort_values(by='Predicted Stars (6 months)', ascending=False).head(10)

# Step 7: Save the results to CSV files
top_10_df.to_csv('top_10_ai_ml_repos.csv', index=False)
predicted_top_10_df.to_csv('predicted_top_10_ai_ml_repos.csv', index=False)

# Step 8: Visualization (Bubble Charts with Watcher Count on X-axis)

scaling_factor = 0.002  # Adjust the scaling factor

# Function to wrap long descriptions
def wrap_text(text, width=40):
    """Wrap long text descriptions to a specific width."""
    return "<br>".join([text[i:i+width] for i in range(0, len(text), width)])

# Apply text wrapping to descriptions
top_10_df['Wrapped Description'] = top_10_df['Description'].apply(lambda x: wrap_text(x, width=40))
predicted_top_10_df['Wrapped Description'] = predicted_top_10_df['Description'].apply(lambda x: wrap_text(x, width=40))

# Function to add annotations with dynamic offsets and clickable labels
def add_annotations_with_links(fig, df, x_col, y_col, label_col, url_col):
    annotations = []
    for i, row in df.iterrows():
        # Dynamically calculate offset for each point
        offset_x = (i % 2) * 50 + 40  # Alternate offsets for every other bubble
        offset_y = -(i % 2) * 50 - 40
        annotations.append(
            dict(
                x=row[x_col],
                y=row[y_col],
                text=f"<a href='{row[url_col]}' target='_blank'>{row[label_col]}</a>",  # Make label clickable
                showarrow=True,
                arrowhead=2,
                ax=offset_x,  # Set the x-offset of the label
                ay=offset_y,  # Set the y-offset of the label
                font=dict(size=12, color="blue"),
                arrowcolor="black",
                bgcolor="rgba(255,255,255,0.8)",  # White background for better readability
            )
        )
    fig.update_layout(annotations=annotations)

# Bubble chart for Top 10 Most Popular Repositories
fig_top_10 = px.scatter(top_10_df, 
                       x='Watchers', y='Stars', 
                       size=np.square(top_10_df['Stars']) * scaling_factor, color='Stars',
                       hover_name='Name', hover_data=['Language', 'Wrapped Description'], 
                       size_max=100, 
                       title='Top 10 Most Popular AI/ML Repos (Watchers vs. Stars)',
                       labels={'Watchers': 'Watchers (View Count)', 'Stars': 'Star Count', 'Name': 'Repository'})

# Add clickable annotations with dynamic offsets for Top 10
add_annotations_with_links(fig_top_10, top_10_df, 'Watchers', 'Stars', 'Name', 'URL')

# Bubble chart for Top 10 Predicted Repositories
fig_predicted = px.scatter(predicted_top_10_df, 
                           x='Predicted Watchers (6 months)', y='Predicted Stars (6 months)', 
                           size=np.square(predicted_top_10_df['Predicted Stars (6 months)']) * scaling_factor, 
                           color='Predicted Stars (6 months)',
                           hover_name='Name', hover_data=['Language', 'Wrapped Description'], 
                           size_max=100, 
                           title='Top 10 Predicted AI/ML Repos to Emerge (Predicted Watchers vs. Predicted Stars)',
                           labels={'Predicted Watchers (6 months)': 'Predicted Watchers', 
                                   'Predicted Stars (6 months)': 'Predicted Star Count', 
                                   'Name': 'Repository'})

# Add clickable annotations with dynamic offsets for Predicted Repos
add_annotations_with_links(fig_predicted, predicted_top_10_df, 'Predicted Watchers (6 months)', 'Predicted Stars (6 months)', 'Name', 'URL')

# Show the updated figures
fig_top_10.show()
fig_predicted.show()
