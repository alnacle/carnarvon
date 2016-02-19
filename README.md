# carnarvon

Carnarvon analyses how old the software system is on a per-line basis and extracts figures and indexes that make it
possible to identify how `old' the software is, how much it has been maintained and how much effort it may suppose to
maintain it in the future.

A lot of software, mostly open source software, is developed using version control tools from which it is possible to
extract even when a single line of code was edited for the last time. To collect all this kind of data and analyze it
statistically could show information in terms of software aging and indicators of maintainability could be obtained from
different perspectives, systems area and development area, for example.

Carnarvon runs on any platform with python 2.3+ interpreter installed. Current supported versioning systems are CVS and
Subversion.

## Installation

    $ python setup.py install

## Usage

carnarvon needs a config file in order to run. You can generate this config file in two ways:

    $ carnarvon -a my.conf

will generate a basic template. Edit it with your proper values.

    $ carnarvon -w my.conf

will execute a wizard in order to generate the config file step by step.

Once you have a proper config file, you will be able to run carnarvon:

    $ carnarvon my.conf

Note that carnarvon accepts several flags. Try running carnarvon without arguments for more help.

After carnarvon finishes the analysis of the given project, run the other tools in order to get graphs and a nice website:

    $ carnarvon2web my.conf

