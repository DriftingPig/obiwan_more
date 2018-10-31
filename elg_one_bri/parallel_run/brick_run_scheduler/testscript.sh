next_brick=none
function GetNextBrick {
next_brick=${ARRAY[$brick_index]}
brick_index=$brick_index+1
}

ARRAY=()
count=0
while IFS='' read -r line || [[ -n "$line" ]]; do
     ARRAY[$count]=$line
     count=$count+1
done < InsideBrick.txt

GetNextBrick

echo $next_brick

GetNextBrick

echo $next_brick
