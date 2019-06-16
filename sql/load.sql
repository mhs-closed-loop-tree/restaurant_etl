TRUNCATE TABLE restaurant;

INSERT INTO restaurant
WITH latest_grades AS (SELECT
FIRST_VALUE ( camis   )  OVER ( PARTITION BY camis ORDER BY grade_date DESC, grade DESC ) as camis,
FIRST_VALUE ( dba     )  OVER ( PARTITION BY camis ORDER BY grade_date DESC, grade DESC ) as dba,
FIRST_VALUE ( boro    )  OVER ( PARTITION BY camis ORDER BY grade_date DESC, grade DESC ) as boro,
FIRST_VALUE ( building )  OVER ( PARTITION BY camis ORDER BY grade_date DESC, grade DESC ) as building,
FIRST_VALUE ( street  )  OVER ( PARTITION BY camis ORDER BY grade_date DESC, grade DESC ) as street,
FIRST_VALUE ( zipcode )  OVER ( PARTITION BY camis ORDER BY grade_date DESC, grade DESC ) as zipcode,
FIRST_VALUE ( phone   )  OVER ( PARTITION BY camis ORDER BY grade_date DESC, grade DESC ) as phone,
FIRST_VALUE ( cuisine_description )  OVER ( PARTITION BY camis ORDER BY grade_date DESC, grade DESC ) as cuisine_description,
FIRST_VALUE ( grade )    OVER ( PARTITION BY camis ORDER BY grade_date DESC, grade DESC ) as grade,
FIRST_VALUE ( line_no )  OVER ( PARTITION BY camis ORDER BY grade_date DESC, grade DESC ) as line_no,
FIRST_VALUE ( load_timestamp ) OVER ( PARTITION BY camis ORDER BY grade_date DESC, grade DESC ) as load_timestamp
FROM restaurant__staging 
WHERE grade is not null
AND valid = 1
)
SELECT DISTINCT camis, dba,boro, building, street, zipcode, phone, cuisine_description, grade, line_no, load_timestamp FROM latest_grades
