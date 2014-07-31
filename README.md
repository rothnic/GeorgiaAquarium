GeorgiaAquarium
===============

OpenMDAO model of the georgia aquarium energy system


# Install

## Install Compiler
* Download [MinGW](https://sourceforge.net/projects/mingw/files/latest/download)
* Install MinGW by running the downloader that is installed, then selecting the compilers (gcc,fortran,etc.), then applying changes. This downloads the various compiler types.
* Download [Visual Studio Express](http://go.microsoft.com/?linkid=7729279)
* Install Visual Studio Express

## Install OpenMDAO
* [Download OpenMDAO 0.9.7 Installer Script](http://openmdao.org/downloads/recent/) Note: There were significant speed improvements in 0.10.0, but changes to the drivers. Only 0.9.7 has been tested, but others may work.
* Open Console (cmd.exe)
* Copy script to the location you want openmdao installed. This could be within the anaconda install (c:\anaconda\go-openmdao-0.9.7.py) or in a personal workspace folder (c:\)
* Go to location of script
* Run: python install_script_name.py

## Install Python Editor
* [Pycharm (tested)](http://www.jetbrains.com/pycharm/download/) *or*
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
* pip install sphinx_pyreverse
* pip install ggplot
* pip install seaborn

### Install ffnet
* download [ffnet .exe installer](https://pypi.python.org/packages/2.7/f/ffnet/ffnet-0.7.1.win32-py2.7.exe#md5=b00b20e226993f78cd09f8e2d5e9d333) (avoids compiler issues)
* activate openmdao environment
* Run "easy_install ffnet_installer_name.exe"

* pip install sphinx_rtd_theme

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

# Setup Pycharm
* In Pycharm project settings under File, set the python interpreter to be the OpenMDAO environment's python.exe file. There will be a copy of python.exe in your main install, and one in the virtualenv that OpenMDAO creates. Just point Pycharm to the latter.
![](http://i.imgur.com/80VWPIb.png =400x)

* Create a run configuration for pytest. The setup requires you point to the GeorgiaAquarium project folder in two places.
![](http://i.imgur.com/oCXztSf.png =400x)

* Create a build configuration for the Sphinx documentation generation
![](http://i.imgur.com/dVDh9lI.png =400x)

# Fix Errors
* There is currently a bug in pickle in ipython that needs to be manually fixed. Open c:\Anaconda32\Lib\site-packages\IPython\utils\pickleshare.py, where you may need to modify the path based on your anaconda install location. Line 56 should read:
```
if not os.path.isdir(self.root):
```
Instead of:
```
if not self.root.isdir():
```

# Use the project
## With OpenMDAO GUI
OpenMDAO scans the opened project for any components/assemblies that it can load. If you have a well structured component or assembly, they will appear in the right side window. If they show up, then they can be dragged into the canvas, just like any built in tool.
* First, activate the OpenMDAO environment
* Run "openmdao gui"
* Open the GeorgiaAquarium project


## Run directly as Python Scripts
Each of the OpenMDAO components/assemblies is a typical python class. This means you can import the class, instantiate it, then execute it via OpenMDAO's placeholder methods they define. This is "execute()" for components, and "run()" for assemblies. Since assemblies typically wrap a component and drive, then "run()" method kicks off the execution of the driver on the component.
* Load the GeorgiaAquarium folder as a project in Pycharm
* Many of the OpenMDAO GeorgiaAquarium Components are developed to be directly executable from their implementation. In Pycharm, this means just opening the Solar.py file, for example, right clicking it, then selecting "Run". This will execute all code within the "if __name__=='__main__':" statement. If you import the class to use later in a different script, this code is not executed.


# Build the docs
* One thing to note is that the use of numba to speed up computation also clears out the documentation. When building documentation, the current workaround is to comment out the just in time decorators (@jit)
* Run the build configuration that was setup previously, the output is put into doc/_build
