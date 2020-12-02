import json
from sys import path
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

    xticks = [f'Game {i+1}' for i in x]
    plt.xticks(x, labels=xticks)

    plt.legend()
    plt.title("Path Accuracy for each player arcoss all games")
    plt.ylabel("Accuracy percentage")
    plt.show()

    print(all_y)

    for xe, ye in list(zip(x, all_y)):
        plt.scatter([xe]*len(ye), ye)
    plt.xticks(x, labels=xticks)
    plt.title("Path Accuracy for each player arcoss all games")
    plt.ylabel("Accuracy percentage")
    plt.show()

    plt.scatter(x, average)
    plt.title("Average Path Accuracy")
    plt.ylabel("Accuracy percentage")
    plt.xticks(x, labels=xticks)
    plt.show()


def plot_predictions(games):
    predicitions = []
    actual = []

    x = range(len(games))

    for predict, act, _, _, _ in games:
        predicitions.append(predict)
        actual.append(act)

    plt.scatter(x, predicitions, color='red', label='Prediction')
    plt.scatter(x, actual, color='blue', label='Actual')

    p = np.array(predicitions)
    actual = np.array(actual)

    

    xtick = [f'Game {i+1}' for i in x]
    plt.xticks(x, labels=xtick)
    plt.title("Prediction vs. Actual across all games")
    plt.ylabel("ID of Player")
    plt.legend()
    plt.show()

    plt.scatter(x, np.abs(p - actual), color='green')
    plt.title("Difference between Actual and Prediction")
    plt.ylabel("Amount differed")
    plt.xticks(x, labels=xtick)
    plt.show()




metrics_file = "./presentation-10-3-metrics.json"
metrics_data = {}

with open(metrics_file, "r") as file:
    metrics_data = json.load(file)

games, accr = metrics_data

path_accuracy_plots(games)

plot_predictions(games)




