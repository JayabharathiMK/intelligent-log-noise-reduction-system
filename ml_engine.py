import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import re

def clean_log(log_message):
    """
    Basic cleaning of log messages to remove timestamps, IPs, etc.
    This helps in better clustering.
    """
    # Remove timestamps (heuristic: assuming generic formats)
    log_message = re.sub(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', '', log_message)
    # Remove numbers (IDs, etc.) to generalize
    log_message = re.sub(r'\d+', '<NUM>', log_message)
    # Remove IP addresses
    log_message = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '<IP>', log_message)
    return log_message.strip()

def cluster_logs(df, n_clusters=5, target_col='Log Message'):
    """
    Clusters logs using TF-IDF and KMeans.
    Expects df to have the target_col column.
    """
    if target_col not in df.columns:
        raise ValueError(f"DataFrame must contain '{target_col}' column")
    
    # Clean logs for processing
    # If using email, cleaning might not be strictly necessary, but good for consistency
    df['Cleaned Log'] = df[target_col].apply(str).apply(clean_log)
    
    # Vectorize
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df['Cleaned Log'])
    
    # Cluster
    # Adjust n_clusters if dataset is small
    true_k = min(n_clusters, len(df))
    if true_k > 0:
        model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init='auto')
        model.fit(X)
        df['Cluster'] = model.labels_
    else:
         df['Cluster'] = 0
    
    return df

def identify_noise(df, target_col='Log Message'):
    """
    Identifies noise by finding exact duplicates of actual log messages within clusters.
    This version keeps column names 'Count' and 'Representative Log' for 
    compatibility with the UI while ensuring specific IDs are not grouped together.
    """
    if 'Cluster' not in df.columns or df.empty:
        return df
    
    # We group by the original email/log to keep 020 and 045 separate
    noise_summary = df.groupby(['Cluster', target_col, 'Cleaned Log']).size().reset_index(name='Count')
    
    # Rename the original log column to 'Representative Log' for the UI
    noise_summary = noise_summary.rename(columns={target_col: 'Representative Log'})
    
    # Sort by frequency to show most frequent logs at top
    noise_summary = noise_summary.sort_values(by='Count', ascending=False)
    
    # Ensure columns are in the expected order for the UI table
    cols = ['Cluster', 'Cleaned Log', 'Count', 'Representative Log']
    return noise_summary[cols]

def compare_log_sets(df_baseline, df_current, n_clusters=5, target_col='Log Message'):
    """
    Compares two sets of logs and identifies 'New Patterns' in the current set
    that were not present in the baseline.
    """
    if df_baseline.empty or df_current.empty:
        return pd.DataFrame()

    # Process baseline to get unique patterns
    baseline_clustered = cluster_logs(df_baseline.copy(), n_clusters, target_col)
    baseline_patterns = set(baseline_clustered['Cleaned Log'].unique())

    # Process current
    current_clustered = cluster_logs(df_current.copy(), n_clusters, target_col)
    
    # Identify logs in current that don't match any pattern in baseline
    current_clustered['Is New Pattern'] = current_clustered['Cleaned Log'].apply(
        lambda x: x not in baseline_patterns
    )
    
    # Filter to show only new patterns
    new_patterns = current_clustered[current_clustered['Is New Pattern']].copy()
    
    if new_patterns.empty:
        return pd.DataFrame()

    # Group by the new patterns to show a summary
    new_summary = new_patterns.groupby(['Cleaned Log', target_col]).size().reset_index(name='Occurrences')
    new_summary = new_summary.rename(columns={target_col: 'Example Log'})
    
    return new_summary.sort_values(by='Occurrences', ascending=False)
