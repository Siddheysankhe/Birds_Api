import sys
from pydub import AudioSegment
import subprocess
import re
import csv
import os
import myaudioAnalysis
import operator


#pyaduio_folder = os.getcwd()

def check_duration(fname):
	op= 0.0
	process = subprocess.Popen(['ffmpeg',  '-i', fname], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	stdout, stderr = process.communicate()
	matches = re.search(r"Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", stdout, re.DOTALL).groupdict()
	#print matches['hours']
	#print matches['minutes']
	#print matches['seconds']
	print matches
	op = float(matches['hours'])*3600+float(matches['minutes'])*60+float(matches['seconds'])
	return op

def processing(folder):
	#os.chdir(folder)
	result_folders = []
	files = os.listdir(os.getcwd())
	for f in files:
		if('.wav' in f.lower()):
			#print int(check_duration(f))
			fname,file_format = f.split(".")
			#print fname 
			duration = int(check_duration(f))
			print "Processing  File Name:",f + "\tDuration:",duration
			no_samples = duration-1   #no of samples created
			start = 0 
			end = 2*1000 #duration of each audio frame
			step = 2*1000 #duration of each audio frame
			count = 0
			while(end<=duration*1000):
				song = AudioSegment.from_wav(f)
				new_song = song[start:end]
				start += 1000
				end = (start+step)
				count+=1
				result_folder=""
				result_folder = os.getcwd()+"/Result_Audio_"+fname
				if not os.path.exists(result_folder):
					os.makedirs("Result_Audio_"+fname)
				new_song.export("Result_Audio_"+fname+"/"+fname+"_cut_"+str(count)+".wav", format="wav")
			#print count
			print "Processing Done!!!!!!"
			result_folders.append(result_folder)
	#os.chdir(pyaduio_folder)
	return result_folders

def check_bird(folder):
	bird = myaudioAnalysis.classifyFolderWrapper(folder,"svm_rbf","svm_new_dataset") #return dictionary of birds and their count for format uncomment below print
	print bird
	result = max(bird.iteritems(), key=operator.itemgetter(1))[0]
	return result


# folder_name = sys.argv[1]
# result_folders = processing(folder_name)
# #print result_folders
# for folder in result_folders:
# 	result = check_bird(folder)
# 	print "Bird is:",result






