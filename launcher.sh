#!/bin/sh
# /home/pi/Inselnetz/launcher.sh
# Der Script wird vom Benutzer 'pi' nach dem reboot automatisch gestartet.
# Welche Skripte werden während des Bootens gestartet, 
# kann man unter dem Benutzer 'pi' mit dem Befehl anschauen:
# sudo crontab -l

# Mit dem Befehl edirieren:
# sudo crontab -e

# "launcher.sh" ist dafür gemacht, um mehrere Python scripts zu starten


# Windlogging mit Aeocon 5000
# Navigate to directory Aeocon5000, execute datalogger.py (python script), go back home
cd /home/pi/Inselnetz/Aeocon5000/
sudo python logger.py
cd /
