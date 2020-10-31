kill -9 $(cat pid.out) 
python3 platformApp.py > log.out & 
echo "$!" > pid.out
cat pid.out
