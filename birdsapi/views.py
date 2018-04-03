import os
import shutil

from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer
import subprocess
import re
from pydub import AudioSegment
import myaudioAnalysis
import operator



og_folder = os.getcwd()

def check_duration(fname):
	op= 0.0
	#os.chdir(os.getcwd()+"/birdsapi")
	process = subprocess.Popen(['ffmpeg',  '-i', fname], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	stdout, stderr = process.communicate()
	matches = re.search(r"Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", stdout, re.DOTALL).groupdict()
	# #print matches['hours']
	# #print matches['minutes']
	# #print matches['seconds']
	op = float(matches['hours'])*3600+float(matches['minutes'])*60+float(matches['seconds'])
	return op



def processing(folder):
    result_folders = []
    files = os.listdir(os.getcwd())
    result_folder =""
    fname = ""
    for f in files:
        if ('.wav' in f.lower()):
            # print int(check_duration(f))
            fname, file_format = f.split(".")
            # print fname
            duration = int(check_duration(f))
            print "Processing  File Name:", f + "\tDuration:", duration
            no_samples = duration - 1  # no of samples created
            start = 0
            end = 2 * 1000  # duration of each audio frame
            step = 2 * 1000  # duration of each audio frame
            count = 0
            while (end <= duration * 1000):
                song = AudioSegment.from_wav(f)
                new_song = song[start:end]
                start += 1000
                end = (start + step)
                count += 1
                result_folder = os.getcwd() + "/Result_Audio_" + fname
                if not os.path.exists(result_folder):
                    os.makedirs("Result_Audio_" + fname)
                new_song.export("Result_Audio_" + fname + "/" + fname + "_cut_" + str(count) + ".wav", format="wav")
            # print count
            print "Processing Done!!!!!!"
            print result_folder
            #result_folders.append(result_folder)
        #os.chdir(og_folder)
    return result_folder,fname

def check_bird(folder):
    bird = myaudioAnalysis.classifyFolderWrapper(folder,"svm_rbf","svm_new_dataset")
    print bird
    result = max(bird.iteritems(), key=operator.itemgetter(1))[0]
    return result



class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            folder = og_folder + "/birdsapi"
            os.chdir(folder)
            fname1 = file_serializer.data['file']
            wavFileName = (fname1.split('/')[2]).split('.')[0]
            f = wavFileName+".wav"
            f1 = wavFileName+"_resampled.wav"
            command = "avconv -i \"" + f + "\" -ar " +str(16000) + " -ac " + str(1) + " \"" + f1 + "\"";
            print command
            os.system(command.decode('unicode_escape').encode('ascii', 'ignore').replace("\0", ""))
            os.remove(f)
            res_folder,fname= processing(folder)
            result = check_bird(res_folder)
            fname = fname+".wav"
            from1 = folder+"/"+fname
            to1 = res_folder+"/"+fname
            print from1
            print to1
            os.rename(from1,to1)
            shutil.rmtree(res_folder)
            return Response({'data':file_serializer.data,'bird':result}, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)