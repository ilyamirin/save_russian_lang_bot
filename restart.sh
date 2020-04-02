if [[ $(ps -x | grep -E ^[0-9]+s.+savior.py | grep -E -o ^[0-9]+ | wc -l) = "2" ]]; then echo "works"; else nohup python3 savior.py ./voices/ ; fi &
