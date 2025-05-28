import numpy as np
import pandas as pd

def cosine_similarity(matrix):
    """Compute pairwise cosine similarity while handling missing values."""
    n_samples = matrix.shape[0]
    similarity = np.zeros((n_samples, n_samples))

    for i in range(n_samples):
        for j in range(n_samples):
            vec_a = matrix[i, :]
            vec_b = matrix[j, :]
            valid_idx = ~np.logical_or(np.isnan(vec_a), np.isnan(vec_b))

            if not np.any(valid_idx):
                similarity[i, j] = 1.0
            else:
                a = vec_a[valid_idx]
                b = vec_b[valid_idx]
                denom = np.sqrt(np.sum(a ** 2) * np.sum(b ** 2))
                similarity[i, j] = 1.0 if denom == 0 else np.dot(a, b) / denom
    return similarity

def frmf_impute(
    data,
    rank=3,
    learning_rate=0.0005,
    max_steps=5000,
    convergence_threshold=0.05,
    lambda_a=0.005,
    lambda_s=0.005,
    neighbor_matrix=None,
    neighbor_threshold=0.9,
    cross_regularization_coeff=0,
    normalization="max_norm"
):
    """
    Fused Regularization Matrix Factorization (FRMF) for missing value imputation.
    """
    X = data.copy().values.astype(float)
    nan_mask = np.isnan(X)
    original_data = X.copy()

    if neighbor_matrix is not None:
        print("External information incorporated.")
        neighbor_similarity = cosine_similarity(neighbor_matrix)
    else:
        print("No external information incorporated.")
        neighbor_similarity = None

    if normalization == "max_norm":
        col_max = np.nanmax(X, axis=0)
        X = X / col_max
    elif normalization == "std_score":
        col_mean = np.nanmean(X, axis=0)
        col_std = np.nanstd(X, axis=0)
        X = (X - col_mean) / col_std

    sample_count, feature_count = X.shape
    A = np.random.rand(sample_count, rank)
    S = np.random.rand(rank, feature_count)
    indicator = (~nan_mask).astype(float)
    X[np.isnan(X)] = 0

    prev_loss = float("inf")

    for step in range(max_steps):
        reconstruction = A @ S
        error = (reconstruction - X) * indicator

        # Update A
        for i in range(sample_count):
            gradient_a = error[i, :] @ S.T + lambda_a * A[i, :]
            A[i, :] -= learning_rate * gradient_a

        # Update S
        for j in range(feature_count):
            gradient_s = A.T @ error[:, j] + lambda_s * S[:, j]
            S[:, j] -= learning_rate * gradient_s

        loss = 0.5 * np.sum((A @ S - X) * indicator) ** 2
        loss += (lambda_a / 2) * np.linalg.norm(A, "fro") ** 2
        loss += (lambda_s / 2) * np.linalg.norm(S, "fro") ** 2

        if neighbor_similarity is not None:
            for i in range(sample_count):
                neighbors = np.where(neighbor_similarity[i, :] >= neighbor_threshold)[0]
                neighbors = neighbors[neighbors != i]
                if len(neighbors) > 0:
                    diff = A[i] - A[neighbors]
                    A[i] -= learning_rate * cross_regularization_coeff * np.sum(diff, axis=0)
                    loss += 0.5 * cross_regularization_coeff * np.sum(np.linalg.norm(diff, axis=1))

        if abs(prev_loss - loss) < convergence_threshold:
            print("Converged at step", step)
            break
        if loss > 1e6:
            print("Diverged at step", step)
            break

        prev_loss = loss

    reconstructed = A @ S

    # Reverse normalization
    if normalization == "max_norm":
        reconstructed *= col_max
    elif normalization == "std_score":
        reconstructed = reconstructed * col_std + col_mean

    # Fill in missing values
    imputed = original_data.copy()
    imputed[nan_mask] = reconstructed[nan_mask]

    return pd.DataFrame(imputed, index=data.index, columns=data.columns)

def impute_missing_values(df):
    """Impute missing values using minimum value per column."""
    min_values = df.min()
    return df.fillna(min_values)

if __name__ == "__main__":
    df = pd.read_csv('read_counts.csv', sep='\t')

    from quality_control import filter_low_counts
    df_filtered = filter_low_counts(df)

    df_imputed = impute_missing_values(df_filtered)  # basic version

    # Optionally use FRMF imputation
    # df_imputed = frmf_impute(df_filtered)
