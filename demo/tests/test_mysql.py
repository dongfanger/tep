def test(mysql_execute):
    sql = "select 1 from dual"
    cursor = mysql_execute(sql)
    column_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        print(row[column_names.index("1")])  # get by column name
