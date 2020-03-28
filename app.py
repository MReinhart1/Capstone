from flask import Flask, render_template, url_for, flash, redirect, request
from forms import *
from flask_mysqldb import MySQL
import yaml
import csv, os


app = Flask(__name__)

# Configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['SECRET_KEY'] = os.urandom(24)


#All routing
mysql = MySQL(app)
@app.route('/')
def index():
    return render_template("/home.html")

@app.route('/home.html', methods=['GET', 'POST',  'PUT'])
def home():
    return render_template('home.html')


@app.route('/time.html', methods=['GET', 'POST',  'PUT'])
def timeFunction():
    form = userTime()
    return render_template('time.html')


@app.route('/addUser.html', methods=['GET', 'POST',  'PUT'])
def userFunction():
    form = makeNewUser()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        if (form.rateType.data == "Academic"):
            rate = 33
        else:
            rate = 22
        permissionString = ""
        if(form.perMac1.data == True):
            permissionString += "1"
        else:
            permissionString += "0"

        if(form.perMac2.data == True):
            permissionString += "1"
        else:
            permissionString += "0"

        if(form.perMac3.data == True):
            permissionString += "1"
        else:
            permissionString += "0"

        if(form.perMac4.data == True):
            permissionString += "1"
        else:
            permissionString += "0"

        if(form.perMac5.data == True):
            permissionString += "1"
        else:
            permissionString += "0"

        if(form.perMac6.data == True):
            permissionString += "1"
        else:
            permissionString += "0"

        if(form.perMac7.data == True):
            permissionString += "1"
        else:
            permissionString += "0"
        cur.execute("INSERT INTO users(username, supervisor, department, faculty, institution, rateType, Permissions) VALUES(%s, %s, %s, %s, %s, %s, %s)",([form.userName.data, form.supervisor.data, form.department.data, form.faculty.data, form.institution.data,rate, permissionString]))
        mysql.connection.commit()
        cur.close()
        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT * FROM users")
        if resultValue > 0:
            userDetails = cur.fetchall()
        return render_template('addUser.html',
        form=form ,
        data=form.userName.data,
        mac1=form.perMac1.data,
        mac2=form.perMac2.data,
        mac3=form.perMac3.data,
        mac4=form.perMac4.data,
        mac5=form.perMac5.data,
        mac6=form.perMac6.data,
        mac7=form.perMac7.data,
        userDetails=userDetails)
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('addUser.html', form=form , data="", userDetails=userDetails)
    return render_template('addUser.html', form=form , data="")

@app.route('/configure.html', methods=['GET', 'POST',  'PUT'])
def configure():
    superForm = newSupervisor()
    deptForm = newDepartment()
    facultyForm = newFaculty()
    institutionForm = newInstitution()
    rateForm = newRateType()
    if request.method == "POST":
        try :
            request.form['superName']
            cur = mysql.connection.cursor()
            superName = superForm.superName.data
            cur.execute("INSERT INTO supervisors (superName) VALUES (%s)", ([superName]))
            mysql.connection.commit()
            cur.close()
            return redirect("/configure.html")
        except:
            pass
        try:
            request.form['deptName']
            cur = mysql.connection.cursor()
            deptName = deptForm.deptName.data
            cur.execute("INSERT INTO departments (deptName) VALUES (%s)", ([deptName]))
            mysql.connection.commit()
            cur.close()
            return redirect("/configure.html")
        except:
            pass
        try:
            request.form['facultyName']
            cur = mysql.connection.cursor()
            facultyName = facultyForm.facultyName.data
            cur.execute("INSERT INTO faculty (facultyName) VALUES (%s)", ([facultyName]))
            mysql.connection.commit()
            cur.close()
            return redirect("/configure.html")
        except:
            pass
        try:
            request.form['institutionName']
            cur = mysql.connection.cursor()
            institutionName = institutionForm.institutionName.data
            cur.execute("INSERT INTO institution (institutionName) VALUES (%s)", ([institutionName]))
            mysql.connection.commit()
            cur.close()
            return redirect("/configure.html")
        except:
            pass
        try:
            request.form['rateTypeName']
            cur = mysql.connection.cursor()
            rateTypeName = rateForm.rateTypeName.data
            rateAmount = rateForm.rateAmount.data
            cur.execute("INSERT INTO rateType (rateName, rateAmount) VALUES (%s, %s)", ([rateTypeName, rateAmount]))
            mysql.connection.commit()
            cur.close()
            return redirect("/configure.html")
        except:
            pass


    cur = mysql.connection.cursor()
    supers = cur.execute("SELECT * FROM supervisors")
    supers = cur.fetchall()
    dept = cur.execute("SELECT * FROM departments")
    dept = cur.fetchall()
    faculty = cur.execute("SELECT * FROM faculty")
    faculty = cur.fetchall()
    institution = cur.execute("SELECT * FROM institution")
    institution = cur.fetchall()
    rate = cur.execute("SELECT * FROM rateType")
    rate = cur.fetchall()
    return render_template("/configure.html",
    supers=supers,
    dept=dept,faculty=faculty,institution=institution,rate=rate,
    superForm=superForm, deptForm=deptForm, facultyForm=facultyForm,
    institutionForm=institutionForm,rateForm=rateForm )



@app.route('/dataEdit.html', methods=['GET', 'POST',  'PUT'])
def dataEditFunction():
    return render_template('dataEdit.html')


@app.route('/reports.html', methods=['GET', 'POST',  'PUT'])
def reportFunction():
    makeDatabase()
    return render_template('reports.html')


@app.route('/logout.html')
def logout():
    return render_template('logout.html')


#All functions to delete things such as users, supers, institutions
@app.route('/deleteUser/<string:userIdentificationNumber>')
def deleteUser(userIdentificationNumber):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users where userID=" + str(userIdentificationNumber))
    mysql.connection.commit()
    cur.close()
    form = makeNewUser()
    return redirect("/addUser.html")


@app.route('/deleteSuper/<string:superIdentificationNumber>')
def deleteSuper(superIdentificationNumber):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM supervisors where superID=" + str(superIdentificationNumber))
    mysql.connection.commit()
    cur.close()
    return redirect("/configure.html")


@app.route('/deleteDepartment/<string:deptIdentificationNumber>')
def deleteDepartment(deptIdentificationNumber):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM departments where deptID=" + str(deptIdentificationNumber))
    mysql.connection.commit()
    cur.close()
    return redirect("/configure.html")

@app.route('/deleteFaculty/<string:facultyIdentificationNumber>')
def deleteFaculty(facultyIdentificationNumber):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM faculty where facultyID=" + str(facultyIdentificationNumber))
    mysql.connection.commit()
    cur.close()
    return redirect("/configure.html")

@app.route('/deleteInstitution/<string:institutionIdentificationNumber>')
def deleteInstitution(institutionIdentificationNumber):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM institution where institutionID=" + str(institutionIdentificationNumber))
    mysql.connection.commit()
    cur.close()
    return redirect("/configure.html")

@app.route('/deleteRate/<string:rateIdentificationNumber>')
def deleteRate(rateIdentificationNumber):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM rateType where rateID=" + str(rateIdentificationNumber))
    mysql.connection.commit()
    cur.close()
    return redirect("/configure.html")


def writeCSV(tableList):
    writer = csv.writer(open("out.csv", 'w'))
    for line in tableList:
        writer.writerow(line)

def makeDatabase():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("CREATE TABLE people (PersonID int)")
        mysql.connection.commit()
        cur.close()
