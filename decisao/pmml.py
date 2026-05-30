import pandas as pd
from sqlalchemy import create_engine
from os import environ 
from dotenv import load_dotenv

from pypmml import Model
from sys import argv

def get_uri():
    uri = ''
    load_dotenv()
    
    passwrd = environ.get("MYSQL_ROOT_PASSWORD")
    host    = environ.get("MYSQL_HOST")
    db      = environ.get("MYSQL_DATABASE")

    uri = "mysql+pymysql://root:" + passwrd + '@' + host + '/' + db
    return uri

def main():
    
    if (len(argv) < 2):
        print("USO: pyhton3 pmml.py <modelo.pmml>")
        return 0

    uri = get_uri()
    engine = create_engine(uri)

    query = "SELECT * FROM data"
    result = pd.read_sql(query, engine)

    indict = result.groupby('id').apply(lambda x: x.to_dict("records")).to_dict() 

    final = list()
    for i in indict:
        indict[i][0].pop("id")
        final.append(indict[i])        


    print(argv[1])
    model = Model.load(argv[1])
  
    # print(f"Campos de entrada: {model.inputFields}")
    # print(f"Campos de saída: {model.outputFields}")



    resultado = model.predict(final)
    print(resultado)

if __name__ == "__main__":
    main()
