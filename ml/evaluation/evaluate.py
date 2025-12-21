import torch
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    roc_auc_score,
    accuracy_score,
    balanced_accuracy_score,
    f1_score
)
from torch.utils.data import DataLoader, SubsetRandomSampler
from sklearn.model_selection import train_test_split

from preprocessing.deap_preprocess import DEAPDataset
from model.brain2vec import Brain2Vec


def evaluate_model(model_path, data_path):

    print("\n==============================")
    print("        EVALUATING MODEL")
    print("==============================")

    dataset = DEAPDataset(data_path)

    indices = list(range(len(dataset)))
    _, test_idx = train_test_split(indices, test_size=0.2, random_state=42)

    loader = DataLoader(dataset, batch_size=16, sampler=SubsetRandomSampler(test_idx))

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load model
    model = Brain2Vec().to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()

    labels, preds, probs = [], [], []

    with torch.no_grad():
        for X, y in loader:
            X, y = X.to(device), y.to(device)

            out = model(X)                 # (B,1)
            p = torch.sigmoid(out).squeeze()   # convert logits → probability

            pred = (p >= 0.5).long()

            labels.extend(y.cpu().numpy())
            preds.extend(pred.cpu().numpy())
            probs.extend(p.cpu().numpy())

    # Metrics
    print("\n CONFUSION MATRIX:\n", confusion_matrix(labels, preds))

    print("\n CLASSIFICATION REPORT:\n", classification_report(labels, preds))

    print("Accuracy:", accuracy_score(labels, preds))
    print("Balanced Accuracy:", balanced_accuracy_score(labels, preds))
    print("F1 Score:", f1_score(labels, preds))

    try:
        print("AUC:", roc_auc_score(labels, probs))
    except:
        print("AUC cannot be computed (maybe only one class predicted)")
