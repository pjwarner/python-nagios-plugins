python-nagios-plugins
=====================

Nagios Plugins Written in Python

check_bandwidth.py
        This script allows you to pull the bandwidth settings from a router that
        stores the data in nvram.  More specifically this plugin works with the
        Buffalo Technology AirStation High Power N300 Gigabit Wireless Router
        & AP WZR-HP-G300NHv2 (Black) -- http://goo.gl/b0NoS

        See example_commands.cfg for how to set up the commands
        See check_bandwidth_example.cfg for how to configure the commands as 
            services of a host I always use a generic Global Host for these 
            types of services and just pack them all under the same host
            for ease of locating them in the Nagios Web Page
