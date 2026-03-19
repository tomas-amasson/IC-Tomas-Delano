#!/bin/bash

# Correct usage
if  [ $# -lt 2 ]; then
	echo 'Correct usege: ./add_database.sh <final_file.sh> <data_file.sh ...>'
	exit 1
fi

FINAL=$1

# Checks if final file already exist, if not creates it
touch "$FINAL"
echo "SET FOREIGN_KEY_CHECKS = 0;SET UNIQUE_CHECKS = 0;" >> "$FINAL"

# Finds number of messages of a specific file
find_size()
{
	local toffset=$(grep "^INSERT INTO" "$1" | grep -o "([0-9]\+" | wc -l)
	toffset=$(( toffset / 2 ))
	offset=$(( offset + toffset ))

	echo "File $1 contains $toffset messages."
}

remove_kc()
{
	touch temp
	sed '/FOREIGN_KEY_CHECKS/d' "$1" > temp
}

# Appends data to file
to_final()
{
	remove_kc "$1"
	if [ "$offset" -eq 0 ]; then
		cat temp >> "$FINAL"
	else
		echo -e "\n" >> "$FINAL"
		perl -ne "if (/^INSERT INTO/) { s/(\(\s*)(\d+)/\$1 . (\$2 + $offset)/ge; print }" temp  >> "$FINAL"
	fi
	rm temp
}


if [ -s "$FINAL" ]; then
	find_size "$FINAL"
fi

# Finds total ID offset
while [[ $# -ne 1 ]]; do
	to_final $2
	find_size $2
	
	shift
done

echo "SET FOREIGN_KEY_CHECKS = 1;SET UNIQUE_CHECKS = 1;" >> $FINAL
echo $offset

exit 0
