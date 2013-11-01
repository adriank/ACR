Asyncode Runtime
================

What is Asyncode Runtime?
-------------------------

Asyncode Runtime (ACR) is BLSL Runtime that allows you to develop nearly any internet application using a markup language (resembling HTML) and ObjectPath - a simple data manipulation language (resembling spreadsheet macros). It  can connect to databases and manipulate data, send e-mails or interact with filesystem. It handles all low level details of HTTP protocol and makes one simple and consistent XML API giving the developer an efficient way to create complex applications (e.g. business applications).

ACR runs on any WSGI-compilant server. The standalone version is available and is default for this distribution of ACR. It is tested under:

1. Apache with mod_wsgi - resource consuming,
2. Python WSGIRef module - also resource consuming,
3. Nginx with uWSGI - fast and stable.

What about Windows? It works, but it is not supported as of now.

Where is the documentation?
---------------------------

http://docs.asyncode.com/

Current state of the art
------------------------

ACR is a stable piece of software, working in production but is maintained and used by a limited number of users. It is well tested on our production server (Amazon AWS, Debian, Nginx/UWSGI, Python 2.7, MongoDB 2.2.0) and several applications. None of them is running under heavy load, but Apache Benchmark shows no serious problems when running with 100 or 1000 concurrent connections. It is due to uWSGI, but it shows that the code is not resource-demanding - it was implemented to be fast!

Security
--------

We place great emphasis on security and we always use the best practises we know. You can test ACR and send us bug reports. We'll fix bugs as fast as we can.

License notes
-------------

ACR is licensed under the GNU AGPL v3. Nearly all code is written by Adrian Kalbarczyk. There is some code taken from BSD/MIT licensed projects, but it is subject to change - you can find information about the orginal authors and the license in the respective files.

Please note that applications written in BLSL (the XML code) have their own licenses and they are not necessairly free. Take a look at the first lines of each file to determine the license. Also no license means that it is proprietary and you can not do anything but read the code, without asking the author for permission . If you find a file in this package without any license in the header, please contact us.

If you want to use the code in a way that goes beyond GNU AGPL v3, a commercial licence is required. 

Contributions
-------------

If you'd like to donate some code, write tutorials, documentation or spread the word, feel free to do so. The prefered way to send code the is via e-mail or github. Please keep in mind that in the future you may be asked for a permission to use your code in commercial products. This is one way to raise funds to develop high quality software. You can be sure that your code WILL NOT be used in commercial products without your permission.

Support
-------

There are two options for support. One is free community support (on http://docs.asyncode.com/ website). The other is business level support which ensures quick bug fix, answers to your questions etc. For the latter contact us by e-mail (support@asyncode.com). Support is provided only for Linux-based systems in English and Polish. Feel free to ask for other options.

Contact
-------

Website: http://www.asyncode.com/
E-mail: office@asyncode.com

[![githalytics.com alpha](https://cruel-carlota.pagodabox.com/a09a968bb861c456520d5aec2e9b83b2 "githalytics.com")](http://githalytics.com/adriank/ACR)
