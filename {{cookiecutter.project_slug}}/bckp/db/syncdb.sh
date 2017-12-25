#!/usr/bin/env bash

#title          :syncdb.sh
#description    :A GeoDjango Postgis Database Backup & Restore Script
#author         :Victor Miti<victormiti@umusebo.com>
#date           :20170224
#version        :0.1    
#usage          :syncdb.sh [option] (option is either *backup* OR *restore*)
#todo           :this script needs quite some work ...
#                - the need to terminate smartly and return appropriate msg on error
#                - provide a smarter way of providing DB_Name & DB_User instead of hardcoding
#                - the need for smart string substitution during the `restore` operation
#============================================================================


#############
# log to file as described at https://gist.github.com/benbuckman/6102425
LOGFILE=../../logs/syncdb.log
exec > >(tee -a $LOGFILE)
exec 2>&1
############

echo
echo "============================================================================"
echo "This is engineervix's syncdb v0.1 running on "$(uname -a)"."
echo "Script Start Time: "$(date)""
echo 

# To Do: Let these variables be provided as argument variables.
# For now, they have to be hardcoded before running the script
db_name="indicate_the_database_here"  # <--- edit this accordingly
db_user="indicate_the_username_here"  # <--- edit this accordingly

if [[ $1 = "backup" ]]; then
  # let's dump the database:
  SECONDS=0
  echo "I'm now backing up the Database for you ..."
  db_backup_file=db_bckp_$(date +%Y%m%d_%H%M%S).sql
  echo "The DB will be dumped to "$db_backup_file" ..."
  pg_dump -C -h localhost -U "$db_user" "$db_name" > $db_backup_file
  duration=$SECONDS
  echo "----------------------------------------------------"
  echo "RESULT: Database Backup Completed in $(($duration / 60)) min & $(($duration % 60)) sec"
  echo "----------------------------------------------------"
elif [[ $1 = "restore" ]]; then
  # let's restore the database:
  SECONDS=0
  echo "I'm now gonna restore the Database for you ..."

  psql <<-EOF
    DROP DATABASE "$db_name";
    \q
EOF

  # we'll list all files, filter by extension, select the latest SQL file
  # and use it as our database restoration file
  db_restore_file=$(ls -t1 | grep sql | head -n 1)

  # We'll do some string substitution in the database backup
  # This has to do with the issue of ROLES. If you don't wanna ignore them,
  # then we have to ensure we use the appropriate ROLE on whatever system

  # the_owner=$(grep -oP '(?<=topology\ OWNER\ TO).*' "$db_restore_file") | sed 's/;$//'
  # echo "the owner is $the_owner!"
  # sed -i "s/OWNER\ TO\ \$the_owner/OWNER\ TO\ $(whoami)/g" "$db_restore_file"
  # sed -i "s/Owner:\ \$the_owner/Owner:\ $(whoami)/g" "$db_restore_file"

  # the database is already in existence, so we need to comment out the line that
  # creates the database

  # sed -i 's/^CREATE\ DATABASE/--\ &/' "$db_restore_file"

  echo "The DB Restore File to be used is "$db_restore_file" ..."
  psql -h localhost -U "$db_user" "$db_name" < $db_restore_file
  duration=$SECONDS
  echo "-------------------------------------------------------------"
  echo "RESULT: Database Restoration Completed in $(($duration / 60)) min & $(($duration % 60)) sec"
  echo "-------------------------------------------------------------"
else
  echo "-------------------------------------------------------------------------"
  echo "RESULT: Nothing has been done."
  echo "You need to run the script with either the 'backup' or 'restore' option."
  echo "I can't do nothing without either of these options!"
  echo "-------------------------------------------------------------------------"
fi

echo 
echo "Thanks for using engineervix's syncdb v0.1"
echo "Script End Time: "$(date)""
echo "============================================================================"
