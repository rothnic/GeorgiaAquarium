GeorgiaAquarium
===============

OpenMDAO model of the georgia aquarium energy system


## Install
* Download and install [Anaconda Python 32bit](http://09c8d0b2229f813c1b93-c95ac804525aac4b6dba79b00b39d1d3.r79.cf1.rackcdn.com/Anaconda-2.0.1-Windows-x86.exe). This should install at C:\Anaconda32.
* Open a terminal (cmd.exe), and typing "python" should provide feedback that it is installed
* If not, insure "C:\Anaconda32" is on your path without an ending "\"
* Install [OpenMDAO](http://openmdao.org/docs/getting-started/install.html). This requires you to download go-openmdao.py, then run it from the command line with:

```
python go-openmdao.py
or
python go-openmdao-VERSION.py
```

* OpenMDAO will create a python virtual environment, which is like a sandbox, but it has to be activated with:

```
cd C:\Anaconda32\openmdao-VERSION\Scripts
activate
# You should now see (openmdao-VERSION) at the command prompt
```

* Run the following command to test the install:

```
openmdao test
```

## Checkout the github project
* Use a GUI, or do the following:

```
cd C:\Users\USERNAME\.openmdao\gui\projects
git clone git://github.com/rothnic/GeorgiaAquarium.git
```

## Run the OpenMDAO GUI
* From the activated openmdao virtual environment type:

```
openmdao gui
```

* A web browser should appear, allowing you to open the GeorgiaAquarium project
