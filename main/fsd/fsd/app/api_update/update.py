import sqlite3


def update(source_db, source_table, target_db, target_table, target_fields=None):
    """Keep two tables up to date.
    ASSUMES TARGET TABLE SHOULD HAVE DISTINCT ROWS!!!

    Args:
        source_db (string): path
        source_table (string): name of table
        target_db (string): path
        target_table (string): name of table
        target_fields (list, optional): list of fields in target table. Defaults to None.
    """
    conn = sqlite3.connect(source_db)
    c = conn.cursor()
    c.execute("ATTACH DATABASE '" + target_db + "' AS db2")
    try:
        # Try to create the target table as a copy of source table,
        # will fail if the target table already exists

        if target_fields:
            query_str = (
                "CREATE TABLE db2."
                + target_table
                + " AS SELECT DISTINCT "
                + ",".join(target_fields)
                + " FROM "
                + source_table
            )
            c.execute(query_str)
        else:
            c.execute(
                "CREATE TABLE db2."
                + target_table
                + " AS SELECT DISTINCT * FROM "
                + source_table
            )
        conn.commit()
        conn.close()
        return

    except sqlite3.OperationalError:
        # If the target table already exists, clear it and reload from source table
        c.execute("DELETE FROM db2." + target_table)

        if target_fields:
            query_str = (
                "INSERT INTO db2."
                + target_table
                + " ("
                + ",".join(target_fields)
                + ")"
                + " SELECT DISTINCT "
                + ",".join(target_fields)
                + " FROM "
                + source_table
            )
            c.execute(query_str)
        else:
            c.execute(
                "INSERT INTO db2."
                + target_table
                + " SELECT DISTINCT * FROM "
                + source_table
            )

        conn.commit()
        conn.close()