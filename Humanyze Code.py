# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import csv
import networkx as nx
from operator import itemgetter
import community
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import subplots, show
import seaborn as sns
import statistics


##################################################Creating graph files########################################################################################################

#Import CSV data
Networkdata1 = pd.read_csv('/Users/christiaanbecker/Desktop/Humanyze/Humanyze_Sample_Dataset_email/Daily E-mail_Table 1.csv')
Nodes = pd.read_csv('/Users/christiaanbecker/Desktop/Humanyze/Humanyze_Sample_Dataset_email/ParticipantInfo-Table 1.csv')

#Drop columns
NetworkdataD = Networkdata1.drop(['Date', 'Count', 'Receiver Type Percentage', 'Receiver Type'], axis=1)

#Collapse dataset accros sender and reciever ID
Networkdata = NetworkdataD.groupby(['Sender', 'Sender Location', 'Sender Team', 'Sender Manager?', 'Receiver',	'Receiver Location', 'Receiver Team', 'Receiver Manager?',  'Internal/External', 'Internal Location',	'External Location', 'Internal / External Team Coms', 'Internal / External Team Coms / Business unit'])['Weight'].sum().to_frame('Sum Weights').reset_index() 

##################################################Internal Boston########################################################################################################

NetworkdataInB = Networkdata['Internal/External'] == "Internal"
NetworkdataIn = Networkdata[NetworkdataInB].reset_index(drop = True)

#Create internal coms dataframe for Boston
NetworkdataInBB = NetworkdataIn['Internal Location'] == "Boston"
NetworkdataInB = NetworkdataIn[NetworkdataInBB].reset_index(drop = True)

#Create internal coms dataframe for Boston for Business
NetworkdataInBB1 = NetworkdataIn[(NetworkdataIn['Sender Team'] == "Business")  & (NetworkdataIn['Sender Location'] == "Boston")]

#Create internal coms dataframe for Boston for Tech DC
NetworkdataInBTDCB = NetworkdataIn['Sender Team'] == "Tech DC"
NetworkdataInBTDC = NetworkdataIn[NetworkdataInBTDCB].reset_index(drop = True)

#Create internal coms dataframe for Boston for Tech HYPE
NetworkdataInBTHB = NetworkdataIn['Sender Team'] == "Tech HYPE"
NetworkdataInBTH = NetworkdataIn[NetworkdataInBTHB].reset_index(drop = True)

#Create internal coms dataframe for Boston for external coms between Business and other teams
NetworkdataInBExBBB = NetworkdataIn['Internal / External Team Coms / Business unit'] == "B External Business"
NetworkdataInBExBB = NetworkdataIn[NetworkdataInBExBBB].reset_index(drop = True)

#Create internal coms dataframe for Boston for external coms between Tech DC and other teams
NetworkdataInBExBTDCB = NetworkdataIn['Internal / External Team Coms / Business unit'] == "B External Tech DC"
NetworkdataInBExBTDC = NetworkdataIn[NetworkdataInBExBTDCB].reset_index(drop = True)

#Create internal coms dataframe for Boston for external coms between Tech HYPE and other teams
NetworkdataInBExBTHB = NetworkdataIn['Internal / External Team Coms / Business unit'] == "B External Tech HYPE"
NetworkdataInBExBTH = NetworkdataIn[NetworkdataInBExBTHB].reset_index(drop = True)

##################################################Internal Palo Alto########################################################################################################

NetworkdataInBPA = NetworkdataIn['Internal Location'] == "Palo Alto"
NetworkdataInPA = NetworkdataIn[NetworkdataInBPA].reset_index(drop = True)

#Create internal coms dataframe for Palo Alto for Business
NetworkdataInPAB1 = NetworkdataIn[(NetworkdataIn['Sender Team'] == "Business")  & (NetworkdataIn['Sender Location'] == "Palo Alto")]

#Create internal coms dataframe for Palo Alto for Analytics
NetworkdataInPAAB = NetworkdataIn['Sender Team'] == "Analytics"
NetworkdataInPAA = NetworkdataIn[NetworkdataInPAAB].reset_index(drop = True)

