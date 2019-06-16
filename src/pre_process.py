import io
import sys
import csv
import jsonschema
import json
import datetime


def titleCase(st):
    return ' '.join(''.join([w[0].upper(), w[1:].lower()]) for w in st.split())


def fixEncoding(st):
    return st.replace('Â', '')

# Transform and convert the row into a form suitable for validation
# Note two transforms being applied: titleCase and fixEncoding
# The latter occurs in a field which is currently non-critical
# So its a quick and dirty attempt at fixing - not ideal
# as it looks like an upstream encoding problem that needs fixing
def map(row):
    return {
      "camis": int(row[0]),
      "dba": titleCase(row[1]),
      "boro": titleCase(row[2]),
      "building": titleCase(row[3]),
      "street": titleCase(row[4]),
      "zipcode": row[5],
      "phone": row[6],
      "cuisine_description": titleCase(row[7]),
      "inspection_date": row[8],
      "action": row[9],
      "violation_code": row[10],
      "violation_description": fixEncoding(row[11]),
      "critical_flag": row[12],
      "score": row[13],
      "grade": row[14],
      "grade_date": row[15],
      "record_date": row[16],
      "inspection_type": row[17]
    }

# Use Json Schema to validate the payload
def get_schema_validator():
    with open('schema/restaurant.json') as schema_file:
        in_schema = json.load(schema_file)
        return jsonschema.Draft4Validator(in_schema)


validator = get_schema_validator()


def validate(json_row):
    validation_errors = validator.iter_errors(json_row)
    valid = 1
    for schema_error in validation_errors:
        # We might well log some output here but it could get too verbose
        valid = 0
    return valid


def process(row):
    json_row = map(row)  # We can do some schema driven mapping here but I've left for now
    valid = validate(json_row)
    # We're going to do some downstream checks and filters
    json_row['valid'] = valid
    return json_row


def write(json_row, out_file):
    out_writer = csv.DictWriter(out_file, json_row.keys())
    out_writer.writerow(json_row)


def processFile(in_file_name, out_file_name):
    load_timestamp = datetime.datetime.now()

    with io.open(in_file_name, 'r', encoding='utf8') as in_file:
        with io.open(out_file_name, 'w', encoding='utf8') as out_file:
            csv_reader = csv.reader(in_file, delimiter=',')
            next(csv_reader, None)  # throw away the header
            line_no = 0
            for row in csv_reader:
                line_no += 1
                processed_row = process(row)
                # Include some lineage metadata
                processed_row['line_no'] = line_no
                processed_row['load_timestamp'] = load_timestamp
                write(processed_row, out_file)


processFile(sys.argv[1], sys.argv[2])
