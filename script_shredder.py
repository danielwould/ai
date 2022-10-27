import glob, os,re
os.chdir("./scripts")



scenesf = open ("scenes.csv","w")

scenetype = None
scenetext=""
scenesCount=0
scene_line_count=0
total_line_count=0
episode=""
scene_location=""

def write_csv_line(scene_text,scene_number,scene_length,scene_type,scene_location,episode, labels):
    
    scenesf.writelines("\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\"\n".format(episode,scene_number,scene_length,scene_type,scene_location,labels,scene_text))

def write_csv_header():
    
    scenesf.writelines("Episode,SceneNumber,SceneLength,SceneType,SceneLocation,Labels,SceneText\n")

write_csv_header()

for file in glob.glob("*.txt"):
    print(file)
    episode=file
    scenesCount=0
    labels=""
    character_count=0
    f = open(file, "r")

    for x in f:
        if ("shooting script" in x.lower() ):
            continue
        if ("swx" in x.lower() ):
            continue
        if ("responder - ep" in x.lower() ):
            continue
        if ("CAST IN ORDER OF APPEARANCE" in x.upper() ):
            break
        if ("END CREDITS" in x.upper() ):
            break
        
        pattern = r'[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
        whitespace_pattern = r'\s+'
        # Replace all occurrences of character s with an empty string
        mod_string = re.sub(pattern, '', x )
        mod_string = re.sub(whitespace_pattern, ' ', mod_string )
        mod_string=mod_string.replace("|","")
        mod_string=mod_string.replace("*","")
        
        mod_string=mod_string.replace("\"","\"\"")
        x=mod_string.strip()
        if (x == ""):
            continue

        if (character_count+len(x) >495):
            write_csv_line(scenetext,scenesCount,scene_line_count,scenetype,scene_location,episode,labels)
            scenetext=""
            labels=""
            scene_line_count=0
            character_count=0
        character_count=character_count+len(x)
        if ("INT." in x and "EXT." in x):
            print("scene inside and outside")
            scenesCount=scenesCount+1
            if scenetext!="":
                print ("scene: {} : length {} : {}".format(scenetype,scene_line_count,scenetext))
                write_csv_line(scenetext,scenesCount,scene_line_count,scenetype,scene_location,episode,labels)
                scenetext=""
                labels=""
                total_line_count=total_line_count+scene_line_count
                scene_line_count=0
                character_count=0
            
            scenetype="INT.EXT."
            scene_location=x
            scenetext=x


        elif ("INT." in x): 
            scenesCount=scenesCount+1
            print("scene interior")
            if scenetext!="":
                print ("scene: {} : length {} : {}".format(scenetype,scene_line_count,scenetext))
                write_csv_line(scenetext,scenesCount,scene_line_count,scenetype,scene_location,episode,labels)
                scenetext=""
                labels=""
                total_line_count=total_line_count+scene_line_count
                scene_line_count=0
                character_count=0
            scenetype="INTERIOR"
            labels=labels+"INTERIOR"
            scene_location=x
            scenetext=x
        elif ("EXT." in x):
            scenesCount=scenesCount+1
            print("scene exterior")
            if scenetext!="":
                print ("scene: {} : length {} : {}".format(scenetype,scene_line_count,scenetext))
                write_csv_line(scenetext,scenesCount,scene_line_count,scenetype,scene_location,episode,labels)
                scenetext=""
                labels=""
                total_line_count=total_line_count+scene_line_count
                scene_line_count=0
                character_count=0
            scenetype="EXTERIOR"
            labels=labels+"EXTERIOR"
            scene_location=x
            scenetext=x
        elif (scenetype!=None):
            if (scenetext==""):
                scenetext=x
            else:
                if "body" in x.lower():
                    labels=labels+";BODY"
                if "kill" in x.lower():
                    labels=labels+";KILL"
                if "murder" in x.lower():
                    labels=labels+";MURDER"
                if "gun" in x.lower():
                    labels=labels+";GUN"
                if "suspect" in x.lower():
                    labels=labels+";SUSPECT"
                scenetext=scenetext+"\n"+x
            scene_line_count=scene_line_count+1
    write_csv_line(scenetext,scenesCount,scene_line_count,scenetype,scene_location,episode,labels)
    scenetext=""
    labels=""
    scenetype = None
    scene_line_count=0
    character_count=0

print("found {} scenes with average length {}".format(scenesCount, total_line_count/scenesCount))