git add .
git commit -m "%*"
git push
ssh user@34.107.115.96 "cd /home/veliganchev/projects/todo-list-backend/ && git pull"
