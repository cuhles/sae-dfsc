import os
from pandas import read_csv, read_excel, DataFrame
import sae
import gurobipy as gp
from gurobipy import GRB
import numpy as np

import sys
sys.path.append('../')
import saedfsc

# directory path
SAE_DFSCdir: str = os.path.dirname(__file__)

# read data into dataframes
suppliers: DataFrame = read_csv(SAE_DFSCdir + "/resources/suppliers.csv")
customers: DataFrame = read_csv(SAE_DFSCdir + "/resources/customers.csv")

seed = 1

def getPartsDataFromWithRandomSuppliers(df):
    num_rows = df.shape[0]
    #random_suppliers = np.random.choice(suppliers['Name'], num_rows)
    random_suppliers = [np.random.choice(suppliers['Name'], size = np.random.randint(low=1, high=4), replace=False) for _ in range(num_rows)]
    df['Suppliers'] = random_suppliers
    return df

def getPartOptionsWithSuppliers():
    parts = {}
    samples = 20
    np.random.seed(seed)

    wingparts = getPartsDataFromWithRandomSuppliers(sae.materials.merge(sae.wings, how='cross').sample(n=samples, random_state=seed))
    parts['wings'] = wingparts
    #parts['frontwing'] = wingparts
    #parts['sidewing'] = wingparts

    tireOptions = getPartsDataFromWithRandomSuppliers(sae.pressure.merge(sae.tires, how='cross'))
    parts['tires'] = tireOptions
    #parts['fronttire'] = tireOptions

    parts['engine'] = getPartsDataFromWithRandomSuppliers(sae.motors)
    parts['cabin'] = getPartsDataFromWithRandomSuppliers(sae.materials.merge(sae.cabins, how='cross').sample(n=samples, random_state=seed))
    parts['impactattenuator'] = getPartsDataFromWithRandomSuppliers(sae.materials.merge(sae.attenuators, how='cross').sample(n=samples, random_state=seed))
    parts['brakes'] = getPartsDataFromWithRandomSuppliers(sae.brakes)

    suspensionParts = getPartsDataFromWithRandomSuppliers(sae.suspension)
    parts['suspension'] = suspensionParts
    #parts['frontsuspension'] = suspensionParts
    return parts
