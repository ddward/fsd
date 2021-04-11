import os
import sqlite3
import unittest

from update import update


class TestDatabaseUpdate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        # Create Test Databases
        sqlite3.connect("test_reciever.db")
        conn = sqlite3.connect("test_sender.db")
        c = conn.cursor()
        c.execute(
            """CREATE TABLE test_sender_table (
            test_col int,
            test_col_2 int
            )"""
        )
        for i in range(5):
            c.execute("INSERT INTO test_sender_table VALUES (?, ?)", (i, 5))
        conn.commit()

    def test_update_full(self):
        conn = sqlite3.connect("test_sender.db")
        c = conn.cursor()
        c.execute("select * from test_sender_table")
        conn.commit()
        table_first = c.fetchall()

        conn = sqlite3.connect("test_reciever.db")
        c = conn.cursor()
        c.execute(
            """CREATE TABLE test_reciever_table (
            test_col int,
            test_col_2 int
            )"""
        )
        conn.commit()

        update(
            "test_sender.db",
            "test_sender_table",
            "test_reciever.db",
            "test_reciever_table",
        )
        c.execute("select * from test_reciever_table")
        table_copied = c.fetchall()

        self.assertEqual(table_first, table_first)

    def test_update_partial(self):
        conn = sqlite3.connect("test_sender.db")
        c = conn.cursor()
        c.execute("SELECT test_col FROM test_sender_table")
        table_first = c.fetchall()

        conn = sqlite3.connect("test_reciever.db")
        c = conn.cursor()
        c.execute(
            """CREATE TABLE test_reciever_table_2 (
            test_col int
            )"""
        )
        conn.commit()
        update(
            "test_sender.db",
            "test_sender_table",
            "test_reciever.db",
            "test_reciever_table_2",
            ["test_col"],
        )
        c.execute("select * from test_reciever_table")
        table_copied = c.fetchall()

        self.assertEqual(table_first, table_first)

    @classmethod
    def tearDownClass(cls):

        # Destroy Test Databases
        os.remove("test_sender.db")
        os.remove("test_reciever.db")


if __name__ == "__main__":
    unittest.main()