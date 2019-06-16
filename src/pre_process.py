import io
import sys
import csv
import jsonschema
import json
import datetime
import logging


# Util function for fixing case, python str.title() is not that good!
def titleCase(st):
    return ' '.join(''.join([w[0].upper(), w[1:].lower()]) for w in st.split())


# See encoding note beow
def fixEncoding(st):
    return st.replace('Â', '')


# Transform and convert the row into a form suitable for validation
# Note two transforms being applied: titleCase and fixEncoding
# The latter occurs in a field which is currently non-critical
# So its a quick and dirty attempt at fixing - not ideal
# as it looks like an upstream encoding problem that needs fixing
def map(row):
    logging.debug('Entering map(row)')
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
    logging.info('Entering validate(json_row)')
    with open('schema/restaurant.json') as schema_file:
        in_schema = json.load(schema_file)
        return jsonschema.Draft4Validator(in_schema)


validator = get_schema_validator()


# Check for any schema validation errors
# note the schema is first pass only at present
def validate(json_row):
    logging.debug('Entering validate(json_row)')
    validation_errors = validator.iter_errors(json_row)
    valid = 1
    for schema_error in validation_errors:
        # We could log some output here but it could get too verbose
        valid = 0
    return valid


# The core processing sequence for a row of CSV style data
def process(row):
    logging.debug('Entering process(row)')
    json_row = map(row)  # Refactor: Schema driven mapping
    valid = validate(json_row)
    # We're going to do some downstream checks and filters based upon this
    json_row['valid'] = valid
    return json_row


def write(json_row, out_file):
    logging.debug('Entering write(json_row, out_file)')
    out_writer = csv.DictWriter(out_file, json_row.keys())
    out_writer.writerow(json_row)


# Entry point. Takes an input CSV file and generates a validated
# CSV output file with lineage metadata
# Note a JSON output would be better, but the dowstream postgres
# load step is tied to CSV
# Other target backends would be better with JSON records.
# Most bulk inserts require a proprietrary format however.
def processFile(in_file_name, out_file_name):
    logging.info('Entering processFile')
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


if __name__ == '__main__':
    processFile(sys.argv[1], sys.argv[2])
