from xml.sax.saxutils import quoteattr
from sklearn.metrics import cohen_kappa_score
import xml.etree.ElementTree as ET

import pandas as pd


def getAgreement():

    Mapping= pd.read_csv('Final.csv')
    Mapping=Mapping.drop_duplicates(subset=['Class_Name_1', 'Class_Name_2'], keep='first').reset_index(drop=True)
    df1=pd.read_csv('gold_standard_mapping2.csv')
    df2=pd.read_csv('gold_standard_mapping3.csv')

    s1 = pd.merge(df1, df2, how='inner', on=['Class_Name_1', 'Class_Name_2'])
    #print(s1.head())
    L1=s1['Relation_y'].to_list()
    L2=df1['Relation'].to_list()
    L3=df2['Relation'].to_list()
    print(cohen_kappa_score(L1, L2, L3))

def get_file_header():
    return """<?xml version=\"1.0\" encoding=\"utf-8\"?>
    <rdf:RDF xmlns="http://knowledgeweb.semanticweb.org/heterogeneity/alignment"
      xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
      xmlns:xsd="http://www.w3.org/2001/XMLSchema#">
<Alignment>
  <xml>yes</xml>
  <level>0</level>
  <type>??</type>"""

def get_mapping_format(source, target, measure):
    relation= '='
    return """
  <map>
    <Cell>
      <entity1 rdf:resource=%s/>
      <entity2 rdf:resource=%s/>
      <relation>%s</relation>
      <measure rdf:datatype="xsd:float">%.1f</measure>
    </Cell>
  </map>""" %(quoteattr(source), quoteattr(target), relation, float(measure))
#(quoteattr(source), quoteattr(target), relation, measure)

def _get_file_footer():
    return """
  </Alignment>
</rdf:RDF>
"""

def writeAlignments(file, df):
    #df=pd.read_csv(alignments)
    #df=df.drop_duplicates(subset=['Class_Name_1', 'Class_Name_2'], keep='first')

    with open(file, 'w', encoding='utf-8') as Myfile:
        Myfile.write(get_file_header())
        for i in range(len(df)):
            if df.loc[i,'Relation'] == '1':
                Myfile.write(get_mapping_format(df.loc[i,'URI_1'], df.loc[i,'URI_2'], df.loc[i,'Relation']))
            else:
                pass
        Myfile.write(_get_file_footer())




def main():
    FilePath ='reference.xml'
    Alignment ='Final.csv'
    df = pd.read_csv(Alignment)
    df= df.drop_duplicates(subset=['Class_Name_1', 'Class_Name_2'], keep='first').reset_index(drop=True)
    #print(df)
    writeAlignments(FilePath, df)
    #getAgreement()
if __name__ == "__main__":
    main()