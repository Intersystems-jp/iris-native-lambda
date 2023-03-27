import irisnative
import json
import time
import os


def lambda_handler(event, context):
    
    # Retrieve connection information from configuration file
    #connection_detail = get_connection_info("connection.config")

    #ip = connection_detail["ip"]
    #port = int(connection_detail["port"])
    #namespace = connection_detail["namespace"]
    #username = connection_detail["username"]
    #password = connection_detail["password"]

    # Overrides for Portal
    ip = os.environ.get('IRISHOST')
    port = int(os.environ.get('IRISPORT'))
    namespace = os.environ.get('NAMESPACE')
    username = os.environ.get('USERNAME')
    password = os.environ.get('PASSWORD')
    
    print("ip: " + ip)
    print("port: " + str(port))
    print("namespace: " + namespace)
    print("username: " + username)
    print("password: " + password)


    # Create connection to InterSystems IRIS
    connection = irisnative.createConnection(ip, port, namespace, username, password)

    print("Connected to InterSystems IRIS")

    # Create an iris object
    iris_native = irisnative.createIris(connection)

    # Managed wrapper class, hard-coded right now for sanity
    classname = "Test.Utils"
    returnvalue = ""

    '''
    # 以下実行例です。
    # *** 使用しないパラメータにはnoneを指定してください。****
    # TestlUtilsクラスのHello()メソッドを実行する場合
    {
      "method": "Hello",
      "function":"none",
      "args": "none"
    }
    
    # Test.Personテーブルの作成とダミーデータの登録する例
    # TestlUtilsクラスのCreateDummyTbl()メソッドを実行する場合
    {
      "method": "CreateDummyTbl",
      "function":"none",      
      "args": "none"
    }
    
    # Test.PersonテーブルのSELECTの結果を取得する例
    # Test.UtilsクラスのGetPetPerson()メソッド実行する場合
    {
      "method": "GetPerson",
      "function":"none",
      "args": "none"
    }
    
    # ^KIONグローバル変数を設定する例
    # Test.UtilsクラスのCreateDummyGlo()メソッドを実行する場合
    {
      "method": "CreateDummyGlo",
      "function":"none",
      "args": "none"
    }

    # index.pyのFunctionを動かす例
    # ^KION全データ取得する get_globaldataを実行する例
    {
      "method":"none",
      "function":"getglobal",
      "args":"none"
    }
    
    # index.pyのFunctionを動かす例
    # ^KIONにデータを追加する例
    {
      "method":"none",
      "function": "setglobal",
      "args": {"area":"長野","min":5,"max":10}
    }
    '''
    method = event['method']
    function = event['function']
    args = event['args']


    if (method=="none") and (function == "getglobal"):
        returnvalue = get_globaldata("KION",iris_native)
    elif (method=="none") and (function == "setglobal"):
        returnvalue = set_kiondata(args,iris_native)
    elif (function=="none") and (args == "none"):
      returnvalue = iris_native.classMethodValue(classname,method)
    else:
      returnvalue = iris_native.classMethodValue(classname,method,args)

    connection.close()
    return returnvalue
    
    
def get_connection_info(file_name):
    # Initial empty dictionary to store connection details
    connections = {}

    # Open config file to get connection info
    with open(file_name) as f:
        lines = f.readlines()
        for line in lines:
            # remove all white space (space, tab, new line)
            line = ''.join(line.split())

            # get connection info
            connection_param, connection_value = line.split(":")
            connections[connection_param] = connection_value
    
    return connections

def get_globaldata(glo,iris_native):
    kion=[]
    ite1=iris_native.iterator(glo)
    for area in ite1.subscripts():
        areakion=[]
        ite2=iris_native.iterator(glo,area)
        areakion=[area,iris_native.get(glo,area,"min"),iris_native.get(glo,area,"max")]
        kion.append(areakion)
    print(kion)
    returnjson=json.dumps(kion,ensure_ascii=False)
    return returnjson
    
def set_kiondata(args,iris_native):
    # ^KION(area,"min")
    # ^KION(area,"max")
    # args={"area":"x","min":12,"max":20}
    #
    iris_native.set(args["min"],"KION",args["area"],"min")
    iris_native.set(args["max"],"KION",args["area"],"max")
    retval='{"Status":"OK","Message":"グローバル設定完了"}'
    returnjson=json.dumps(retval,ensure_ascii=False)
    return returnjson