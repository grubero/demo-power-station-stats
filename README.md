# demo-power-station-stats
Demonstration of using a public api to retrieve power station statistics through the OpenNEM project (https://opennem.org.au/about/) Some source code in this repo is specific to 11 Origin Energy power stations. Origin Energy is in no way affiliated with this repo.

Script can pull live data of energy generation (--genenergy), emissions (--emissions), and energy market trading value (--marketvalue) from the listed power generation sites (--list).

Installation instructions:
(venv) $ pip install -r requirements.txt

Usage instructions:
(venv) $python originenergyapi.py -h