#Create internal coms dataframe for  Palo Alto for external coms between Business and other teams
NetworkdataInPAExPABB = NetworkdataIn['Internal / External Team Coms / Business unit'] == "PA External Business"
NetworkdataInPAExPAB = NetworkdataIn[NetworkdataInPAExPABB].reset_index(drop = True)

#Create internal coms dataframe for Palo Alto for external coms between Analytics and other teams
NetworkdataInPAExPAAB = NetworkdataIn['Internal / External Team Coms / Business unit'] == "PA External Analytics"
NetworkdataInPAExPAA = NetworkdataIn[NetworkdataInPAExPAAB].reset_index(drop = True)

##################################################External dataframes########################################################################################################

NetworkdataExB = Networkdata['Internal/External'] == "External"
NetworkdataEx = Networkdata[NetworkdataExB].reset_index(drop = True)

#Create external coms dataframe for Boston
NetworkdataExBB = NetworkdataEx['External Location'] == "Boston"
NetworkdataExB = NetworkdataEx[NetworkdataExBB].reset_index(drop = True)

#Create external coms dataframe for Boston for Business
NetworkdataExBB1 = NetworkdataEx[(NetworkdataEx['Sender Team'] == "Business")  & (NetworkdataEx['Sender Location'] == "Boston")]

#Create external coms dataframe for Boston for Tech DC
NetworkdataExBTDCB = NetworkdataEx['Sender Team'] == "Tech DC"
NetworkdataExBTDC = NetworkdataEx[NetworkdataExBTDCB].reset_index(drop = True)

#Create external coms dataframe for Boston for Tech HYPE
NetworkdataExBTHB = NetworkdataEx['Sender Team'] == "Tech HYPE"
NetworkdataExBTH = NetworkdataEx[NetworkdataExBTHB].reset_index(drop = True)

#Create external coms dataframe for Palo Alto
NetworkdataExBPA = NetworkdataEx['External Location'] == "Palo Alto"
NetworkdataExPA = NetworkdataEx[NetworkdataExBPA].reset_index(drop = True)

#Create external coms dataframe for Palo Alto for Business
NetworkdataExBPA1 = NetworkdataEx[(NetworkdataEx['Sender Team'] == "Business")  & (NetworkdataEx['Sender Location'] == "Palo Alto")]

#Create external coms dataframe for Palo Alto for Analytics
NetworkdataExPAAB = NetworkdataEx['Sender Team'] == "Analytics"
NetworkdataExPAA = NetworkdataEx[NetworkdataExPAAB].reset_index(drop = True)

#Create graphs for all dataframes
GraphIn = nx.from_pandas_edgelist(NetworkdataIn, "Sender", "Receiver", edge_attr = "Sum Weights", create_using = nx.DiGraph())                                            
GraphInB = nx.from_pandas_edgelist(NetworkdataInB, "Sender", "Receiver", edge_attr = "Sum Weights", create_using = nx.DiGraph())
GraphInBB = nx.from_pandas_edgelist(NetworkdataInBB1, "Sender", "Receiver", edge_attr = "Sum Weights", create_using = nx.DiGraph())
GraphInBTDC = nx.from_pandas_edgelist(NetworkdataInBTDC, "Sender", "Receiver", edge_attr = "Sum Weights", create_using = nx.DiGraph())
GraphInBTH = nx.from_pandas_edgelist(NetworkdataInBTH, "Sender", "Receiver", edge_attr = "Sum Weights", create_using = nx.DiGraph())
GraphInPA = nx.from_pandas_edgelist(NetworkdataInPA, "Sender", "Receiver", edge_attr = "Sum Weights", create_using = nx.DiGraph())  
GraphInPAB = nx.from_pandas_edgelist(NetworkdataInPAB1, "Sender", "Receiver", edge_attr = "Sum Weights", create_using = nx.DiGraph())  
GraphInPAA = nx.from_pandas_edgelist(NetworkdataInPAA, "Sender", "Receiver", edge_attr = "Sum Weights", create_using = nx.DiGraph())  
GraphInBExBB = nx.from_pandas_edgelist(NetworkdataInBExBB, "Sender", "Receiver", edge_attr = "Sum Weights", create_using = nx.DiGraph())
GraphInBExBTDC = nx.from_pandas_edgelist(NetworkdataInBExBTDC, "Sender", "Receiver", edge_attr = "Sum Weights", create_using = nx.DiGraph())
GraphInBExBTH = nx.from_pandas_edgelist(NetworkdataInBExBTH, "Sender", "Receiver", edge_attr = "Sum Weights", create_using = nx.DiGraph())
GraphInPAExPAB = nx.from_pandas_edgelist(NetworkdataInPAExPAB, "Sender", "Receiver", edge_attr = "Sum Weights", create_using = nx.DiGraph())
GraphInPAExPAA = nx.from_pandas_edgelist(NetworkdataInPAExPAA, "Sender", "Receiver", edge_attr = "Sum Weights", create_using = nx.DiGraph())

