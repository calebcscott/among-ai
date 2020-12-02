import json
from sys import path
import sys
import matplotlib.pyplot as plt
import numpy as np


def path_accuracy_plots(games):
    path_accr_y = []
    
    for i in range(10):
        path_accr_y.append([])

    all_y = []

    average = []

    for _, _, corr, tot, paths in games:
        labeled = [0] * 10

        x, y = list(zip(*paths))
        y = list(y)

        for i in range(len(x)):
            if i+1 != x[i]:
                y.insert(i, 0)

        all_y.append(y)
        
        for i in paths:
            path_accr_y[i[0] - 1].append(i[1])
            labeled[i[0] - 1] = 1

        for i in range(len(labeled)):
            if not labeled[i]:
                path_accr_y[i].append(0)

        average.append(corr/tot)


    colors = ["black", "gray", "red", "orange", "saddlebrown", "yellow", "green", "lime", "cyan", "blue"]
    x = range(len(games))

    for idx, value in enumerate(path_accr_y):
        plt.scatter(x, value, c=colors[idx], label=f'{idx+1}')

    
    plt.xlabel("Number of Games")

    plt.legend()
    plt.title("Path Accuracy for each player arcoss all games")
    plt.ylabel("Accuracy percentage")
    plt.xlabel("Number of Games")
    plt.show()

    for xe, ye in list(zip(x, all_y)):
        plt.scatter([xe]*len(ye), ye)
    plt.xlabel("Number of Games")
    plt.title("Path Accuracy for each player arcoss all games")
    plt.ylabel("Accuracy percentage")
    plt.show()

    plt.scatter(x, average)
    plt.title("Average Path Accuracy")
    plt.ylabel("Accuracy percentage")
    plt.xlabel("Number of Games")
    plt.show()

    return np.array(average)


def plot_predictions(games):
    predicitions = []
    actual = []

    x = range(len(games))

    for predict, act, _, _, _ in games:
        predicitions.append(predict)
        actual.append(act)

    plt.scatter(x, predicitions, color='red', label='Prediction')
    plt.scatter(x, actual, color='blue', label='Actual')
    plt.xlabel("Number of Games")
    plt.title("Prediction vs. Actual across all games")
    plt.ylabel("ID of Player")
    plt.legend()
    plt.show()

    p = np.array(predicitions)
    actual = np.array(actual)

    plt.hist(actual)
    plt.title(f"Frequency of Actual Killer by Player in {len(games)} games")
    plt.xlabel("Player number")
    plt.ylabel("Number of times player was killer")
    plt.show()

    plt.hist(p)
    plt.title(f"Frequency of Predicted Killer by Player in {len(games)} games")
    plt.xlabel("Player number")
    plt.ylabel("Number of times player was killer")
    plt.show()
    

    plt.scatter(x, np.abs(p - actual), color='green')
    plt.title("Difference between Actual and Prediction")
    plt.ylabel("Amount differed")
    plt.xlabel("Number of Games")
    plt.show()



    return np.abs(p - actual)



if __name__ == "__main__":
    metrics_file = "./presentation-10-100-metrics.json"
    metrics_data = {}


    if len(sys.argv) > 1:
        metrics_file = sys.argv[1]

    

    with open(metrics_file, "r") as file:
        metrics_data = json.load(file)

    games, accr = metrics_data

    avg_accr = path_accuracy_plots(games)

    diff = plot_predictions(games)

    # m, b = np.polyfit(diff, avg_accr, 1)

    plt.scatter(diff, avg_accr, marker='o')
    # plt.plot(diff, m*diff + b, color="red")
    plt.show()

    print(f"Total Accuracy of AI for {len(games)} was {accr}")



