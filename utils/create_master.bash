#Run from inside utils folder. It will create a folder "master_standalone" with all the code required to run a master server
standalone="./master_standalone"

if [ ! -d "$standalone" ]; then
    mkdir "$standalone"
else
    time=$(date +%T_%d-%m-%y)
    mv "$standalone" "$standalone-$time"
    sleep 0.1
    mkdir "$standalone"
fi

#Copy web folder
cp -r ../web/ "$standalone/"
#Get rid of unnecessary stuff
rm "$standalone/web/"db.db
#Copy utils
if [ ! -d "$standalone/utils" ]; then
    mkdir "$standalone/utils"
fi
cp ../utils/*.py "$standalone/utils/"

#Copy commands
cp -r ../commands/ "$standalone/commands/"

#Copy usual_data.py and requirements
cp ../usual_data.py "$standalone/"
cp ../requirements_all.txt "$standalone/"

#Create venv
python3 -m venv "$standalone/.venv"
source $standalone"/.venv/bin/activate"
pip install -r "$standalone"/requirements_all.txt >> "$standalone"/pip.log

#Collect static
$standalone/.venv/bin/python $standalone/web/manage.py collectstatic
echo "Static collected, update nginx if needed"

echo "Installed in $standalone"
echo "All done, configure web settings and start running the web"