GraphEx = nx.from_pandas_edgelist(NetworkdataEx, "Sender", "Receiver", edge_attr = "Sum Weights", create_using = nx.DiGraph())                                            
GraphExB = nx.from_pandas_edgelist(NetworkdataExB, "Sender", "Receiver", edge_attr = "Sum Weights", create_using = nx.DiGraph())  
GraphExBB = nx.from_pandas_edgelist(NetworkdataExBB1, "Sender", "Receiver", edge_attr = "Sum Weights", create_using = nx.DiGraph())  
GraphExBTDC = nx.from_pandas_edgelist(NetworkdataExBTDC, "Sender", "Receiver", edge_attr = "Sum Weights", create_using = nx.DiGraph())  
GraphExBTH = nx.from_pandas_edgelist(NetworkdataExBTH, "Sender", "Receiver", edge_attr = "Sum Weights", create_using = nx.DiGraph())  
GraphExPA = nx.from_pandas_edgelist(NetworkdataExPA, "Sender", "Receiver", edge_attr = "Sum Weights", create_using = nx.DiGraph())                                            
GraphExPAB = nx.from_pandas_edgelist(NetworkdataExBPA1, "Sender", "Receiver", edge_attr = "Sum Weights", create_using = nx.DiGraph())                                            
GraphExPAA = nx.from_pandas_edgelist(NetworkdataExPAA, "Sender", "Receiver", edge_attr = "Sum Weights", create_using = nx.DiGraph())                                            

#Create extra graphs for use later
GraphInB1 = nx.from_pandas_edgelist(NetworkdataInB, "Sender", "Receiver", edge_attr = "Sum Weights", create_using = nx.DiGraph())                                            
GraphInB2 = nx.from_pandas_edgelist(NetworkdataInB, "Sender", "Receiver", edge_attr = "Sum Weights", create_using = nx.DiGraph())                                            
GraphInB3 = nx.from_pandas_edgelist(NetworkdataInB, "Sender", "Receiver", edge_attr = "Sum Weights", create_using = nx.DiGraph())                                            
GraphInPA1 = nx.from_pandas_edgelist(NetworkdataInPA, "Sender", "Receiver", edge_attr = "Sum Weights", create_using = nx.DiGraph())                                            
GraphInPA2 = nx.from_pandas_edgelist(NetworkdataInPA, "Sender", "Receiver", edge_attr = "Sum Weights", create_using = nx.DiGraph())                                            

#Tests
'''print ("Internal")
print (nx.info(GraphIn))
print ("External")
print(nx.info(GraphEx))
print ("InternalB")
print(nx.info(GraphInB))
print ("ExternalB")
print(nx.info(GraphExB))
print ("InternalPA")
print(nx.info(GraphInPA))
print ("ExternalPA")
print(nx.info(GraphExPA))'''

#Create dictionaries 
NodesUI = Nodes['UserID'].tolist()
NodesTeam = Nodes['Team'].tolist()
NodesLocation = Nodes['Location'].tolist()
NodesManager = Nodes['Manager?'].tolist()

DictTeam = dict(zip(NodesUI, NodesTeam))
DictLocation = dict(zip(NodesUI, NodesLocation))
DictManager = dict(zip(NodesUI, NodesManager))

