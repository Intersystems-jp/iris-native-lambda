Class Test.Utils
{

/// Lambda関数から呼び出すときは、以下入力引数に指定します。
/// { 
///   "method": "Hello",
///   "args":"none"
/// }
ClassMethod Hello() As %String
{
   Set tVersion = $ZV
   if ( tVersion '="" ) { set tSC = $$$OK }

   Set jsonret = {}
   set jsonret.message="こんにちは！只今の日付時刻は："_$ZDATETIME($HOROLOG,16)_"です"
   Set jsonret.status = $$$OK
   Set jsonret.payload = tVersion

   Quit jsonret.%ToJSON()
}

ClassMethod GetPerson() As %String
{
   set sql="select JSON_OBJECT('Name':Name,'Email': Email) as json from Test.Person"
   set stmt=##class(%SQL.Statement).%New()
   set st=stmt.%Prepare(sql)
   set rset=stmt.%Execute()
   set array=[]
   while rset.%Next() {
      set rjson={}.%FromJSON(rset.%Get("json"))
      do array.%Push(rjson)
   }
   return array.%ToJSON()
}

ClassMethod CreateDummyTbl() As %String
{
   &sql(create table Test.Person(Name VARCHAR(50),Email VARCHAR(50)))
   &sql(INSERT INTO Test.Person (Name,Email) VALUES('山田','taro@mail.com'))
   &sql(INSERT INTO Test.Person (Name,Email) VALUES('斉藤','saito@mail.com'))
   set json={}
   set json.Message="登録完了"
   return json.%ToJSON()
}

ClassMethod CreateDummyGlo() As %String
{
   set ^KION("久留米","min")=14
   set ^KION("久留米","max")=19

   set ^KION("大阪","min")=12
   set ^KION("大阪","max")=18

   set ^KION("東京","min")=14
   set ^KION("東京","max")=19

   set ^KION("愛知","min")=13
   set ^KION("愛知","max")=15

   set ^KION("奈良","min")=10
   set ^KION("奈良","max")=18

   set ^KION("沖縄","min")=21
   set ^KION("沖縄","max")=26

   set ^KION("新潟","min")=6
   set ^KION("新潟","max")=12
   set json={}
   set json.Message="登録完了"
   return json.%ToJSON()
}

}
