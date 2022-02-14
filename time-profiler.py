import argparse
import re
import os
parser = argparse.ArgumentParser()
parser.add_argument("path", help="Filepath")
args = parser.parse_args()
files = os.listdir(args.path)
count=0
for f in files:
	if re.search('.py',f):
            path=args.path+"/"+f
            count+=1
            with open(path, 'r+') as fd:
                contents = fd.readlines()
                offset=0
                if count==1:
                    fd.seek(0)
                    contents.insert(0, 'import time \nf = open("exec-time.log", "a")\nf.write("path, method, time")\nf.write("\\n")\nf.close()\ndef cal_time(fun):\n  def time_cal1(*arg, **kw):\n    startTime= time.time()*1000\n    fun(*arg,**kw)\n'
                                       '    endTime = time.time()*1000\n    f = open("exec-time.log", "a")\n'
                                       '    f.write(__file__+" "+fun.__name__+" "+str(endTime-startTime)+" ms")\n    f.write("\\n")\n'
                                       '    f.close()\n  return time_cal1\n')
                else:
                    fd.seek(0)
                    contents.insert(0, 'import time \ndef cal_time(fun):\n  def time_cal1(*arg, **kw):\n    startTime= time.time()*1000\n'
                                       '    fun(*arg,**kw)\n    endTime = time.time()*1000\n    f = open("exec-time.log", "a")\n'
                                       '    f.write(__file__+" "+fun.__name__+" "+str(endTime-startTime)+" ms")\n    f.write("\\n")\n'
                                       '    f.close()\n  return time_cal1\n')
                for i in range(len(contents)):
                    if re.search('^def', contents[i+offset]):
                        contents.insert(contents.index(contents[i+offset]),'@cal_time\n')
                        offset+=1
                fd.seek(0)
                fd.writelines(contents)
