def test(mysql_execute):
    sql = "select 1 from dual"
    ro = mysql_execute(sql)
    cursor = ro.cursor
    column_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        print(row[column_names.index("1")])  # get by column name
