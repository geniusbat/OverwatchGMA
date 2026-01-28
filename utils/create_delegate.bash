#Run from inside utils folder. It will create a folder "standalone" with all the code required to run a delegate client
standalone="./standalone"

if [ ! -d "$standalone" ]; then
    mkdir "$standalone"
else
    time=$(date +%T_%d-%m-%y)
    mv "$standalone" "$standalone-$time"
    sleep 0.1
    mkdir "$standalone"
fi

#Copy delegate folder
cp -r ../delegate/ "$standalone/delegate"
cp "$standalone/delegate/example_delegate_config.yml" "$standalone/delegate/delegate_config.yml"
#Get rid of unnecessary stuff
rm "$standalone/delegate/"*.log 
rm -r "$standalone/delegate/__pycache__"
rm -r "$standalone/delegate/venv/"
#Copy utils
if [ ! -d "$standalone/utils" ]; then
    mkdir "$standalone/utils"
fi
cp ../utils/*.py "$standalone/utils/"

#Copy commands
cp -r ../commands/ "$standalone/commands/"

#Copy usual_data.py
cp ../usual_data.py "$standalone/"

#Create venv
python3 -m venv "$standalone/.venv"
source $standalone"/.venv/bin/activate"
pip install -r "$standalone"/delegate/requirements.txt >> "$standalone"/pip.log

echo "Installed in $standalone"
echo "All done, configure $standalone/delegate/delegate_config.yml and then run the following to get started"
echo "source $standalone/.venv/bin/activate"
echo "Test everything goes well"
echo "python $standalone/delegate/main.py -c $standalone/delegate/delegate_config.yml --test"