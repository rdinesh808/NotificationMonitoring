from dateutil.relativedelta import relativedelta
import mysql.connector
import HtmlTestRunner
import datetime
import unittest
import json

class dbconnection(unittest.TestCase):
  def test_getconnection(self):
      with open('../JSONFile/Environment-Variables.json') as env_data:
          env_details = json.load(env_data)

          mydb = mysql.connector.connect(
              host=env_details["host"],
              user=env_details["user"],
              passwd=env_details["passwd"]
          )


          mycursor = mydb.cursor()
          mycursor.execute("SELECT v.notification_subscription_id,c.application_name,c.application_id,c.notification_endpoint,v.status FROM gsialerting.notification_subscription v LEFT JOIN connect.application c ON v.application_id = c.application_id WHERE v.status='ENABLED' AND v.community_id="+env_details["com_id"]+" AND c.community_id="+env_details["com_id"]+";")
          output = mycursor.fetchall()
          notification_endpoint = []
          subscription_id = []
          application_name = []

          for i in range(len(output)):
              subscription_id.append(output[i][0])
              application_name.append(output[i][1])
              notification_endpoint.append(output[i][3])

          q = notification_endpoint
          t = subscription_id
          an = application_name

          mycursor = mydb.cursor()
          mycursor.execute("SELECT v.notification_subscription_id,v.NOTIFICATION_TYPE_ID,c.NOTIFICATION_NAME FROM gsialerting.notification_subscription v LEFT JOIN gsialerting.notification_type c on v.NOTIFICATION_TYPE_ID = c.NOTIFICATION_TYPE_ID WHERE v.community_id="+env_details["com_id"]+" AND v.status='ENABLED';")
          output1 = mycursor.fetchall()
          notification_name = []

          for notify_name in range(len(output1)):
              notification_name.append(output1[notify_name][2])

          names = notification_name


          a = datetime.datetime.now().date()  # Current Date
          b = datetime.datetime.now().date() + relativedelta(months=-3)  # Minus Three months

          print("<h5><b>COMMUNITY_ID : </b>" + env_details["com_id"] + "</br>" + "<b>HOSTNAME : </b>" + env_details["host"] + "</br>" + "<b>USERNAME : </b>dinesh.netaji</h5>")
          print("<h4>Notification Audit Monitoring <b>'" + str(b) + "'</b> to <b>'" + str(a) + "'</b></h4>")
          print("<table border='1' cellspacing='2'>")
          print("<tr><th><b><font color='blue'>Subscripition_ID</font></b></th><th><div align='center'><b><font color='blue'>Application_Name</font></b></div></th><th><div align='center'><b><font color='blue'>Notification_Name</font></b></div></th><th><div align='center'><b><font color='blue'>Notification_End_Point</font></b></div></th><th><b><font color='blue'>SUCCESS</font></b></th><th><b><font color='blue'>FAILURE</font></b></th><th><b><font color='blue'>NULL</font></b></th><th><b><font color='blue'>TOTAL</font></b></th></tr>")
          for j in range(len(q)):
              mycursor.execute("SELECT COUNT(DISPOSITION) FROM gsialerting.notification_audit WHERE creation_date_time BETWEEN '" + str(b) + "' AND '" + str(a) + "' AND NOTIFICATION_SUBSCRIPTION_ID = " + str(t[j]) + " AND ENDPOINT = '" + q[j] + "' AND DISPOSITION='SUCCESS';")
              output_1 = mycursor.fetchall()
              disposition = []
              for k in range(len(output_1)):
                  disposition.append(output_1[k][0])
              r = disposition
              r1 = 0
              for x in r:
                  r1 += x


                  for l in range(len(q)):
                      mycursor.execute("SELECT COUNT(DISPOSITION) FROM gsialerting.notification_audit WHERE creation_date_time BETWEEN '" + str(b) + "' AND '" + str(a) + "' AND NOTIFICATION_SUBSCRIPTION_ID = " + str(t[j]) + " AND ENDPOINT = '" + q[j] + "' AND DISPOSITION='FAILURE';")
                      output_1 = mycursor.fetchall()
                      disposition = []
                      for k in range(len(output_1)):
                          disposition.append(output_1[k][0])
                      r = disposition
                      r2 = 0
                      for y in r:
                          r2 += y

                          for m in range(len(q)):
                              mycursor.execute("SELECT COUNT(*) FROM gsialerting.notification_audit WHERE creation_date_time BETWEEN '" + str(b) + "' AND '" + str(a) + "' AND NOTIFICATION_SUBSCRIPTION_ID = " + str(t[j]) + " AND ENDPOINT = '" + q[j] + "' AND ISNULL(DISPOSITION);")
                              output_1 = mycursor.fetchall()
                              disposition = []
                              for k in range(len(output_1)):
                                  disposition.append(output_1[k][0])
                              r = disposition
                              r3 = 0
                              for z in r:
                                  r3 += z

              n = r1 + r2 + r3
              print("<tr><td align='center'><b><font color='black'>"+str(t[j])+"</font></b></td><td align='center'><b><font color='black'>"+an[j]+"</font></b></td><td align='center'><b><font color='black'>"+names[j]+"</font></b></td><td><b><font color='black'>"+q[j]+"</font></b></td><td align='center'><b><font color='black'>"+str(r1)+"</font></b></td><td align='center'><b><font color='black'>"+str(r2)+"</font></b></td><td align='center'><b><font color='black'>"+str(r3)+"</font></b></td><td align='center'><b><font color='black'>"+str(n)+"</font></b></td></tr>")
          print("</table>")

if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output="../Report",combine_reports=True,report_name="Notification_EndPoint_Verification",report_title="Notification_EndPoint_Disposition_Value"))
