#!/usr/bin/env bash

#title          :initialize_db.sh
#description    :A GeoDjango Postgis Database Cleanup and Initialization Tool
#author         :Victor Miti<victormiti@umusebo.com>
#date           :20171210
#version        :0.1    
#usage          :initialize_db.sh [-n <DB_name>] [-u <DB_user>]
#============================================================================

echo
echo "============================================================================"
echo "This is engineervix's initialize_db v0.1 running on "$(uname -a)"."
start=`date +%s`
echo

# Step 0: Define your DB NAME and DB USER (get them as argument variables)

bold=$(tput bold)
normal=$(tput sgr0)
underline=$(tput smul)
nounderline=$(tput rmul)

# usage() { echo "Usage: $0 [-n <DB_name>] [-u <DB_user>]" 1>&2; exit 1; }

{% raw %}

usage() {
cat <<-EOF
  Usage: ${0##*/}  [-n ${bold}DB_Name${normal}] [-f ${bold}DB_Username${normal}]
  The ${bold}DB_Name${normal} and ${bold}DB_Username${normal} are required for the script to run.

    -n ${bold}DB_Name		${normal}the Name of the Postgres/PostGIS Database
    -u ${bold}DB_Username	${normal}the Postgres/PostGIS Database User

  ${underline}${bold}If you're using SQLite, just use 0 for both DB_Name & DB_Username${normal}${nounderline}
EOF
1>&2; exit 1;
}

while getopts ":n:u:" o; do
    case "${o}" in
        n)
            n=${OPTARG}
            ;;
        u)
            u=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${n}" ] || [ -z "${u}" ]; then
    usage
fi

db_name="${n}"
db_user="${u}"

{% endraw %}

# Step 1: Remove the all migrations files within your project
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

# Step 2: Drop Existing Database and Create a New One

{% if cookiecutter.database == "postgis" %}
psql <<-EOF
  DROP DATABASE "$db_name";
  CREATE DATABASE "$db_name" OWNER "$db_user";
  GRANT ALL PRIVILEGES ON DATABASE "$db_name" to "$db_user";
  \c "$db_name";
  CREATE EXTENSION postgis;
  CREATE EXTENSION postgis_topology;
  \q
EOF

{% elif cookiecutter.database == "postgres" %}
psql <<-EOF
  DROP DATABASE "$db_name";
  CREATE DATABASE "$db_name" OWNER "$db_user";
  GRANT ALL PRIVILEGES ON DATABASE "$db_name" to "$db_user";
  \q
EOF

{% elif cookiecutter.database == "sqlite" %}
# make a copy of existing SQLite Database, just in Case
db_file="../conf/db/db.sqlite3"
right_now=`date +%Y%m%d%H%M%S`
if [ -f "$db_file" ]
then
    mv -v "$db_file" ../conf/db/db_bckp_"$right_now".sqlite3
    # rm -v ../conf/db/db.sqlite3
else
    echo "$db_file not found."
fi

{% else %}
db_file="../conf/db/db.sqlite3"
right_now=`date +%Y%m%d%H%M%S`
if [ -f "$db_file" ]
then
    mv -v "$db_file" ../conf/db/db_bckp_"$right_now".sqlite3
    # rm -v ../conf/db/db.sqlite3
else
    echo "$db_file not found."
fi

{% endif %}


# Step 3: Create the initial migrations and generate the database schema
python manage.py makemigrations
python manage.py migrate

# Step 4: Create Superuser
python manage.py createsuperuser


echo 
echo "Thanks for using engineervix's initialize_db v0.1"
end=`date +%s`
runtime=$((end-start))
echo "Total Script Execution Time is "$runtime" seconds"
echo "============================================================================"
