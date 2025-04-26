from datetime import datetime

now = datetime.now()

if now.hour == 23 and now.minute <= 45:
  print("🎯 It's between 23:00 and 23:45!")
else: 
  print("🕒 Current Time:", now.strftime("%Y-%m-%d %H:%M:%S"))
  