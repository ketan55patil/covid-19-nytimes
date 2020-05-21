import requests
import mysql.connector
from mysql.connector import errorcode
import csv
# import datetime


class Covid19Nytime():

    def get_nytimes_csv(self):
        file_name = "us-counties.csv"
        url = f"https://raw.githubusercontent.com/nytimes/covid-19-data/master/{file_name}"

        response = requests.get(url, allow_redirects=True)
        if response.status_code == 200:
            print('Connection to URL was successful!')

            print('Writing contents to file...')
            with open(file_name, 'wb') as fw:
                fw.write(response.content)
        return True

    def read_nytimes_csv(self, file_name):
        with open(file_name, newline='') as csvfile:
            # spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            spamreader = csv.reader(csvfile)

            for row in spamreader:
                print(', '.join(row))

    def do_not_call_me(self):
        # max_date = "2020-04-28"

        # DB
        db_host = "127.0.0.1"
        db_user = "root"
        db_pass = "1234"
        db_name = "covid_19"
        db_table_name = "nytimes"

        try:
            cnx = mysql.connector.connect(user=db_user, password=db_pass,
                                          host=db_host,
                                          database=db_name)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

        cursor = cnx.cursor()
        query = f"SELECT max(date) as max_date_col from {db_table_name}"

        print("Reading max_date from the table")
        cursor.execute(query)

        for max_date_col in cursor:
            max_date = str(max_date_col[0])

        print('Closing cursor')
        cursor.close()
        # max_date = "2020-04-29"

        print(f"max_date is {max_date}")
        # print(f'max_date type is {type(max_date)}')
        sql_insert = f"INSERT INTO {db_table_name} (date, county, state, fips, cases, deaths) \
                       VALUES (%s, %s, %s, %s, %s, %s)"

        # if connection was successful with nytimes only then do the following
        if True:
            commit_required = False
            cursor = cnx.cursor()
            print(f'Reading file to get data where date is greater than max_date: {max_date}...')

            # row_count = 0
            with open(file_name, newline='') as csvfile:
                data = csv.reader(csvfile)
                for line in data:
                    date_col = line[0]

                    # print(f"max_date is None: {max_date == 'None'}")
                    # print(f'date_col > max_date: {date_col > max_date}')
                    # print(f'{max_date is None or date_col > max_date}')
                    # print(f"AND date_col != 'date' is {date_col != 'date'}")
                    #
                    # exit(0)

                    if (max_date == 'None' or date_col > max_date) and date_col != 'date':
                        county_col = line[1]
                        state_col = line[2]
                        fips_col = line[3] if line[3] != '' else 0
                        cases_col = line[4]
                        deaths_col = line[5]

                        row_list = (date_col, county_col, state_col, fips_col,
                                    cases_col, deaths_col)

                        print(f'Attempting to insert {row_list}...')
                        cursor.execute(sql_insert, row_list)

                        if not commit_required:
                            commit_required = True

        if commit_required:
            print('Committing insert...')
            cnx.commit()
        print('Closing cursor')
        cursor.close()
        print('Closing DB connection')
        cnx.close()

file_name = 'us-counties.csv'
my_obj = Covid19Nytime()
# my_obj.get_nytimes_csv()
# my_obj.read_nytimes_csv(file_name)
my_obj.do_not_call_me()
