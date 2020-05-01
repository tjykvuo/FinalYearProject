import os
import io
import csv 
from django.core.exceptions import ValidationError

REQUIRED_HEADER = ['username' ,'password']

def csv_file_validator_function(value):
    filename, ext = os.path.splittext(value.name)
    if str(ext) != '.csv':
        raise ValidationError("csv file required")
    decoded_file = value.read().decode('utf-8')
    io_string = io.StringIO(decoded_file)
    reader = csv.reader(io_string, delimiter=';', quotechar='|')
    header_= next(reader)[0].split(',')
    if header_[-1] == '':
        header.pop()
    required_header = REQUIRED_HEADER
    if required_header != header_:
        raise ValidationError("File is invalid. Please use a valid CSV (Comma-Seperated Values) Header")