#Add label information
#Internal
nx.set_node_attributes(GraphIn, DictTeam, 'Team')
nx.set_node_attributes(GraphIn, DictLocation, 'Location')
nx.set_node_attributes(GraphIn, DictManager, 'Manager?')

#External
nx.set_node_attributes(GraphEx, DictTeam, 'Team')
nx.set_node_attributes(GraphEx, DictLocation, 'Location')
nx.set_node_attributes(GraphEx, DictManager, 'Manager?')

#InternalB
nx.set_node_attributes(GraphInB, DictTeam, 'Team')
nx.set_node_attributes(GraphInB, DictLocation, 'Location')
nx.set_node_attributes(GraphInB, DictManager, 'Manager?')

#InternalPA
nx.set_node_attributes(GraphInPA, DictTeam, 'Team')
nx.set_node_attributes(GraphInPA, DictLocation, 'Location')
nx.set_node_attributes(GraphInPA, DictManager, 'Manager?')

#ExternalB
nx.set_node_attributes(GraphExB, DictTeam, 'Team')
nx.set_node_attributes(GraphExB, DictLocation, 'Location')
nx.set_node_attributes(GraphExB, DictManager, 'Manager?')

#ExternalPA
nx.set_node_attributes(GraphExPA, DictTeam, 'Team')
nx.set_node_attributes(GraphExPA, DictLocation, 'Location')
nx.set_node_attributes(GraphExPA, DictManager, 'Manager?')

#Save files
nx.write_gexf(GraphIn, 'GraphIn.gexf')
nx.write_gexf(GraphEx, 'GraphEx.gexf')
nx.write_gexf(GraphInB, 'GraphInB.gexf')
nx.write_gexf(GraphInPA, 'GraphInPA.gexf')
nx.write_gexf(GraphExB, 'GraphExB.gexf')
nx.write_gexf(GraphExPA, 'GraphExPA.gexf')

##################################################Analyses part one########################################################################################################

#Type of email
print ("Boston email type")
NetworkdataInL = Networkdata1[(Networkdata1['Internal/External'] == "Internal") & (Networkdata1['Sender Location'] == "Boston")]
NetworkdataInLN = NetworkdataInL.groupby(['Receiver Type'])['Count'].sum().to_frame('Sum Counts').reset_index() 
NetworkdataInLN["Percentage"] = NetworkdataInLN["Sum Counts"]/sum(NetworkdataInLN["Sum Counts"])
print (NetworkdataInLN)
print ("\n")

print ("Palo Alto email type")
NetworkdataInLPA = Networkdata1[(Networkdata1['Internal/External'] == "Internal") & (Networkdata1['Sender Location'] == "Palo Alto")]
NetworkdataInLNPA = NetworkdataInLPA.groupby([ 'Receiver Type'])['Count'].sum().to_frame('Sum Counts').reset_index() 
NetworkdataInLNPA["Percentage"] = NetworkdataInLNPA["Sum Counts"]/sum(NetworkdataInLNPA["Sum Counts"])
print (NetworkdataInLNPA)
print ("\n")

#Team of email
print ("Boston email team")
NetworkdataInT = Networkdata1[(Networkdata1['Internal/External'] == "Internal") & (Networkdata1['Sender Location'] == "Boston")]
NetworkdataInTN = NetworkdataInT.groupby([ 'Sender Team'])['Count'].sum().to_frame('Sum Counts').reset_index() 
NetworkdataInTN["Percentage"] = NetworkdataInTN["Sum Counts"]/sum(NetworkdataInTN["Sum Counts"])
NetworkdataInTN["Average"] = NetworkdataInTN["Sum Counts"]/[6,9,9]
print (NetworkdataInTN)
print ("\n")

print ("Palo Alto email team")
NetworkdataInTPA = Networkdata1[(Networkdata1['Internal/External'] == "Internal") & (Networkdata1['Sender Location'] == "Palo Alto")]
NetworkdataInTNPA = NetworkdataInTPA.groupby(['Sender Team'])['Count'].sum().to_frame('Sum Counts').reset_index() 
NetworkdataInTNPA["Percentage"] = NetworkdataInTNPA["Sum Counts"]/sum(NetworkdataInTNPA["Sum Counts"])
NetworkdataInTNPA["Average"] = NetworkdataInTNPA["Sum Counts"]/[10,4]
print (NetworkdataInTNPA)
print ("\n")

