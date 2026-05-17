from collections import Counter

def get_last7_pattern(last7_logs: list):
    if not last7_logs or len(last7_logs) < 2:
        return "Not enough data to detect pattern"

    keys = ["language", "motor", "social", "cognitive"]

    # STEP 1: split into two halves (trend detect korar jonno)
    mid = len(last7_logs) // 2
    first_half = last7_logs[:mid]
    second_half = last7_logs[mid:]

    def avg(logs, key):
        return sum([l.get(key, 0.5) for l in logs]) / len(logs)

    insights = []

    for key in keys:
        first_avg = avg(first_half, key)
        second_avg = avg(second_half, key)

        diff = second_avg - first_avg

        # STEP 2: trend detect
        if diff > 0.15:
            insights.append(f"{key} improving")
        elif diff < -0.15:
            insights.append(f"{key} decreasing")
        else:
            # STEP 3: level detect
            overall = avg(last7_logs, key)

            if overall < 0.4:
                insights.append(f"{key} consistently low")
            elif overall > 0.7:
                insights.append(f"{key} strong")
            else:
                insights.append(f"{key} stable")

    return ", ".join(insights)
