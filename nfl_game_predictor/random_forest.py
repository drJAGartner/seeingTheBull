############# ############# #############
# stat_plotter v1.0
# by JAG3
#
# Basic stats plotting
############# ############# #############
import argparse
import nflgame as nfl

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def clockToFractionalMinutes(str_clock):
    return float(str_clock.split(":")[0]) + float(str_clock.split(":")[1])/60.

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("year", help="Year for the game", type=int, default=2014)
    args = parser.parse_args()

    score_differential = []
    turnover_margin = []
    first_downs = []
    total_yds = []
    rush_yds = []
    pass_yds = []
    time = []

    games = nfl.games(args.year)
    for g in games:
        sd = g.score_away - g.score_home
        score_differential.append(sd)
        score_differential.append(-1*sd)

        sta_a = g.stats_away
        sta_h = g.stats_home
        to = sta_a.turnovers - sta_h.turnovers
        turnover_margin.append(to)
        turnover_margin.append(-1*to)
        first_downs.append(sta_a.first_downs)
        first_downs.append(sta_h.first_downs)
        total_yds.append(sta_a.total_yds)
        total_yds.append(sta_h.total_yds)
        rush_yds.append(sta_a.rushing_yds)
        rush_yds.append(sta_h.rushing_yds)
        pass_yds.append(sta_a.passing_yds)
        pass_yds.append(sta_h.passing_yds)
        time.append(clockToFractionalMinutes(sta_a.pos_time.clock))
        time.append(clockToFractionalMinutes(sta_h.pos_time.clock))

    f, ([ax1, ax2], [ax3, ax4], [ax5, ax6]) = plt.subplots(3, 2)
    ax1.scatter(score_differential, total_yds)
    ax1.set_title("Total Yards")

    ax2.scatter(score_differential, turnover_margin)
    ax2.set_title("Net Turnovers")

    ax3.scatter(score_differential, first_downs)
    ax3.set_title("First Downs")

    ax4.scatter(score_differential, rush_yds)
    ax4.set_title("Rush Yards")

    ax5.scatter(score_differential, pass_yds)
    ax5.set_title("Pass Yards")

    ax6.scatter(score_differential, time)
    ax6.set_title("Time of Possession")

    f.savefig("figures/2014Stats.pdf")