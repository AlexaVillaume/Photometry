'''
AUTHOR
    Alexa Villaume, UCSC

PURPOSE
    To find the point-source objects in a catalog and make a
    cut to only include them

INPUT PARAMETERS
    The catalog for the cuts to be made ont

FILES CREATED
    Shape cut catalog

NOTES
    This is very incomplete. As of now you need to know where to make the
    cut. Plan to make this more complete and interactive.

'''


# Make histogram of a_world values and cut below peak

output = open("shapecutCatalog.txt" , "w")

with open('temp.txt', 'r') as f:
    for object in (raw.strip().split() for raw in f):
        if float(object[11]) < 2e-4:
            output.write("%10s" % object[0] + "%12s" % object[1] +  "%12s" % object[2]
            + "%10s" % object[3] + "%13s" % object[4] + "%10s" % object[5]
            + "%13s" % object[6]+ "%10s" % object[7] + "%13s" % object[8]
            + "%10s" % object[9] + "%13s" % object[10] + "%13s" % object[11] +
            "%13s" % object[12] + "\n")