#Degrees
#Internal
degreeIn = GraphIn.degree(weight = "Sum Weights")
degreeInA = sum([x[1] for x in degreeIn]) / len([x[1] for x in degreeIn])
print("Network degree internal:", degreeInA)

#InternalB
degreeInB = GraphInB.degree(weight = "Sum Weights")
degreeInBA = sum([x[1] for x in degreeInB]) / len([x[1] for x in degreeInB])
print("Network degree internal B:", degreeInBA)

degreeInBB = GraphInBB.degree(weight = "Sum Weights")
degreeInBBA = sum([x[1] for x in degreeInBB]) / len([x[1] for x in degreeInBB])
print("Network degree internal B Business:", degreeInBBA)

degreeInBTDC = GraphInBTDC.degree(weight = "Sum Weights")
degreeInBTDCA = sum([x[1] for x in degreeInBTDC]) / len([x[1] for x in degreeInBTDC])
print("Network degree internal B Tech DC:", degreeInBTDCA)

degreeInBTH = GraphInBTH.degree(weight = "Sum Weights")
degreeInBTHA = sum([x[1] for x in degreeInBTH]) / len([x[1] for x in degreeInBTH])
print("Network degree internal B Tech H:", degreeInBTHA)

#InternalPA
degreeInPA = GraphInPA.degree(weight = "Sum Weights")
degreeInPAA1 = sum([x[1] for x in degreeInPA]) / len([x[1] for x in degreeInPA])
print("Network degree internal PA:", degreeInPAA1)

degreeInPAB = GraphInPAB.degree(weight = "Sum Weights")
degreeInPABA = sum([x[1] for x in degreeInPAB]) / len([x[1] for x in degreeInPAB])
print("Network degree internal PA Business:", degreeInPABA)

degreeInPAA = GraphInPAA.degree(weight = "Sum Weights")
degreeInPAAA = sum([x[1] for x in degreeInPAA]) / len([x[1] for x in degreeInPAA])
print("Network degree internal PA Analytics:", degreeInPAAA)

#External
degreeEx = GraphEx.out_degree(weight = "Sum Weights")
degreeExA = sum([x[1] for x in degreeEx]) / len([x[1] for x in degreeEx if x[1] != 0])
print("Network degree external:", degreeExA)

#ExternalB
degreeExB = GraphExB.out_degree(weight = "Sum Weights")
EdegreeExB = [(val, key) for (val, key) in degreeExB if key != 0]
degreeExBA = sum([x[1] for x in EdegreeExB]) / len([x[1] for x in EdegreeExB if x[1] != 0])
print("Network degree external B:", degreeExBA)

degreeExBB = GraphExBB.out_degree(weight = "Sum Weights")
EdegreeExBB = [(val, key) for (val, key) in degreeExBB if key != 0]
degreeExBBA = sum([x[1] for x in EdegreeExBB]) / len([x[1] for x in EdegreeExBB if x[1] != 0])
print("Network degree external B Business:", degreeExBBA)

degreeExBTDC = GraphExBTDC.out_degree(weight = "Sum Weights")
EdegreeExBTDC = [(val, key) for (val, key) in degreeExBTDC if key != 0]
degreeExBTDCA = sum([x[1] for x in EdegreeExBTDC]) / len([x[1] for x in EdegreeExBTDC if x[1] != 0])
print("Network degree external B Tech DC:", degreeExBTDCA)

degreeExBTH = GraphExBTH.out_degree(weight = "Sum Weights")
EdegreeExBTH = [(val, key) for (val, key) in degreeExBTH if key != 0]
degreeExBTHA = sum([x[1] for x in EdegreeExBTH]) / len([x[1] for x in EdegreeExBTH if x[1] != 0])
print("Network degree external B Tech H:", degreeExBTHA)

#ExternalPA
degreeExPA = GraphExPA.out_degree(weight = "Sum Weights")
EdegreeExPA = [(val, key) for (val, key) in degreeExPA if key != 0]
degreeExPAA1 = sum([x[1] for x in EdegreeExPA]) / len([x[1] for x in EdegreeExPA if x[1] != 0])
print("Network degree external PA:", degreeExPAA1)

