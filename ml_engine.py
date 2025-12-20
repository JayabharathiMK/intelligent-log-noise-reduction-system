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
    Identifies noise by finding duplicates within clusters or generally.
    Returns a dataframe with 'Noise Reduced' items (unique representative).
    """
    if 'Cluster' not in df.columns:
        return df
    
    # For each cluster, we can pick one representative or aggregate.
    # Here, we will just count occurrences to show noise level.
    noise_summary = df.groupby(['Cluster', 'Cleaned Log']).size().reset_index(name='Count')
    
    # Get representative original log for each cleaned log group
    # We take the first original log message that maps to the cleaned log
    representatives = []
    for index, row in noise_summary.iterrows():
        # Cleaned Log matches, get the first original text
        subset = df[df['Cleaned Log'] == row['Cleaned Log']]
        if not subset.empty:
            original = subset[target_col].iloc[0]
            representatives.append(original)
        else:
            representatives.append("N/A")
    
    noise_summary['Representative Log'] = representatives
    
    noise_summary['Representative Log'] = representatives
    
    # Sort by count to show most frequent (noisy) logs
    noise_summary = noise_summary.sort_values(by='Count', ascending=False)
    
    return noise_summary
