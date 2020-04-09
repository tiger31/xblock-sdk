dir="custom-xblocks";

if [[ -d $dir ]]; then
	for entry in `ls $dir`; do
		file=$dir/$entry
		if [[ -L $file && -d $file || -d $file ]]; then
			setup="$file/setup.py";
			if [[ -f "$setup" ]]; then
				echo "Found xblock in $file, running setup script...";
				if [[ ! -x "$setup" ]]; then
					echo "Fixing permissions...";
					chmod u+x $setup;
				fi
				pip3 install -e $file #Dirrectory is a xblock name i believe
			else
				echo "No setup.py file found if $file" &1>2
			fi
		else 
			echo "$file is not a directory or symlink to directory" &1>2
		fi
	done
fi