degreeExPAB = GraphExPAB.out_degree(weight = "Sum Weights")
EdegreeExPAB = [(val, key) for (val, key) in degreeExPAB if key != 0]
degreeExPABA = sum([x[1] for x in EdegreeExPAB]) / len([x[1] for x in EdegreeExPAB if x[1] != 0])
print("Network degree external PA Business:", degreeExPABA)

degreeExPAA = GraphExPAA.out_degree(weight = "Sum Weights")
EdegreeExPAA = [(val, key) for (val, key) in degreeExPAA if key != 0]
degreeExPAAA = sum([x[1] for x in EdegreeExPAA]) / len([x[1] for x in EdegreeExPAA if x[1] != 0])
print("Network degree external PA Analytics:", degreeExPAAA)
print ("\n")

#Density measure
#Internal
densityIn = nx.density(GraphIn)
print("Network density internal:", densityIn)

#InternalB
densityInB = nx.density(GraphInB)
print("Network density internal B:", densityInB)

densityInBB = nx.density(GraphInBB)
print("Network density internal B Business:", densityInBB)

densityInBTDC = nx.density(GraphInBTDC)
print("Network density internal B Tech DC:", densityInBTDC)

densityInBTH = nx.density(GraphInBTH)
print("Network density internal B Tech H:", densityInBTH)

#InternalPA
densityInPA = nx.density(GraphInPA)
print("Network density internal PA:", densityInPA)

densityInPAB = nx.density(GraphInPAB)
print("Network density internal PA Business:", densityInPAB)

densityInPAA = nx.density(GraphInPAA)
print("Network density internal PA Analytics:", densityInPAA)

#External
densityEx = nx.density(GraphEx)
print("Network density external:", densityEx)

#ExternalB
densityExB = nx.density(GraphExB)
print("Network density external B:", densityExB)

densityExBB = nx.density(GraphExBB)
print("Network density external B Business:", densityExBB)

densityExBTDC = nx.density(GraphExBTDC)
print("Network density external B Tech DC:", densityExBTDC)

densityExBTH = nx.density(GraphExBTH)
print("Network density external B Tech Hype:", densityExBTH)

#ExternalPA
densityExPA = nx.density(GraphExPA)
print("Network density external PA:", densityExPA)

densityExPAB = nx.density(GraphExPAB)
print("Network density external PA Business:", densityExPAB)

densityExPAA = nx.density(GraphExPAA)
print("Network density external PA Analytics:", densityExPAA)

CCInBExBB = nx.density(GraphInBExBB)
print("Network density for Boston for external coms between Business and other teams:", CCInBExBB)

CCInBExBTDC = nx.density(GraphInBExBTDC)
print("Network density for Boston for external coms between Tech DC and other teams:", CCInBExBTDC)

CCInBExBTH = nx.density(GraphInBExBTH)
print("Network density for Boston for external coms between Tech HYPE and other teams:", CCInBExBTH)

CCInPAExPAB = nx.density(GraphInPAExPAB)
print("Network density for Palo Alto for external coms between Business and other teams:", CCInPAExPAB)

CCInPAExPAA = nx.density(GraphInPAExPAA)
print("Network density for Palo Alto for external coms between Analytics and other teams:", CCInPAExPAA)

#Internal density
#Remove nodes which are not from the team of intrest
GraphInPA1.remove_nodes_from([273033, 273034, 273038, 296638]) 
GraphInPA2.remove_nodes_from([281038, 286433, 286434, 286438, 292633, 292634, 292638, 94933, 94934, 94938])
GraphInB1.remove_nodes_from([174733,	 174734, 174738,	182838, 227533, 227534, 227538, 260334, 260338,      234033, 234034, 234038,	298033, 298034,	298038, 323233,	323234,323238])
GraphInB2.remove_nodes_from([234033,234034, 234038,	298033, 298034,	298038, 323233,	323234,323238, 174133,174134,174138,260833,	260838,53534])
GraphInB3.remove_nodes_from([174733,	174734,174738,182838,227533,227534, 227538, 260334, 260338,174133,174134,174138,260833,	260838,53534])

