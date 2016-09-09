thing = cmds.ls(sl=True)


######### Remove Namespace ############

newThing = []
for node in thing:
    new = node.replace('abcLIGHT3:copied','')
    print new
    newThing.append(new)
    
##### Convert to Int ##########

newThingInt = []
for node in newThing:
    print node
    new = int(node)
    newThingInt.append(new)
    
######## Sort ####

sort = sorted(newThingInt)
    
######### Back to String ############
    
newThingString = []    
    
for node in sort:
    #print node
    newString = str(node)
    newThingString.append(newString)
    
############# Add namespace back on #####################

newThingStringNamed = []
    
for node in newThingString:
    newObject = 'abcLIGHT3:copied' + node
    newThingStringNamed.append(newObject)

#### Get Every Other ####
thingSort = newThingStringNamed[::2]   
cmds.select(thingSort)
