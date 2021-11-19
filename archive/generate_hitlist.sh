DIRECTORY=$1
IN=$(cat $DIRECTORY/debug_*.txt | grep "index_start")
echo "" > tmpfile.txt
for p in $IN
do
  IFS=',' read -a splitp <<< "${p}"
  echo ${splitp[1]}
done

