import os
import gntp.notifier
import sys
import easygui as eg
import urllib

def download(url):
    """Copy the contents of a file from a given URL
    to a local file.
    """
    home = os.getenv("HOME")
    folder = home + "/Library/Application Support/NH_CremaModule/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    if not os.path.exists(folder + url.split('/')[-1]):
        webFile = urllib.urlopen(url)
        localFile = open(folder + url.split('/')[-1], 'w')
        localFile.write(webFile.read())
        webFile.close()
        localFile.close()
    return (folder + url.split('/')[-1])

if __name__ == '__main__':
    direc = ""
    name = eg.enterbox(msg='Enter Module Name.', title='New CremaMobile Module', default='', strip=True, 	image=None, root=None)
    new = 0
    existed = 0
    message = ""
    image = ""

    ### image runterladen
    try:
       image = open(download("http://niklas-heer.de/pics/new_file.png")).read()
    except IOError:
        print 'Filename not found.'

    for f in sys.argv[1:]:
        direc = f

    folder = direc + "/" + name
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Create "manifest.json.php"
    try:
        fd = os.open(folder + "/manifest.json.php", os.O_WRONLY | os.O_CREAT | os.O_EXCL)
        f = os.fdopen(fd, "w")
        f.write('<?php\n    return array(\n        "dependencies" => array(\n            "libs" => array("cremabase/cremaMobile"),\n            \n            "project" => array(),\n            \n            "controller" => array(),\n            \n            "features" => array()\n        ),\n        \n        "js" => array(\n            "files" => array(\n                "View.coffee",\n                "ViewController.coffee"\n            )\n        ),\n        \n        "php" => array(\n            "files" => array()\n        ),\n        \n        "less" => array(\n            "files" => array()\n        )\n    );\n?>')
        f.close()
        new += 1
    except Exception, e:
        existed += 1

    # Create "View.coffee"
    try:
        fd = os.open(folder + "/View.coffee", os.O_WRONLY | os.O_CREAT | os.O_EXCL)
        f = os.fdopen(fd, "w")
        f.write('class crema.views.' + name + ' extends crema.MobileView\n    constructor: (@controller, options) ->\n        super @controller, options)\n')
        f.close()
        new += 1
    except Exception, e:
        existed += 1

    # Create "ViewController.coffee"
    try:
        fd = os.open(folder + "/ViewController.coffee", os.O_WRONLY | os.O_CREAT | os.O_EXCL)
        f = os.fdopen(fd, "w")
        f.write('class crema.viewControllers.' + name + ' extends crema.ViewController\n    constructor: (options = {}) ->\n        super options')
        f.close()
        new += 1
    except Exception, e:
        existed += 1

    message = str(new) + ' files created - ' + str(existed) + ' files existed'

    growl = gntp.notifier.GrowlNotifier(
        applicationName = "My Application Name",
        notifications = ["New Updates","New Messages"],
        defaultNotifications = ["New Messages"],
    )
    growl.register()
    
    growl.notify(
        noteType = "New Messages",
        title = '"' + name + '" Modul created!',
        description = message,
    	icon = image,
        sticky = False,
        priority = 1,
    )