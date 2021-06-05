## Guidance Hack

## Import libraries

import mysql.connector
from getpass import getpass
import pandas as pd

# Connect to database

passw = getpass('Enter your password')
cnx = mysql.connector.connect(user = "root", password = passw,host="localhost",database="jobs_interviews")
cnx.is_connected()

cursor = cnx.cursor()
cursor

def queries_execute(x):
    cursor.execute(x)
    queries_result = cursor.fetchall()
    return queries_result

def job_search():
    #first lets show courses possibilities:
    courses_possibilites = queries_execute("""SELECT DISTINCT Course FROM jobs_interviews.jobs;""")
    options = pd.DataFrame(courses_possibilites)
    print(options)
    course_choice = int(input('Choose your course:'))
    while course_choice not in range(int(options.shape[0])):
        print('Please try again')
        course_choice = int(input('Choose your course:'))
    course = options.loc[course_choice,0]
    
    #second lets show locations possibilities:
    locations_possibilites = queries_execute("""SELECT DISTINCT Country FROM jobs_interviews.jobs;""")
    options1 = pd.DataFrame(locations_possibilites)
    print(options1)
    location_choice = int(input('Choose your location:'))
    while location_choice not in range(int(options1.shape[0])):
        print('Please try again')
        location_choice = int(input('Choose your course:'))

    location = options1.loc[location_choice,0]
    
    #your jobs possibilities
    your_jobs = queries_execute("""SELECT Course,Job,Company,Link,City,Country FROM jobs_interviews.jobs WHERE ((Course = '"""+course+"""') & (Country = '"""+location+"""'));""")
    job_option = pd.DataFrame(your_jobs, columns=['Course','Job','Company','Link','City','Country'])
    print(job_option)

    #lets choose your perfect job
    application_choice = int(input('Choose the job you want to apply:'))
    while application_choice not in range(int(job_option.shape[0])):
        print('Please try again')
        application_choice = int(input('Choose the job you want to apply:'))

    the_job = job_option.iloc[application_choice]
    the_job = pd.Series(the_job, index=['Course','Job','Company','Link','City','Country'])
    print(the_job)
    return the_job


def interview_prep():
    #first get the job information
    job_choice = job_search()
    job_area = job_choice.iloc[0]
    job_location = job_choice.iloc[5]

    #your preparation
    your_questions = queries_execute("""SELECT job_company,questions,answers FROM jobs_interviews.interviews WHERE ((country = '"""+job_location+"""') & (area = '"""+job_area+"""'));""")
    prep_option = pd.DataFrame(your_questions, columns=['job_company','questions','answers'])
    print(prep_option)

    #read a specific question
    spec_question = (input('Do you want to see specific question? Y/N:')).lower()
    while spec_question != 'n':
        if spec_question == 'y':
            question_choice = int(input('Choose the question you want to read:'))
            while question_choice not in range(int(prep_option.shape[0])):
                print('Please try again')
                question_choice = int(input('Choose the question you want to read:'))
            quest = prep_option.at[question_choice,'questions']
            print(quest)
            spec_question = (input('Do you want to see another question? Y/N:')).lower()
        
        else:
            spec_question = (input('You option is not possible. Do you want to see another question? Y/N:')).lower()

    if spec_question == 'n':
        print('Lets get the job!!')


interview_prep()
