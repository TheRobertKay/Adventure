# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 03:27:15 2017

@author: rob
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random 
import PIL.Image as Image
import PIL.ImageDraw as ImgDraw
import sys

POOL_LOW = ["Lehmkate", "Holzhütte", "Erbärmlicher Verschlag", "Schweinekoben", "Mietskaserne", "Armenhaus", "Hospital"]
POOL_HANDWERKER_LOW = ["Fassträger", "Hure", "Scherenschleifer", "Bader", "Henker", "Totengräber", "Krämer"]
POOL_AVG = ["Fachwerkhäuschen", "Fischerhütte", "Kleine Werkstatt", ]
POOL_RIVER = ["Fischerhütte", "Flößerei", "Wassermühle", "Lehmgrube"]
POOL_HANDWERKER_AVG = ["Schmied", "Seiler", "Schneider", "Tischler", "Zimmermann", "Gerber", "Schuhmacher", "Färber", "Sattler", "Kürschner", "Steinmetz"]
POOL_WEALTHY = ["Bürgerhaus", "Badehaus", "Bordell"]
POOL_HANDWERKER_WEALTHY = ["Medicus", "Apotheke", "Händler", ]
POOL_RICH = ["Anwesen", "Stadtschloss", ]
POOL_HANDWERKER_RICH = ["Handelskontor"]
POOL_STAEDTISCHE_EINRICHTUNGEN = ["Gericht", "Zwinger", "Schule", "Universität", "Friedhof", "Großer Marktplatz", "Kleiner Marktplatz"]
POOL_WEHRANLAGEN = ["Tor", "Befestigte Pforte", "Torturm", "Wehrturm", "Mauer", "Geschützstellung", "Graben", "Wehrgang"]
POOL_ZUNFTHAEUSER =  ["der Schneider", "der Tuchhändler", "der Schmiede", "der Zimmerleute", "der Steinmetze"]
POOL_ZUSTAENDE_POOR = ["heruntergekommen", "leerstehend", "zerstört", "schäbig", "abgebrannt", "eingestürzt", "schmutzig", "geschlossen", "verrammelt", "verwüstet", "beschmiert", "besetzt", "stinkend", "modrig"]
POOL_ZUSTAENDE_KATASTROPHEN = ["brennend", "schwelend", "qualmend", "überflutet"]

def loc_gen(height=200,width=200,min_distance=10,border=50):
    loc_list = []
    
    centrum = np.array([width/2,height/2])
    
    for i in range(1000):
        x = random.uniform(0,width)
        y = random.uniform(0,height)
        tmp_coord = np.array([x,y])
        
        
        dist_vec = tmp_coord-centrum
        if (np.linalg.norm(dist_vec) < min((height-border)/2,(width-border)/2)):
            min_dist = max(height,width)
            for j in range(len(loc_list)):
                neigh_dist = np.linalg.norm(loc_list[j]-tmp_coord)
                if (neigh_dist < min_dist):
                    min_dist = neigh_dist
            
            if min_dist > min_distance:
                loc_list.append(tmp_coord)
    
    
    return loc_list


def wall_gen(loc_list,img,height=200,width=200,border=50):
    #town = np.zeros((height,width))
    #img = Image.fromarray(town)
    draw = ImgDraw.ImageDraw(img)
    centrum = np.array([width/2,height/2])
    radius = min((height-border)/2,(width-border)/2)
    
    wall_list = []
    
    for i in range(len(loc_list)):
        if (np.abs(np.linalg.norm(centrum-loc_list[i])-radius) < 30):
            wall_list.append(loc_list[i])

    
    for i in range(len(loc_list)):
        loc = loc_list[i]
        
        draw.line((loc[0] - 2,loc[1] - 2) + (loc[0] + 2,loc[1] + 2),fill=100)
        draw.line((loc[0] - 2,loc[1] + 2) + (loc[0] + 2,loc[1] - 2),fill=100)
        
        draw.text((loc[0],loc[1]),str(i),fill=200)
        
    
    for i in range(len(wall_list)):
        min_angle = 360
        start = (wall_list[i][0],wall_list[i][1])
        current_vec = centrum - wall_list[i]
        for j in range(len(wall_list)):
            if i != j:
                search_vec = centrum - wall_list[j]
                ang1 = np.arctan2(*current_vec[::-1])
                ang2 = np.arctan2(*search_vec[::-1])
                angle = np.rad2deg((ang1-ang2) % (2  * np.pi))
                if angle < min_angle:
                    min_angle = angle
                    end = (wall_list[j][0],wall_list[j][1])
        
        draw.line(start+end,fill=200)
    
    img.show() 
    
    
    
    
def link_gen(loc_list,height=200,width=200,max_distance=10):
    town = np.zeros((height,width))
    img = Image.fromarray(town)
    draw = ImgDraw.ImageDraw(img)
    
    for i in range(len(loc_list)):
        loc = loc_list[i]
        
        draw.line((loc[0] - 2,loc[1] - 2) + (loc[0] + 2,loc[1] + 2),fill=100)
        draw.line((loc[0] - 2,loc[1] + 2) + (loc[0] + 2,loc[1] - 2),fill=100)
        
        #draw.text((loc[0],loc[1]),str(i),fill=200)    
    
    safe_list = []
    
    for i in range(len(loc_list)):
        safe_list.append(0)
    
    for i in range(len(loc_list)):
        n_list = []
        for j in range(len(loc_list)):
            if i != j and safe_list[j] < 6:
                dist = np.linalg.norm(loc_list[i]-loc_list[j])
                if dist < max_distance:
                    if len(n_list) < 6-safe_list[i]:
                        n_list.append((dist,j))
                        n_list = sorted(n_list)
                    else:
                        n_list.append((dist,j))
                        n_list = sorted(n_list)
                        n_list.pop()
                   
        for j in range(len(n_list)):
            safe_list[n_list[j][1]] += 1
            draw.line((loc_list[i][0],loc_list[i][1]) + (loc_list[n_list[j][1]][0],loc_list[n_list[j][1]][1]), fill=128)
    #img.show()
    return img


def main():
    locs = loc_gen(height=1000,width=1000,min_distance=30)
    img = link_gen(locs,height=1000,width=1000,max_distance=60)
    wall_gen(locs,img,height=1000,width=1000)
    #img = image.fromarray(town)

    #test = draw.ImageDraw(img)  
    #test.line((50, 50) + (100,100), fill=128)
    #test.line((0, im.size[1], im.size[0], 0), fill=128)
    #test.save(sys.stdout, "PNG")
    #img.show()
    
    

if __name__ == "__main__":
    main()