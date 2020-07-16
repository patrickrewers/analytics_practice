# Import necessary libraries
import pandas as pd
from chembl_webresource_client.new_client import new_client

# Searching for coronavirus target in ChEMBL
target = new_client.target
target_query = target.search('coronavirus')
targets = pd.DataFrame.from_dict(target_query)
print(targets.columns.values)

