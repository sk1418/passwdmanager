#!/bin/bash

# find current directory
script_path="${BASH_SOURCE[0]}"
if ([ -L "${script_path}" ]) then
	while ([ -L "${script_path}" ]) do script_path=$(readlink "${script_path}"); done
fi
pushd . > /dev/null
cd $(dirname ${script_path}) > /dev/null
script_path=$(pwd)
echo "current path:"$script_path
python passwdManager.py
