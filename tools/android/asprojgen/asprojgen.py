#!/usr/bin/python
"""asprojgen - Android Studio Project Generator

Usage:
    asprojgen --appname MyCinderApp --path /parent/path/of/app --domain org.mydomain.sub

    --appname   Name of application [Default: MyCinderApp]
    --path      Path to a directory that will contain MyCinderApp [Default: . ]
    --domain    Domain to use [Default: org.libcinder.samples]
    --help      This help message
"""
import sys
import getopt
import os
import shutil

def copy_tree(src, dst):
    for root, dirs, files in os.walk(src):
        files = [os.path.join(root, f) for f in files]
        for f in files:
            if os.path.basename(f).startswith("."):
                continue 
            srcFile = f
            dstFile = os.path.join(dst, os.path.relpath(f, src))
            if not os.path.exists(os.path.dirname(dstFile)):
                os.makedirs(os.path.dirname(dstFile))
            shutil.copy2(srcFile, dstFile)
    pass

# Line replace copy
def lineReplaceCopy(appName, appPackage, cinderRelPath, cinderRelPathApp, srcFile, dstFile):
    #print("Copying %s to %s" % (srcFile, dstFile))
    lines = open(srcFile, "r").readlines()
    outFile = open(dstFile, "w+")
    for l in lines:
        l = l.replace("$<<CINDER_APPNAME>>", appName)
        l = l.replace("$<<CINDER_RELPATH>>", cinderRelPath)
        l = l.replace("$<<CINDER_RELPATH_APP>>", cinderRelPathApp)
        l = l.replace("$<<APP_PACKAGE>>", appPackage)
        outFile.write(l)
    pass 

# projgen
def projgen( appName, appPath, appDomain ):
    appName = appName.strip()
    appPath = appPath.strip()
    appDomain = appDomain.strip()

    appPath = os.path.join(os.path.abspath(appPath), appName)
    appPackage = ("%s.%s" % (appDomain, appName.lower()))
    print( "App Name   : %s" % appName)
    print( "App Path   : %s" % appPath)
    print( "App Domain : %s" % appDomain)
    print( "App Package: %s" % appPackage)
    print( "" )

    cinderPath = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", ".."))
    templatePath = os.path.realpath(__file__)
    templatePath = os.path.join(os.path.dirname(templatePath), "template", "CinderApp")   

    asTemplatePath = os.path.join( templatePath, "androidstudio", "CinderApp")
    asProjPath = os.path.join(appPath, "androidstudio", appName)

    cinderRelPath = os.path.relpath(cinderPath, asProjPath)
    cinderRelPathApp = os.path.relpath(cinderPath, os.path.join(appPath, "androidstudio", appName, "app"))

    # Copy the CPP file
    srcCppFile = os.path.join(templatePath, "src", "CinderApp.cpp")
    dstCppFile = os.path.join(appPath, "src", ("%s.cpp" % appName))
    if not os.path.exists(os.path.dirname(dstCppFile)):
        os.makedirs(os.path.dirname(dstCppFile))
    lineReplaceCopy(appName, appPackage, cinderRelPath, cinderRelPathApp, srcCppFile, dstCppFile)

    # Copy the Android Studio project
    if not os.path.exists( asProjPath ):
        os.makedirs( asProjPath ) 
    # copy tree
    copy_tree( asTemplatePath, asProjPath )

    # Copy build.gradle
    srcFile = os.path.join( templatePath, "androidstudio", "CinderApp", "build.gradle")
    dstFile = os.path.join( asProjPath, "build.gradle")
    lineReplaceCopy(appName, appPackage, cinderRelPath, cinderRelPathApp, srcFile, dstFile)

    # Copy app/build.gradle
    srcFile = os.path.join( templatePath, "androidstudio", "CinderApp", "app", "build.gradle")
    dstFile = os.path.join( asProjPath, "app", "build.gradle")
    lineReplaceCopy(appName, appPackage, cinderRelPath, cinderRelPathApp, srcFile, dstFile)

    # Copy app/src/main/AndroidManifest.xml
    srcFile = os.path.join( templatePath, "androidstudio", "CinderApp", "app", "src", "main", "AndroidManifest.xml")
    dstFile = os.path.join( asProjPath, "app", "src", "main", "AndroidManifest.xml")
    lineReplaceCopy(appName, appPackage, cinderRelPath, cinderRelPathApp, srcFile, dstFile)

    # Copy app/src/main/res/values/strings.xml
    srcFile = os.path.join( templatePath, "androidstudio", "CinderApp", "app", "src", "main", "res", "values", "strings.xml")
    dstFile = os.path.join( asProjPath, "app", "src", "main", "res", "values", "strings.xml")
    lineReplaceCopy(appName, appPackage, cinderRelPath, cinderRelPathApp, srcFile, dstFile)

    # Create app/src/main/java/<appPackage>/<appName>Activity.java
    dstFile = os.path.join( asProjPath, "app", "src", "main", "java", appPackage.replace(".", "/"), "%sActivity.java" % appName)
    dirPath = os.path.dirname(dstFile)
    if not os.path.exists(dirPath):        
        os.makedirs(dirPath)
    outFile = open(dstFile, "w+")
    outFile.write("package %s;\n" % appPackage)
    outFile.write("\n")
    outFile.write("import android.app.NativeActivity;\n")
    outFile.write("\n")
    outFile.write("public class %sActivity extends NativeActivity {\n" % appName)
    outFile.write("    static final String TAG = \"%sActivity\";\n" % appName)
    outFile.write("}\n")
    
    print("Project generated at: %s" % appPath)
    print("")
    
    pass

# main
def main():
    appName   = "MyCinderApp"
    appPath   = "."
    appDomain = "org.libcinder.samples"
    
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help", "appname=", "path=", "domain="])          
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
        elif o in ("--appname"):
            appName = a
        elif o in ("--path"):
            appPath = a
        elif o in ("--domain"):
            appDomain = a
    # process arguments
    for arg in args:
        pass 
    # projgen
    if (appName is not None):
        projgen( appName, appPath, appDomain )
        pass
    pass

if __name__ == "__main__":
    main()

