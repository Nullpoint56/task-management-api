from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity

def get_semantically_similar_tasks(tasks, text_similarity_threshold=0.7, top_k_clusters=3):
    """
    Identify the top_k_clusters with the most participants based on task name and description similarity.

    Args:
        tasks (list): List of dictionaries containing task names and descriptions.
        text_similarity_threshold (float): Minimum cosine similarity value for two tasks to be considered similar.
        top_k_clusters (int): Number of clusters to return.

    Returns:
        list: List of dictionaries containing cluster label and corresponding task participants.
    """

    if not tasks:
        return []

    # Extract task names and descriptions
    task_names = [task['name'] for task in tasks]
    task_descriptions = [task['description'] for task in tasks]

    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')

    # Transform descriptions into TF-IDF vectors
    tfidf_vectors = vectorizer.fit_transform(task_descriptions)

    # Compute cosine similarity (without converting to dense array)
    sim_matrix = cosine_similarity(tfidf_vectors)

    # DBSCAN Clustering (eps is 1 - similarity threshold)
    eps = 1 - text_similarity_threshold
    min_samples = max(2, len(tasks) // 10)  # Dynamic min_samples
    db = DBSCAN(eps=eps, min_samples=min_samples, metric='precomputed')
    cluster_labels = db.fit_predict(sim_matrix)

    # Group tasks by clusters
    clusters = {}
    for idx, label in enumerate(cluster_labels):
        if label != -1:  # Ignore noise
            clusters.setdefault(label, []).append(task_names[idx])

    # Sort clusters by size (most common first)
    sorted_clusters = sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True)

    # Return top_k_clusters
    return [tasks for _, tasks in sorted_clusters[:top_k_clusters]]