from datetime import timedelta

def calculate_streaks(completed_dates):
    """
    completed_dates: sorted list of date objects (descending)
    returns: (current_streak, best_streak)
    """

    if not completed_dates:
        return 0, 0

    best_streak = 0
    current_streak = 0
    streak = 1

    for i in range(len(completed_dates) - 1):
        if completed_dates[i] - completed_dates[i + 1] == timedelta(days=1):
            streak += 1
        else:
            best_streak = max(best_streak, streak)
            streak = 1

    best_streak = max(best_streak, streak)

    # current streak = only if last completion is today or yesterday
    today = completed_dates[0]
    current_streak = 1

    for i in range(len(completed_dates) - 1):
        if completed_dates[i] - completed_dates[i + 1] == timedelta(days=1):
            current_streak += 1
        else:
            break

    return current_streak, best_streak
