#/usr/bin/python3


def reshape_preset(data ,value=None,xfade=0,flash=0,ptfade=0,DELAY=None):

    f=0 #fade

    out = []
    delay=0
    for row in data:
        #cprint("reshape_preset in:",row)
        line = {}
        line["DELAY"]=delay
        if type(value) is float:
            line["VALUE"] = value #round(value,3)
        else:
            line["VALUE"] = value

        if "FX" not in row:
            cprint("698 FX not in row...",row,color="red")
            row["FX"] = ""
        else:
            if type(row["FX"]) is not str:
                cprint("702 FX is not str...",row,color="red")
                row["FX"] = ""

        if value is not None:
            line["FX"] = row["FX"].split(":",1)[-1]
        else:
            line["FX"] = row["FX"]

        if row["FX2"]:
            line["FX2"] = row["FX2"]

        if row["FIX"]:
            line["FIX"] = row["FIX"]
        if row["ATTR"]:
            line["ATTR"] = row["ATTR"]


        if row["VALUE"] is not None:
            if value is None: 
                v=row["VALUE"]
                if type(v) is float:
                    line["VALUE"]  = v #round(v,3)
                else:
                    line["VALUE"]  = v

        if row["ATTR"] in ["PAN","TILT"]:
            f = ptfade 

        for a in ["DIM","ZOOM","FOCUS","RED","GREEN","BLUE","WHITE","AMBER","IRIS","BLADE"]: 
            #FADE ATTRIBUTES
            if a in row["ATTR"]:
                f = xfade 
                break

        if flash:
            xfade = 0
        if type( f ) is float:
            line["FADE"] = round(f,4)
        else:
            line["FADE"] = f
        
        if 0:
            cprint("reshape_preset j",line,color="red") 
        #cprint("reshape_preset out:",line)
        out.append(line)

        if DELAY:
            if DELAY._is():
                delay+=DELAY.val()/100 #0.02
    return out
