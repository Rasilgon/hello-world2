# -*- coding: utf-8 -*-
"""
Created on Wed Dec 17 11:03:16 2014

@author: trashtos
"""
############################################################################
# Profound Participants Database
# Purpose:  A class to extract information from Profound Database
# Author: Ramiro
# 
# Takes as an input a csv table and delivers the information as txt file, 
# saving the files in the folder where the csv table is.
# Requires two inputs, see help.
#   
# Columns names are predefined (see self.run)
# Feel free to create any modification of it.
# 
# Requires pandas, numpy and argparse. 
#
#############################################################################


################Import_Moduless########################
import sys, os
import os.path
import subprocess

try:
    import pandas as pd
except:
    print "pandas is required"
try:
    import numpy as np
except: 
    print "numpy is required"

try:
    import argparse
except: 
    print "argparse is required"



###################Class and functions##################
class Profound_Members(object):
   
    def get_mails_TGWG (self, inputTable, cols):
        inTable = str(os.path.abspath(inputTable))
        inFile = pd.read_csv(inTable, header=True, names = cols ) 
        wgtg = cols[13:36]
        mails = np.asarray(inFile["Email"])        
        for group in wgtg:
            print " "
            print group
            people = []
            lista = np.asarray(inFile[group])
            for i in np.arange(len(lista)):
                if lista[i] == "x":
                    print mails[i]
                    people.append(mails[i]) 
            txtfile = inTable[:-4] + "_" + group +".txt"
            print "printing out", txtfile
            f = open(txtfile, "w")
            for i in people:              
                f.write(str(i) + '\n')
            f.close()
    
    
    def get_mails_names_TGWG(self, inputTable, cols):
        inTable = os.path.abspath(inputTable)
        inFile = pd.read_csv(inTable, header=True, names = cols ) 
        wgtg = cols[13:36]
        mails = np.asarray(inFile["Email"])
        names = np.asarray(inFile["Name"])        
        for group in wgtg:
            print " "
            print group
            people = []
            lista = np.asarray(inFile[group])
            for i in np.arange(len(lista)):
                if lista[i] == "x":
                    info =str(names[i]) + " "+ str(mails[i])
                    print info
                    people.append(info)
            txtfile =inTable[:-4] + "_" +  group +" people.txt"
            print "printing out", txtfile
            f = open(txtfile, "w")
            for i in people:              
                f.write(str(i) + '\n')
            f.close()
        
        

    def get_list_of_participants(self, inputTable, cols):
        inTable = os.path.abspath(inputTable)
        inFile = pd.read_csv(inTable, header=True, names = cols ) 
        afils = np.asarray(inFile["Affiliation"])
        countries = np.asarray(inFile["Country"])
        webpages = np.asarray(inFile["Webpage"])
        names = np.asarray(inFile["Name_clean"])
        listed = np.asarray(inFile["listpart"])
        people = []
        lista = np.asarray(names)
        for i in np.arange(len(lista)):
            if listed[i] == "Yes":
                info =str(names[i]) + ", "+ str(afils[i]) + ", "+str(countries[i]) + " (webpage) "+str(webpages[i])
                print info
                people.append(info)
	txtfile =inTable[:-4] + "_participantslist.txt"
	print "printing out", txtfile
	f = open(txtfile, "w")
	for i in people:              
	    f.write(str(i) + '\n')
	f.close()
        
        
    def get_all_mails (self, inputTable, cols):
        inTable = os.path.abspath(inputTable)
        inFile = pd.read_csv(inTable, header=True, names = cols ) 
        mails = np.asarray(inFile["Email"])
        names = np.asarray(inFile["Name"])
        people = []
        lista = np.asarray(names)
        for i in np.arange(len(lista)):
            info =str(mails[i])
            print info
            people.append(info)
        txtfile =inTable[:-4] + "_allmails.txt"
        print "printing out", txtfile
        f = open(txtfile, "w")
        for i in people:              
            f.write(str(i) + '\n')
        f.close()
    
    def get_all_mails_names (self, inputTable, cols):
        inTable = os.path.abspath(inputTable)
        inFile = pd.read_csv(inTable, header=True, names = cols ) 
        mails = np.asarray(inFile["Email"])
        names = np.asarray(inFile["Name"])
        people = []
        lista = np.asarray(names)
        for i in np.arange(len(lista)):
            info =str(names[i]) + " " + str(mails[i])
            print info
            people.append(info)
        txtfile =inTable[:-4] + "_allpeople.txt"
        print "printing out", txtfile
        f = open(txtfile, "w")
        for i in people:              
            f.write(str(i) + '\n')
        f.close()
        
    
    def run(self):
            parser = argparse.ArgumentParser()
            parser.add_argument("-i", "--inTable", dest="inputTable", type=str, help="Input table as csv")
            parser.add_argument("-l", "--list", dest="listtoprint", type=str, help="Specify a list to print: MailsTGWG, NamesMailsTGWG, AllMails, AllMailsNames, ListOfParticipants")
            args = parser.parse_args()        
            cols = ["Name", "Name_clean","Email","second email","Affiliation", "Webpage","listpart", "Country","Inclusiveness country?","Gender", "Early-Stage Researcher","Action Function 1", "Action Function 2","WG1", "WG2", "WG3","WG4","TG1","TG2","TG3", "TG4","TG5","TG6","TG7","TG8","TG9","TG10", "TG11","TG12", "TG13","TG14","TG15","TG16","TG17","TG18","TG19","ESR (Phd less than 8 years ago?)","Researcher, stakeholder (if stakeholder, specifiy)","From international cooperation institutions","Would like to host a MC/WG meeting (which year?)?","Models you mainly use?1","Models you mainly use?2","Database & data networks you use or contribute to", "Already provided info"]            
            
            if args.inputTable is None:
                print("No input table specified.")
                parser.print_help()
                sys.exit()
            if args.listtoprint is None:
                print("No list specified.")
                parser.print_help()
                sys.exit()  
            
            if args.listtoprint == "MailsTGWG":
                self.get_mails_TGWG (args.inputTable, cols)
            if args.listtoprint == "NamesMailsTGWG":
                self.get_mails_names_TGWG(args.inputTable, cols)
            if args.listtoprint == "AllMails":
                self.get_all_mails (args.inputTable, cols)
            if args.listtoprint == "AllMailsNames":
                self.get_all_mails_names (args.inputTable, cols)
            if args.listtoprint == "ListOfParticipants":
                self.get_list_of_participants(args.inputTable, cols)


##################Main #############################################

if __name__ == '__main__':
    obj = Profound_Members()
    obj.run()
   


 
 