CCInPAAN = nx.density(GraphInPA1)
print("Network density for Palo Alto for internal coms between Analytics and other teams:", CCInPAAN)

CCInPAB = nx.density(GraphInPA2)
print("Network density for Palo Alto for internal coms between Business and other teams:", CCInPAB)

CCInBB = nx.density(GraphInB1)
print("Network density for Boston for internal coms between Business and other teams:", CCInBB)

CCInBTDC = nx.density(GraphInB2)
print("Network density for Boston for internal coms between Tech DC and other teams:", CCInBTDC)

CCInBTH = nx.density(GraphInB3)
print("Network density for Boston for internal coms between Tech HYPE and other teams:", CCInBTH)

#Histogram of degrees
histdegreeInB = [x[1] for x in degreeInB]
histdegreeInPA = [x[1] for x in degreeInPA]

sns.distplot(histdegreeInB, bins = 30,  norm_hist = True)
plt.title("Degree Distribution Boston")
plt.xlabel('Weighted Degrees')
plt.show()

sns.distplot(histdegreeInPA, bins = 30,  norm_hist = True)
plt.title("Degree Distribution Palo Alto")
plt.xlabel('Weighted Degrees')

plt.show()
print ("Std Internal Boston")
print (statistics.stdev(histdegreeInB))
print ("Std Internal Palo Alto")
print (statistics.stdev(histdegreeInPA))
print ("\n")

##################################################Managers########################################################################################################

#Type of email
print ("Boston email type managers")
NetworkdataInBM = Networkdata1[(Networkdata1['Sender Manager?'] == 1) & (Networkdata1['Internal/External'] == "Internal") & (Networkdata1['Sender Location'] == "Boston")]
NetworkdataInBMN = NetworkdataInBM.groupby(['Receiver Type'])['Count'].sum().to_frame('Sum Counts').reset_index() 
NetworkdataInBMN["Average"] =  NetworkdataInBMN["Sum Counts"]/6
NetworkdataInBMN["Percentage"] =  NetworkdataInBMN["Sum Counts"]/sum(NetworkdataInBMN["Sum Counts"])
print (NetworkdataInBMN)
print ("\n")

print ("Palo Alto email type managers")
NetworkdataInPAM = Networkdata1[(Networkdata1['Sender Manager?'] == 1) & (Networkdata1['Internal/External'] == "Internal") & (Networkdata1['Sender Location'] == "Palo Alto")]
NetworkdataInPAMN = NetworkdataInPAM.groupby(['Receiver Type'])['Count'].sum().to_frame('Sum Counts').reset_index() 
NetworkdataInPAMN["Average"] = NetworkdataInPAMN["Sum Counts"]/4
NetworkdataInPAMN["Percentage"] =  NetworkdataInPAMN["Sum Counts"]/sum(NetworkdataInPAMN["Sum Counts"])
print (NetworkdataInPAMN)
print ("\n")
#In and out degree for managers
B_Man = [174133, 174134, 227533, 260334, 298033, 298034]
PA_Man = [273033, 281038, 292638, 94933]

IndegreeInB = GraphInB.in_degree(weight = "Sum Weights")
OutdegreeInB = GraphInB.out_degree(weight = "Sum Weights")

DicIndegreeInB = dict(IndegreeInB)
DicOutdegreeInB = dict (OutdegreeInB)

ValIndegreeInB = [DicIndegreeInB[k] for k in B_Man if k in DicIndegreeInB]
ValOutdegreeInB = [DicOutdegreeInB[k] for k in B_Man if k in DicOutdegreeInB]

print ("Average indegreeB")
print (sum(ValIndegreeInB)/len(ValIndegreeInB))
print ("Average outdegreeB")
print (sum(ValOutdegreeInB)/len(ValOutdegreeInB))
print ("\n")

IndegreeInPA = GraphInPA.in_degree(weight = "Sum Weights")
OutdegreeInPA = GraphInPA.out_degree(weight = "Sum Weights")

DicIndegreeInPA = dict(IndegreeInPA)
DicOutdegreeInPA = dict (OutdegreeInPA)

