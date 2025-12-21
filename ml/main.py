from training.train import train_model
from evaluation.evaluate import evaluate_model

if __name__ == "__main__":
    data_path = "data/deap"

    model_path, _ = train_model(data_path)
    evaluate_model(model_path, data_path)
