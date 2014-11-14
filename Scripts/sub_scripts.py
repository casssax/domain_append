import csv
import sys

def pie_tableau_db_file(db_file_name):
    with open(db_file_name, 'r') as db_file:
        print 'Creating PIE database append file'
        delim_type = ','
        data = csv.reader(db_file, delimiter=str(delim_type))
        data = [row for row in data]
        small_data = []
        for i in data:
            small_data.append([i[0].lower(),i[5].lower()])
        return (small_data)

def company_lookup(data,firm_data):
    ##print 'data: ', data
    data = data.lower()
    domains = [i[1] for i in firm_data if i[0] == data]
    #domain = next((i[1] for i in firm_data if i[0] == data), None)
    for domain in domains:
        if domain not in isp_list:
            return domain
            break
        #else:
            #print 'bad: ', domain

def email_lookup(data,email_data):
    pos = data.find('@')
    email = data[pos + 1:]
    if email in email_data:
        if email in esp_list:
            return None
        else:
            return email
    return None

def pick_domain(e_domain,c_domain):
    if e_domain != None:
        return e_domain
    elif c_domain != None:
        return c_domain
    else:
        return None 


def append_firm_domain(input_file, out_file):
    # db_file_name will be the permanent name of file pulled from PIE database for Tableau.
    #     this name should always be the same and new files will overwrite the old file. 
    db_file_name = '\\\\192.168.1.179\\firmographics\\LSC-Firmagraphic-Database.csv'
    # create the firmographic file. 
    firm_data = pie_tableau_db_file(db_file_name)
    email_data = [i[1] for i in firm_data]
    print 'firm_file created'
    delim_type = ','
    data = csv.reader(input_file, delimiter=str(delim_type))
    header_flag = 1
    added_field_list = ['Selected_Domain']
    supp_list = []
    for csvdata in data:
        listdata = list(csvdata)
        if header_flag == 1:
            file_header = listdata
            new_line = ''
            for header_field in file_header:
                new_line = new_line + '"' + header_field + '"' + ','
            for added_fields in added_field_list:
                new_line = new_line + '"' + added_fields + '"' + ','
            out_file.write(new_line[:-1] + '\n')
            header_flag = 0
        else:
            new_line = ''
            c_domain = None
            e_domain = None
            c_domain = company_lookup(listdata[9],firm_data)
            e_domain = email_lookup(listdata[8],email_data)
            ##print 'company: ', c_domain, 'email: ', e_domain
            out_domain = pick_domain(e_domain,c_domain)
            ##print 'out_domain: ', out_domain
            for field in listdata:
                new_line = new_line + '"' + field + '"' + ',' 
            new_line = new_line + '"' + str(out_domain) + '"' + ',' 
            new_line = new_line[:-1] + '\n'
            out_file.write(new_line)

# get isp/esp junk lists
esp_list = [line.strip() for line in open("\\\\192.168.1.179\\firmographics\\ESP Suppression List.csv", 'r')]
isp_list = [line.strip() for line in open("\\\\192.168.1.179\\firmographics\\ISP Suppression List 10-23-14.Csv", 'r')]

# fname = 'test.csv'
# file_ext = '.out'
# with open(fname, 'r') as input_file, open(fname + file_ext, 'w') as out_file:
#     append_tableau_file(input_file, out_file)