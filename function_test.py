import os
import pandas as pd
import numpy as np
import json

fica_loc = os.path.join('data','fica_tax.json')
income_tax_loc = os.path.join('data','income_tax.json')

fica_dict = json.loads(open(fica_loc).read())
income_tax_dict = json.loads(open(income_tax_loc).read())

print(fica_dict)
print(income_tax_dict)