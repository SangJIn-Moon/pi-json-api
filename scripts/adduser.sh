#!/usr/bin/env bash

# create new user
sudo adduser --disabled-password --gecos "" $username
sudo usermod -a -G $groups $username

# set password
echo -e "$password\n$password" | sudo passwd $username > /dev/null 2>&1
echo $?
