#!/usr/bin/env python

import os,sys
import zipfile
import optparse

images = ("jpg","jpeg","png","tiff","gif","bmp")
incompatible = []

def testFile(file_,folder):
	return os.path.isfile(os.path.join(folder,file_)) and file_.split('.')[-1].lower() in images

def serachFile(directory,dictionary):
	files = os.listdir(directory)
	for thing in files:
		if os.path.isdir(os.path.join(directory,thing)):
			 serachFile(os.path.join(os.path.abspath(directory),thing),dictionary)
		else:
			if testFile(thing,directory):
				dictionary[thing] = os.path.expandvars(os.path.realpath(directory))
			else:	
				if thing not in incompatible: incompatible.append(thing)
	return dictionary	

def printFile(what):
	sys.stdout.write(what)
	sys.stdout.flush()

def shorte(word):
	if len(word) > 7:
		word = "_" + word[-7:]
	return word

def zipArchive(name,dictionary,path_):
	i = 1 
	f = zipfile.ZipFile(path_ + name + '.cbr','w')
	for dic in dictionary:
		printFile("\rAdding %s ( %s of %s) to %s" % (shorte(dic),'{0:0>3}'.format(i),len(dictionary),name))
		f.write(dictionary[dic]+"/"+dic,name + "/" + dic)
		i += 1
	print ""
	f.close()

def testPath(path_):
	if path_ is None:
		path_ = '.'
	return str(path_) + '/'

def comicMode():
	print "Entering comic mode..."
	what = True
	volume = 0
	print "Current Volume is " + str(volume) + " what is your order?"
	while what:
		order = raw_input('Next[N],Previos[P],Status[S],Reset[R],End[E]: ')
		if order == "N" or order == "n":
			volume += 1
			os.system("open -a DrawnStrips\ Reader ./*%s.cbr" % (volume))
		elif order == "P" or order == "p":
			volume -= 1
			os.system("open -a DrawnStrips\ Reader ./*%s.cbr" % (volume))
		elif order == "S" or order == "s":
			print "Your current volume is " + str(volume)
			OS.SYSTEM("ls -lh")
		elif order == "E" or order == "e":
			what = False
		elif order == "R" or order == "r":
			print "Reseting from %s to 0" % (volume)
			volume = 0
		else:
			print "Wrong input.."

if len(sys.argv[1:]) > 0:
	if sys.argv[1] == "mode":
		comicMode()
	else:
		parser = optparse.OptionParser()
		parser.add_option('-d','--directory',dest='path',help='where you want to save it')
		(options,args) = parser.parse_args()
		if sys.argv[1] in ('-d','-h'):
			folders = sys.argv[3:]
		else:
			folders = sys.argv[1:]
		for folder in folders:
			fileDic = {}
			fileDic = serachFile(folder,fileDic)
			zipArchive(os.path.basename(folder),fileDic,testPath(options.path))
		if len(incompatible) > 0:
			print "Not compatible files: "
			for i in incompatible: print i
else:
	print "No input\nmode | argv1 argv2 argvN\nsupported fromats: jpg,png,giff,tiff,jpeg"

