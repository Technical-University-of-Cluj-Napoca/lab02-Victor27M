from datetime import datetime

def smart_log(*args, **kwargs) -> None:
    # options (defaults chosen to match the screenshot)
    level    = kwargs.get("level", "info").lower()
    colored  = kwargs.get("color", kwargs.get("colored", True))
    timestamp = kwargs.get("timestamp", True)
    save_to   = kwargs.get("save_to", None)

    # ANSI colors
    GREY  = "\033[90m"
    BLUE  = "\033[94m"
    YELL  = "\033[93m"
    RED   = "\033[91m"
    RESET = "\033[0m"

    level_color = {
        "info": BLUE,
        "debug": GREY,
        "warning": YELL,
        "error": RED,
    }.get(level, BLUE)

    # timestamp (grey)
    time_part = ""
    if timestamp:
        t = datetime.now().strftime("%H:%M:%S")
        time_part = f"{t} "

    # message
    message = " ".join(str(x) for x in args)
    core = f"[{level.upper()}] {message}"

    if colored:
        # grey timestamp + colored level+message
        line_print = f"{GREY}{time_part}{RESET}{level_color}{core}{RESET}"
        line_file  = f"{time_part}{core}"  # plain for file
    else:
        line_print = f"{time_part}{core}"
        line_file  = line_print

    print(line_print)

    if save_to:
        with open(save_to, "a", encoding="utf-8") as f:
            f.write(line_file + "\n")


if __name__ == "__main__":
    smart_log("System started successfully.", level="info")
    smart_log("User", "Alice", "logged in", level="debug", timestamp=True)
    smart_log("Low disk space detected!", level="warning", save_to="system.log")
    smart_log("Model", "training", "failed!", level="error", color=True, save_to="errors.log")
    smart_log("Process end", level="info", color=False, save_to="errors.log")
