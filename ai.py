def categorize_task(task):

    task = task.lower()

    if "python" in task:
        return "Learning"

    elif "sql" in task:
        return "Learning"

    elif "interview" in task:
        return "Career"

    elif "resume" in task:
        return "Career"

    elif "project" in task:
        return "Development"

    elif "app" in task:
        return "Development"

    else:
        return "Personal"