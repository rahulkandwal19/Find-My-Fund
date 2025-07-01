from flask import Flask, request, render_template
from flask_cors import CORS
from flask import jsonify
#--------------------------------------------------------------------------------
import numpy
import pandas
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier 
#--------------------------------------------------------------------------------
app = Flask(__name__)
CORS(app)
#--------------------------------------------------------------------------------
dataFrame = pandas.read_csv(r"MFData.csv") #Update Absolute Path to MFData.csv
data = dataFrame.copy()
mutualFund = "MUTUAL FUND "
typeMF = "Type"
riskLevel = "Risk"
mfReturn = "5Y Retuns"
minInvestment = "Minimum Investment"
minSIP = "Minimum Investment"
time = "LockIn Time"

dataFrame[minInvestment] = dataFrame[minInvestment]/50
dataFrame[minSIP] = dataFrame[minSIP]/10
dataFrame[mfReturn] = dataFrame[mfReturn]*4

uniqueTypes = dataFrame[typeMF].unique() 
typeEncoding = {'Debit':1,'Commodities':3,'Hybrid':2,'Equity':4}
dataFrame[typeMF]=dataFrame[typeMF].map(typeEncoding)
dataFrame[typeMF]=dataFrame[typeMF]*20
uniqueRiskLevels = dataFrame["Risk"].unique()
riskEncoding = {'Moderate':3,'High':5,'Low':1,'Moderate High':4,'Low Moderate':2,'Very High':6}
dataFrame['Risk'] = dataFrame['Risk'].map(riskEncoding)
dataFrame[riskLevel]=dataFrame[riskLevel]*20
features = dataFrame.drop(columns = ["MUTUAL FUND ","Objective","LockIn Time","Link"],axis=1)
target = dataFrame["MUTUAL FUND "]

knn = KNeighborsClassifier(n_neighbors=1) 
knn.fit(features,target) 
#--------------------------------------------------------------------------------
def inputEncoder(inputDataList,typeEncoding,riskEncoding):
    inputDataList[0] = typeEncoding[inputDataList[0]] 
    inputDataList[1] = riskEncoding[inputDataList[1]] 
    return inputDataList

def decodeResult(resultList,fundNames):
    result = []
    for value in resultList[0]:
        result.append(fundNames[value])
    return result
#--------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/getMutualFunds', methods=['GET'])
def getMutualFunds():
    inputType = request.args.get('type')
    inputRisk = request.args.get('risk')
    inputExpectedReturn = float(request.args.get('return'))*4
    inputMinInvestment = int(request.args.get('minInv'))/50
    inputMinSIP = int(request.args.get('minSIP'))/10
    inputObjective = request.args.get('obj')

    inputData = [inputType,inputRisk,inputExpectedReturn,inputMinInvestment,inputMinSIP]
    inputData = inputEncoder(inputData,typeEncoding,riskEncoding)

    inputData[0] = inputData[0]*20
    inputData[1] = inputData[1]*20
    inputData = pandas.DataFrame([inputData], columns= list(features.columns))

    predections = knn.kneighbors(inputData,n_neighbors=3,return_distance=False)
    predections = decodeResult(predections,dataFrame[mutualFund])
    print(predections)
    mfname1 = predections[0]
    mfname2 = predections[1]
    mfname3 = predections[2]

    mutualfund1 = {"name":mfname1,"data":data.loc[data[mutualFund] == mfname1].values.tolist()[0]}
    mutualfund2 = {"name":mfname2,"data":data.loc[data[mutualFund] == mfname2].values.tolist()[0]}
    mutualfund3 = {"name":mfname3,"data":data.loc[data[mutualFund] == mfname3].values.tolist()[0]}
    print(mutualfund1["data"])
    dataResult = {}
    dataResult["mf1Link"]=mutualfund1["data"][7]
    dataResult["mf1Return"]= mutualfund1["data"][3]
    dataResult["mf1MinInv"]= mutualfund1["data"][4]
    dataResult["mf1MinSIP"]= mutualfund1["data"][5]
    dataResult["mf1Name"] = mutualfund1["name"].replace("ICICI","")
    dataResult["mf1Type"] = mutualfund1["data"][1]
    dataResult["mf1Risk"]= mutualfund1["data"][2]
    dataResult["mf1Time"]= mutualfund1["data"][6]

    dataResult["mf2Link"]=mutualfund1["data"][7]
    dataResult["mf2Return"]= mutualfund2["data"][3]
    dataResult["mf2MinInv"]= mutualfund2["data"][4]
    dataResult["mf2MinSIP"]= mutualfund2["data"][5]
    dataResult["mf2Name"] = mutualfund2["name"].replace("ICICI","")
    dataResult["mf2Type"] = mutualfund2["data"][1]
    dataResult["mf2Risk"]= mutualfund2["data"][2]
    dataResult["mf2Time"]= mutualfund2["data"][6]

    dataResult["mf3Link"]=mutualfund1["data"][7]
    dataResult["mf3Return"]= mutualfund3["data"][3]
    dataResult["mf3MinInv"]= mutualfund3["data"][4]
    dataResult["mf3MinSIP"]= mutualfund3["data"][5]
    dataResult["mf3Name"] = mutualfund3["name"].replace("ICICI","")
    dataResult["mf3Type"] = mutualfund3["data"][1]
    dataResult["mf3Risk"]= mutualfund3["data"][2]
    dataResult["mf3Time"]= mutualfund3["data"][6]

    return render_template("result.html",**dataResult)

if __name__ == '__main__':
    app.run()
