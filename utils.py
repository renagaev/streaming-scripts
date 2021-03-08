def format_time(seconds):
    elapsed = int(seconds)
    minutes = str(elapsed // 60)
    seconds = elapsed % 60
    seconds = "0" + str(seconds) if seconds < 10 else seconds
    return f"{minutes}:{seconds}"
