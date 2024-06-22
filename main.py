import zipfile, wget, os, shutil


saveFolder = "output/intern"
try:
    shutil.rmtree(saveFolder.split("/")[0])
except:
    pass

def extractZip(path):
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(saveFolder)
def downloadFromUrl(url):
    filename = wget.download(url,"embeddedPython.zip")
    return filename
def append_line_to_file(file_path, line):
    try:
        with open(file_path, 'a') as file:
            file.write(line + '\n')
    except Exception as e:
        print(f"An error occurred: {str(e)}")

python_versions = ["3.9.0","3.10.0","3.11.0","3.12.0","3.13.0"]

I = 0
for i in range(len(python_versions)-1):
    print(f"{i+1}. {python_versions[i]}")
    I = i
print(f"{I+2}. custom (specify)")
    
selection = int(input("number from 1 to "+str(I+2)+": "))
if not selection == I+2:
    version = python_versions[(selection-1)%len(python_versions)]
else:
    version = str(input("Custom version: "))

try:
    os.removedirs("output")
except:
    pass
try:
    os.mkdir(saveFolder)
except:
    pass
downloadFromUrl(f"https://www.python.org/ftp/python/{version}/python-{version}-embed-amd64.zip")
extractZip("embeddedPython.zip")
os.remove("embeddedPython.zip")
pth_file = ""
files = os.listdir(saveFolder)
for f in files:
    if f[-5:] == "._pth":
        pth_file = str(saveFolder+"/"+f).split("/")[-1]
cwd = os.getcwd()
os.chdir(saveFolder)
os.system(f"python.exe ../../get-pip.py")
print(pth_file)
append_line_to_file(pth_file,"Lib\site-packages")
print("write any pip package you want to install, type quit to quit")
t = input()
while not t == "quit":
    try:
        os.system("python.exe -m pip install "+t)
        print(t + " was successfully installed")
    except:
        print("Not successfull, please try again")
    t = input()
print("Quitting python setup, creating start.bat")
start = input("What is the name of the python file that should be started?: ")

f = open("../start.bat", "w+")
f.write(f"""
@echo off
cd intern
python.exe {start} 

""")
f.close()
print("Copying all files from input folder into the output directory...")
os.chdir(cwd)
os.system('copy "input/*.*" "output/intern"')
