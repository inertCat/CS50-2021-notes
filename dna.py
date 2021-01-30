import csv
import sys
import re

#https://pythonforbiologists.com/regular-expressions
#good resource to learn about Regex library (re) for python

#dictionary for unknown person of interest; will add onto it later
unknown = {
    'name' : "unknown"
}

def main():

    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py database.csv sequences.txt Name")
    
    #open file and read row by row into people[]    
    people = []
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        for row in reader:
            people.append(row)
    #print(people) to see list of all people
    #print(people[0]['AGATC']) to see value of AGATC for first person in the array.

    #open dna sequence file and save into "sequence"
    with open(sys.argv[2]) as f:
        sequence = f.read()

    #how many columns in the table? 4 for small, 9 for large.csv
    columns = len(reader.fieldnames)

    #insert new key:value into unknown{}. Skip 1 since name is set as 'name' : "unknown"
    for i in range(1, columns):
        base = reader.fieldnames[i]
        #important: if '' is not surrounding the number of baseRepeats, won't be able to compare the values from unknown to person
        #people[i] has values listed as with ''. so input of baseRepeats also has to be with ''
        baseRepeats = f'{repeatFinder(base, sequence)}'
        unknown[reader.fieldnames[i]] = baseRepeats

    #print(unknown) to check unknown dictionary

    #compare unknown to list of people. Prints name of matching person
    findUnknown(unknown, people, columns, reader)

#Find number of longest repeats.
def repeatFinder(strbase, sequence):

    longest = 0
    dna = sequence

    #check for str base (learn more about this from the link listed on top)
    if re.search(r"(%s)" % strbase, dna) == False:
        return 0
    
    #find all the repeating sequences and store in matches
    matches = re.finditer(r"(%s){1,}" % strbase, dna)

    #go through every matches to find longest sequence
    for m in matches:
        pos = m.start()   #numerical start point of the str repeats
        endpos = m.end()  #end point
    #    print(str(pos) + "-" + str(endpos)) to see numerical value of start/end of repeats
    #    print(dna[pos:endpos]) to see repeats themselves
        repeats = int(len(dna[pos:endpos])) / int(len(strbase))
    #    print(f"Repeats: {repeats}") to see how many times the base repeats
        if repeats > longest:
            longest = repeats
    #print(f"Longest repeats: {longest}")
    longest = int(longest)
    return longest

#input unknown person of interest to see if it matches with anyone in the csv file
def findUnknown(unknown, people, columns, reader):

    #create keys to compare two dictionaries with
    #had to do this in order to not compare the "name", otherwise comparison would always equal false.
    compkeys = []
    for i in range (1, columns):
        compkeys.append(reader.fieldnames[i])
    #print(compkeys) should show all column titles without the "name"

    #compare two dictionaries except 'name'
    for i in range(0, len(people)):
        if all(unknown[keys] == people[i][keys] for keys in compkeys):
            print(people[i]['name'])
            return

    print("No match")


main()


