# PowerAI Vision Apps

This repository is home to a number of PowerAI Vision applications. Each of them wrap a front end around a different custom model deployed via [PowerAI Vision](https://developer.ibm.com/linuxonpower/deep-learning-powerai/vision/).

This repository is public as I believe that it shows a simple, archetypal way to create computer vision based web applications. The default applications point to inference APIs behind an IBM firewall- if you wish to supply your own please refer to the 'To Get Started' section.

The folder designated `opencv` runs applications purely within the OpenCV video window. The application can be stopped using `Q`, and the screen cleared and reset using `C`. 

The `flask` folder contains applications which have been wrapped within a simple Flask web application. Once you have your Python environment setup you can run them using the `python server.py` command. 

## To Get Started...

`git clone` this repository, and then follow the instructions in each of individual folders to setup the Python environment, and start the server. 

If you are not an IBMer you will have to supply your own inference API. This can easily be swapped out within `inferencehelper.py` by changing the `POWERAI_BASEURL` constant on line 19.  

# Need to add...
- Test to make sure you can add a different URL to it so it's of use to the public. 
- Javascript framework examples- using a purely client side driven approach. 
- Better documentation of the way the apps work- this can be inconjunction with a blog post. 
