# import wandb


# # start a new wandb run to track this script
# wandb.init(
#     # set the wandb project where this run will be logged
#     project="Thesis",

#     # track hyperparameters and run metadata
#     config={
#     "learning_rate": 0.02,
#     "architecture": "CNN",
#     "dataset": "CIFAR-100",
#     "epochs": 10,
#     }
# )


# wandb.log({"acc": acc, "loss": loss})

import matplotlib.pyplot as plt
import numpy as np

X_10_5 = [200, 130, 100, 50, 25, 10]
y_10_5 = [4.6, 7.8, 8.6, 8.6, 8.5, 6.8]
std_10_5 = 0.6

X_50_5 = [3000, 1000, 500, 300, 200, 130, 50, 25, 10]
y_50_5 = [15.0, 28.8, 33.0, 32.7, 35.2, 35.1, 30, 28.5, 22.5]
std_50_5 = 1.8

X_200_5 = [50, 100, 200, 200, 300, 500, 1000, 2000, 4000, 6000]
y_200_5 = [41.2, 46.5, 46.2, 46.4, 47.1, 46.0, 45.9, 46.8, 43.8, 37.1]
std_200_5 = 1.8

X_500_5 = [12000, 6000, 3000, 1000, 500, 300, 100, 25]
y_500_5 = [50.1, 51.6, 52.6, 49.5, 51.2, 49.3, 49.3, 36.8]
std_500_5 = 1.8


marker = ".-"

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(21, 7))
ax1.plot(X_10_5, y_10_5, marker, label="10 steps")
ax1.fill_between(X_10_5, np.array(y_10_5) - std_10_5 * 1.98, np.array(y_10_5) + std_10_5 * 1.98, alpha=0.2)

ax1.plot(X_50_5, y_50_5, marker, label="50 steps")
ax1.fill_between(X_50_5, np.array(y_50_5) - std_50_5 * 1.98, np.array(y_50_5) + std_50_5 * 1.98, alpha=0.2)

ax1.plot(X_200_5, y_200_5, marker, label="200 steps")
ax1.fill_between(X_200_5, np.array(y_200_5) - std_200_5 * 1.98, np.array(y_200_5) + std_200_5 * 1.98, alpha=0.2)

ax1.plot(X_500_5, y_500_5, marker, label="500 steps")
ax1.fill_between(X_500_5, np.array(y_500_5) - std_500_5 * 1.98, np.array(y_500_5) + std_500_5 * 1.98, alpha=0.2)

ax1.set_title("Effect of different number of steps with different \n C values on the average score (sims=5)")
# ax1.set_title("Average Score vs C value (Exploration Rate) \n for different number of steps and sims=5")
# ax1.set_
ax1.set_xscale("log")
ax1.set_xlabel("C value (Exploration Rate)")
ax1.set_ylabel("Average Score")
ax1.legend()

sims_step10_c1 = [200, 100, 50, 25, 15, 8, 5, 3]
time_step10_c1 = [345, 172, 91, 47.6, 30.4, 17.54, 13.8, 8.48]
score_step10_c1 = [12.8, 11.4, 10.3, 8.4, 7.8, 7.5, 6.1, 4.8]
std_step10_c1 = 0.6

steps_sims5_c1 = [10, 50, 200, 500]
score_sims5_c1 = [8.6, 35.2, 47.1, 51.2]
time_sims5_c1 = [12.6, 49.9, 193.2, 492.3]

sims__steps200_c300 = [20, 10, 4, 3, 1]
score_steps200_c300 = [47.5, 46.7, 44.4, 44.0, 42]
time_steps200_c300 = [693.0, 353.0, 170.3, 142.0, 71.9]

marker2 = "-"
ax2.plot(time_step10_c1, score_step10_c1, marker2, label="Sims with steps=10, c=1")
ax2.plot(time_sims5_c1, score_sims5_c1, marker2, label="Steps with sims=5, c=optimal")
ax2.plot(time_steps200_c300, score_steps200_c300, marker2, label="Sims with steps=200, c=300")

number_base = 130
number_scale = 10
for xp, yp, m in zip(time_step10_c1, score_step10_c1, sims_step10_c1):
    ax2.scatter(
        xp,
        yp,
        marker=f"${m}$",
        s=number_base * (np.floor(np.emath.logn(number_scale, m)) + 1),
        color="black",
        zorder=10,
    )

for xp, yp, m in zip(time_sims5_c1, score_sims5_c1, steps_sims5_c1):
    ax2.scatter(
        xp,
        yp,
        marker=f"${m}$",
        s=number_base * (np.floor(np.emath.logn(number_scale, m)) + 1),
        color="black",
        zorder=10,
    )

for xp, yp, m in zip(time_steps200_c300, score_steps200_c300, sims__steps200_c300):
    ax2.scatter(
        xp,
        yp,
        marker=f"${m}$",
        s=number_base * (np.floor(np.emath.logn(number_scale, m)) + 1),
        color="black",
        zorder=10,
    )
ax2.set_xscale("log")
ax2.set_yscale("log")
ax2.set_title(
    "Effect of different number of simulations compared to different \n number of steps on the average score and thinking time"
)
# ax2.set_title("Score vs Think time \n for different steps and sims settings")
ax2.set_xlabel("Think time per move (ms)")
ax2.set_ylabel("Average Score")
ax2.legend()



scores_no_sims = [-30.2,-13.7,-11.5,-8.1, -3.9, 1.3, 4.7, 6.0, 10.8, 16.3, 17.7, 19.8, 19.1, 20.1, 14.5, 16.8, 18.2]
times_no_sims = [0, 4.2, 8.4, 12.6, 16.8, 21, 25.2, 29.4, 33.6, 37.8, 42, 46.2, 50.4, 54.6, 58.8, 63, 67.2]
std_no_sims = 1.8

scores_sims = [-40.5, 22.6, 18.9, 17.9, 14.7, 16.1, 14.9, 17.1, 15.9, 18.1, 18.5, 16.8]
times_sims = [0, 1.0, 2.9, 4.8, 9.6, 14.4, 19.2, 24.0, 28.8, 33.6, 38.4, 43.2]
std_sims = 1.8

scores_boosted = [21.0, 17.5, 17.2, 16.6, 17.4, 15.3]
times_boosted = [0, 4.1, 8.2, 12.3, 16.4, 20.5]
std_boosted = 1.8

ax3.plot(times_no_sims, scores_no_sims, marker, label="RL without sims")
ax3.fill_between(times_no_sims, np.array(scores_no_sims) - std_no_sims * 1.98, np.array(scores_no_sims) + std_no_sims * 1.98, alpha=0.2)
ax3.plot(times_sims, scores_sims, marker, label="RL with sims")
ax3.fill_between(times_sims, np.array(scores_sims) - std_sims * 1.98, np.array(scores_sims) + std_sims * 1.98, alpha=0.2)
ax3.plot(times_boosted, scores_boosted, marker, label="RL boosted")
ax3.fill_between(times_boosted, np.array(scores_boosted) - std_boosted * 1.98, np.array(scores_boosted) + std_boosted * 1.98, alpha=0.2)
ax3.set_title("Progression of the average score while training")
ax3.set_ylabel("Average Score")
ax3.set_xlabel("Training time (hours)")
ax3.legend()
plt.show()
