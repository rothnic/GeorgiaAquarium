GeorgiaAquarium
===============

OpenMDAO model of the georgia aquarium energy system


# Install

## Download Compiler
* [MinGW](https://sourceforge.net/projects/mingw/files/latest/download)
* [Visual Studio Express](http://go.microsoft.com/?linkid=7729279)

## Install OpenMDAO
* [Download OpenMDAO Installer Script](http://openmdao.org/downloads/recent/)
* Open Console (cmd.exe)
* Go to location of script
* Run: python install_script_name.py

## Download Python Editor
* [Pycharm (tested)](http://www.jetbrains.com/pycharm/download/)
* [liclipse](http://brainwy.github.io/liclipse/)

## Install Python
* [Anaconda 32-Bit (tested)](http://09c8d0b2229f813c1b93-c95ac804525aac4b6dba79b00b39d1d3.r79.cf1.rackcdn.com/Anaconda-2.0.1-Windows-x86.exe)

## Install SourceTree/Git
* [Download SourceTree](http://www.sourcetreeapp.com/)
* If Git isn't already installed, SourceTree will ask if you would like to install it, select yes

## Install extra packages
* navigate to install location
* activate environment: Scripts\activate
* pip install neurolab
* pip install ffnet

### Install pyopt
* (all the following still performed in activated environment)
* Download [pyopt](http://www.pyopt.org/_downloads/pyOpt-1.1.0.zip)
* Extract zip file
* Download [swig](http://prdownloads.sourceforge.net/swig/swigwin-3.0.2.zip)
* Extract zip to any folder location
* Add entire swig/swig extracted folder to Windows path
* Change directory to extracted PyOpt folder
* (windows install) Run "python setup.py install --compiler=mingw32"
* Run "plugin install --github pyopt_driver"

## Initialize Placeholder OpenMDAO project
* Activate OpenMDAO environment
* Run "openmdao gui"
* Create new project
* Name it anything, but GeorgiaAquarium is what was used
* Shut down OpenMDAO from menu
* Delete all files inside the GeorgiaAquarium folder in C:\users\username\.openmdao\gui\projects\GeorgiaAquarium

## Clone project repository to project folder
* Open SourceTree
* Choose clone new project (need to have Github account setup already)
* Choose the globe/web icon to navigate to your Github projects
* Select the GeorgiaAquarium project
* Select the previous step's project folder to clone the project to. This fills in the blank project info with the Github material.

# Use the project
## With OpenMDAO GUI
OpenMDAO scans the opened project for any components/assemblies that it can load. If you have a well structured component or assembly, they will appear in the right side window. If they show up, then they can be dragged into the canvas, just like any built in tool.
* First, activate the OpenMDAO environment
* Run "openmdao gui"
* Open the GeorgiaAquarium project

## Run directly as Python Scripts
Each of the OpenMDAO components/assemblies is a typical python class. This means you can import the class, instantiate it, then execute it via OpenMDAO's placeholder methods they define. This is "execute()" for components, and "run()" for assemblies. Since assemblies typically wrap a component and drive, then "run()" method kicks off the execution of the driver on the component.
* Load the GeorgiaAquarium folder as a project in Pycharm
* In Pycharm project settings under File, set the python interpreter to be the OpenMDAO environment's python.exe file. There will be a copy of python.exe in your main install, and one in the virtualenv that OpenMDAO creates. Just point Pycharm to the latter.
* Many of the OpenMDAO GeorgiaAquarium Components are developed to be directly executable from their implementation. In Pycharm, this means just opening the Solar.py file, for example, right clicking it, then selecting "Run". This will execute all code within the "if __name__=='__main__':" statement. If you import the class to use later in a different script, this code is not executed.