ValIndegreeInPA = [DicIndegreeInPA[k] for k in PA_Man if k in DicIndegreeInPA]
ValOutdegreeInPA = [DicOutdegreeInPA[k] for k in PA_Man if k in DicOutdegreeInPA]

print ("Average indegreePA")
print (sum(ValIndegreeInPA)/len(ValIndegreeInPA))
print ("Average outdegreePA")
print (sum(ValOutdegreeInPA)/len(ValOutdegreeInPA))

#Closeness centrality
CCInB = nx.closeness_centrality(GraphInB)
ValCCInB = [CCInB[k] for k in B_Man if k in CCInB]
print (sum(ValCCInB)/len(ValCCInB))

CCInPA = nx.closeness_centrality(GraphInPA)
ValCCInPA = [CCInPA[k] for k in PA_Man if k in CCInPA]
print (sum(ValCCInPA)/len(ValCCInPA))
print ("\n")

##################################################Analyses part two########################################################################################################

#Type of email
print ("Boston External email type")
NetworkdataExL = Networkdata1[(Networkdata1['Internal/External'] == "External") & (Networkdata1['Sender Location'] == "Boston")]
NetworkdataExLN = NetworkdataExL.groupby(['Receiver Type'])['Count'].sum().to_frame('Sum Counts').reset_index() 
NetworkdataExLN["Percentage"] = NetworkdataExLN["Sum Counts"]/sum(NetworkdataExLN["Sum Counts"])
print (NetworkdataExLN)
print ("\n")

print ("Palo Alto External email type")
NetworkdataExLPA = Networkdata1[(Networkdata1['Internal/External'] == "External") & (Networkdata1['Sender Location'] == "Palo Alto")]
NetworkdataExLNPA = NetworkdataExLPA.groupby([ 'Receiver Type'])['Count'].sum().to_frame('Sum Counts').reset_index() 
NetworkdataExLNPA["Percentage"] = NetworkdataExLNPA["Sum Counts"]/sum(NetworkdataExLNPA["Sum Counts"])
print (NetworkdataExLNPA)
print ("\n")

#Team of email
print ("Boston External email team")
NetworkdataExT = Networkdata1[(Networkdata1['Internal/External'] == "External") & (Networkdata1['Sender Location'] == "Boston")]
NetworkdataExTN = NetworkdataExT.groupby([ 'Sender Team'])['Count'].sum().to_frame('Sum Counts').reset_index() 
NetworkdataExTN["Percentage"] = NetworkdataExTN["Sum Counts"]/sum(NetworkdataExTN["Sum Counts"])
NetworkdataExTN["Average"] = NetworkdataExTN["Sum Counts"]/[6,9,9]
print (NetworkdataExTN)
print ("\n")
print(NetworkdataExTN)

print ("Palo Alto External email team")
NetworkdataExTPA = Networkdata1[(Networkdata1['Internal/External'] == "External") & (Networkdata1['Sender Location'] == "Palo Alto")]
NetworkdataExTNPA = NetworkdataExTPA.groupby(['Sender Team'])['Count'].sum().to_frame('Sum Counts').reset_index() 
NetworkdataExTNPA["Percentage"] = NetworkdataExTNPA["Sum Counts"]/sum(NetworkdataExTNPA["Sum Counts"])
NetworkdataExTNPA["Average"] = NetworkdataExTNPA["Sum Counts"]/[10,4]
print (NetworkdataExTNPA)
print ("\n")

#Histogram of degrees
histdegreeExB = [x[1] for x in EdegreeExB]
histdegreeExPA = [x[1] for x in EdegreeExPA]

sns.distplot(histdegreeExB, bins = 40,  norm_hist = True)
plt.title("Degree Distribution Boston")
plt.xlabel('Weighted Degrees')
plt.show()

sns.distplot(histdegreeExPA, bins = 40,  norm_hist = True)
plt.title("Degree Distribution Palo Alto")
plt.xlabel('Weighted Degrees')

plt.show()

print ("Std External Boston")
print (statistics.stdev(histdegreeExB))
print ("Std External Palo Alto")
print (statistics.stdev(histdegreeExPA))
print ("\n")





