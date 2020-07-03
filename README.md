Have you ever wanted a simple hack to monitor a file for a specific value
then if it finds it, set it to something else?

For example, let's say you have the same scenario I did with an annoying
puppet run over which you have no control, that keeps furning off ipv4
packet forwarding between machine interfaces.

Look no further.

The script take 3 arguments, the name of the file to watch, the trigger value
and the desired value. e,g,

filechange_trigger.py /proc/sys/net/ipv4/ip_forward 0 1 

This will write 1 to /proc/sys/net/ipv4/ip_forward, then use the kernel
"inotifywait" function to do a blocking read consuming virtually no machine
resource until the file is modified, at which point the script will leap
to the rescue and blat 1 into that file! Awesome or what?

<jfk@linux.com> 20200703 

2020 - the year of Covid 19 - tomorrow the pubs open again, yay :D
