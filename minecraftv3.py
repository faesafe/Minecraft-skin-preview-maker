# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 12:30:39 2021

@author: Delta
"""

from PIL import Image
import os
import shutil
import json

import firebase_admin
from firebase_admin import credentials
#from firebase_admin import storage
from google.cloud import storage


#directory = sys.argv[1]
#print(sys.argv)
#input('Press ENTER to exit')    
directory  = "PUT YOUR DIRECTORY WITH INPUT SKINS HERE"
outputDirectory = ""
outputBucketDirectory = "PUT YOUR FIREBASE BUCKET URL HERE"

#%%

def confirm(prompt=None, resp=True):
    """prompts for yes or no response from the user. Returns True for yes and
    False for no.

    'resp' should be set to the default value assumed by the caller when
    user simply types ENTER.

    >>> confirm(prompt='Create Directory?', resp=True)
    Create Directory? [y]|n: 
    True
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: 
    False
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: y
    True

    """
    
    if prompt is None:
        prompt = 'Confirm'

    if resp:
        prompt = '%s [%s]|%s: ' % (prompt, 'y', 'n')
    else:
        prompt = '%s [%s]|%s: ' % (prompt, 'n', 'y')
        
    while True:
        ans = input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print('please enter y or n.')
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False



def CreateThumbnail(PathIn, PathOut):
    WorkImage = Image.open(PathIn)
    skinType = False #true for slim, false for normal
    pixel1 = WorkImage.getpixel((46,53))
    pixel2 = WorkImage.getpixel((54,24))
    pixel3 = WorkImage.getpixel((62,39))
    pixel4 = WorkImage.getpixel((42,50))
    
    if pixel1 == pixel2 and pixel3 == pixel4:
        skinType = True
    #     print("SLIM")
    # else:
    #     print("NORMAL")
        

    HeadFront = WorkImage.crop((8, 8, 16, 16))
    HeadBack = WorkImage.crop((24, 8, 32, 16))
    HeadFrontLayer = WorkImage.crop((40, 8, 48, 16))
    HeadBackLayer = WorkImage.crop((56, 8, 64, 16))
    
    TorsoFront = WorkImage.crop((20, 20, 28, 32))
    TorsoBack = WorkImage.crop((32, 20, 40, 32))
    TorsoFrontLayer = WorkImage.crop((20, 36, 28, 48))
    TorsoBackLayer = WorkImage.crop((32, 36, 40, 48))
    
    RightLegFront = WorkImage.crop((4, 20, 8, 32))
    RightLegBack = WorkImage.crop((12, 20, 16, 32))
    RightLegFrontLayer = WorkImage.crop((4, 20+16, 8, 32+16))
    RightLegBackLayer = WorkImage.crop((12, 20+16, 16, 32+16))
      
    LeftLegFront = WorkImage.crop((20, 52, 24, 64))
    LeftLegBack = WorkImage.crop((28, 52, 32, 64))
    LeftLegFrontLayer = WorkImage.crop((20-16, 52, 24-16, 64))
    LeftLegBackLayer = WorkImage.crop((28-16, 52, 32-16, 64))    
    

    OutputImage = Image.new(WorkImage.mode, (36, 32))
    OutputImageLayer = Image.new(WorkImage.mode, (36, 32))
    #OutputImageLayer = Image.new("RGBA", (36,32), (255,255,255)) #for debugging, white background
    distance = 20 # 16 - character width, 
    if skinType == True:
        RightArmFront = WorkImage.crop((36, 52, 40-1, 64))
        RightArmBack = WorkImage.crop((52-1, 20, 56-2, 32))
        RightArmFrontLayer = WorkImage.crop((44, 20+16, 48-1, 32+16))
        RightArmBackLayer = WorkImage.crop((52-1, 20+16, 56-2, 32+16))
        
        LeftArmFront = WorkImage.crop((44, 20, 48-1, 32))
        LeftArmBack = WorkImage.crop((44-1, 52, 48-2, 64))
        LeftArmFrontLayer = WorkImage.crop((36+16, 52, 40+16-1, 64))
        LeftArmBackLayer = WorkImage.crop((44+16-1, 52, 48+16-2, 64))
        
        
        OutputImage.paste(RightArmFront, (12,8))
        OutputImage.paste(LeftArmFront, (1,8))
        OutputImage.paste(RightArmBack, (12+distance,8))
        OutputImage.paste(LeftArmBack, (1+distance,8))
        
        OutputImageLayer.paste(RightArmFrontLayer, (1,8))
        OutputImageLayer.paste(LeftArmFrontLayer, (12,8))# swapped arms due to error above
        OutputImageLayer.paste(LeftArmBackLayer, (1+distance,8))
        OutputImageLayer.paste(RightArmBackLayer, (12+distance,8))# swapped legs due to error above    
        
    else:
        
        #RightArmFront = WorkImage.crop((44, 20, 48, 32))
        RightArmFront = WorkImage.crop((36, 52, 40, 64))
        RightArmBack = WorkImage.crop((52, 20, 56, 32))
        RightArmFrontLayer = WorkImage.crop((44, 20+16, 48, 32+16))
        RightArmBackLayer = WorkImage.crop((52, 20+16, 56, 32+16))   
    
        #LeftArmFront = WorkImage.crop((36, 52, 40, 64))
        LeftArmFront = WorkImage.crop((44, 20, 48, 32))
        LeftArmBack = WorkImage.crop((44, 52, 48, 64))
        LeftArmFrontLayer = WorkImage.crop((36+16, 52, 40+16, 64))
        LeftArmBackLayer = WorkImage.crop((44+16, 52, 48+16, 64))
        
        OutputImage.paste(RightArmFront, (12,8))
        OutputImage.paste(LeftArmFront, (0,8))
        OutputImage.paste(RightArmBack, (12+distance,8))
        OutputImage.paste(LeftArmBack, (0+distance,8))
        
        OutputImageLayer.paste(RightArmFrontLayer, (0,8))
        OutputImageLayer.paste(LeftArmFrontLayer, (12,8))# swapped arms due to error above
        OutputImageLayer.paste(LeftArmBackLayer, (0+distance,8))
        OutputImageLayer.paste(RightArmBackLayer, (12+distance,8))
        
        
        
    OutputImage.paste(HeadFront, (4,0))
    OutputImage.paste(TorsoFront, (4,8))
    OutputImage.paste(LeftLegFront, (8,20))
    OutputImage.paste(RightLegFront, (4,20))# swapped legs due to error above    
    OutputImageLayer.paste(HeadFrontLayer, (4,0))   
    OutputImageLayer.paste(TorsoFrontLayer, (4,8))  
    OutputImageLayer.paste(LeftLegFrontLayer, (4,20))
    OutputImageLayer.paste(RightLegFrontLayer, (8,20))   
    
    OutputImage.paste(HeadBack, (4+distance,0))    
    OutputImage.paste(TorsoBack, (4+distance,8))    
    OutputImage.paste(LeftLegBack, (4+distance,20))
    OutputImage.paste(RightLegBack, (8+distance,20))    
    OutputImageLayer.paste(HeadBackLayer, (4+distance,0))    
    OutputImageLayer.paste(TorsoBackLayer, (4+distance,8))    
    OutputImageLayer.paste(LeftLegBackLayer, (4+distance,20))
    OutputImageLayer.paste(RightLegBackLayer, (8+distance,20))
    
    OutputImage.paste(OutputImageLayer, (0,0), OutputImageLayer) #paste with "transparency"
    # char - 16 wide, 32 high
    OutputImage = OutputImage.resize((180,160), resample=Image.BOX)    
    OutputImage.save(PathOut)
    
    #print("Created thumbnail from " + PathIn + " to " + PathOut)
#%%


def upload_blob(source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"
    storage_client = storage.Client()
    bucket = storage_client.bucket("english-skins-minecraft-pe.appspot.com")
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )
## FOLDER STRUCTURE
## dir 
##  input
##       dream
##          1.png
##  output
##      dream
##          skins
##              1.png
##          icons
##              1.png

def Main():
    print(f"Working directory is {os.getcwd()}\n")
    lista = []
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.path.join(os.getcwd(), "serviceAccountKey.json")
    cred = credentials.Certificate(os.path.join(os.getcwd(), "serviceAccountKey.json"))
    firebase_admin.initialize_app(cred, { 'storageBucket' : outputBucketDirectory})
    outputDir = os.path.join(os.getcwd(), "output")
    print(f"Output directory is {outputDir}\n")
    if os.path.isdir(outputDir):
        if confirm(f"Delete directory {outputDir} with its contents?"):
            shutil.rmtree(outputDir)     
    os.mkdir(outputDir) 
    
    creators = {}
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), "input")):
        lista.append(dirs)
        skinCount = 0
        skinCreator = os.path.basename(os.path.normpath(root))
        skinsPath = os.path.join(outputDir, os.path.basename(os.path.normpath(root)),  "Skins")
        iconsPath = os.path.join(outputDir, os.path.basename(os.path.normpath(root)),  "Icons")
        
        os.makedirs(skinsPath, exist_ok=True)
        os.makedirs(iconsPath, exist_ok=True)
        for file in files: 

            ExitPath = os.path.join(iconsPath, file)
            SourcePath = os.path.join(root, file)
            skinCreator = os.path.basename(os.path.normpath(root))
            fbBlob = "1.0.0/" + skinCreator + "/" # Firebase path for each creator           
            skinCount = skinCount + 1

            CreateThumbnail(SourcePath, ExitPath)
            upload_blob(ExitPath, (fbBlob + "Icons/" + skinCreator + file))
            upload_blob(SourcePath, (fbBlob + "Skins/" + skinCreator + file))
            resulting = shutil.copy(SourcePath, os.path.join(skinsPath, file))
        creators[skinCreator] = skinCount
        print(f"Processed {skinCount} {skinCreator}'s skins")
        
    shutil.rmtree(os.path.join(outputDir, "input"))#removes empty folder created in above loop
    with open(os.path.join(outputDir, "output.json"), "w") as outfile:
        creators.pop("input") #removes empty value created in above loop
        json.dump(creators, outfile, indent = 4)
        print(f"JSON created, with {len(creators)} elements")
        
    input('Press ENTER to exit')    
Main()