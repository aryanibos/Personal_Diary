from datetime import datetime

today = datetime.now()
date_time = today.strftime("%Y-%m-%d-%H-%M-%S")

print("Today's date:", date_time)