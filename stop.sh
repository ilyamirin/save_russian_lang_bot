kill -9 $(ps -x | grep -E ^[0-9]+s.+savior.py | grep -E -o ^[0-9]+ | head -1)
