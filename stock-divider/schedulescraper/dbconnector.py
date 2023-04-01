from mysql import connector as mc

class Connector(object):
    def __init__(self, config):
        self.host = config["db_host"]
        self.user = config["db_user"]
        self.pswd = config["db_pswd"]
        self.name = config["db_name"]

    def find(self, sql, params=None):
        with mc.connect(host=self.host, user=self.user, password=self.pswd, database=self.name) as connection:
            cursor = connection.cursor()
            cursor.execute(sql, params)
            return cursor.fetchall()
    
    def save(self, sql, params):
        with mc.connect(host=self.host, user=self.user, password=self.pswd, database=self.name) as connection:
            cursor = connection.cursor()
            cursor.execute(sql, params)
            cursor.close()
            connection.commit()

class SymbolsConnector(Connector):
    def __init__(self, config):
        super().__init__(config)

    def find_all(self):
        sql = """
            SELECT
                symbol_code,
                right_last_date,
                ratio,
                status
            FROM
                symbol_divide_info
        """
        rows = super().find(sql)
        return [{
            "symbol_code": row[0],
            "right_last_date": row[1],
            "ratio": row[2],
            "status": row[3]
        } for row in rows]
    
    def find_by_status(self, status):
        sql = """
            SELECT
                symbol_code,
                right_last_date,
                ratio,
                status
            FROM
                symbol_divide_info
            WHERE
                status = %s
        """
        rows = super().find(sql, params=(status,))
        return [{
            "symbol_code": row[0],
            "right_last_date": row[1],
            "ratio": row[2],
            "status": row[3]
        } for row in rows]

    def save_one(self, symbol):
        sql = """
            INSERT INTO symbol_divide_info (
                symbol_code,
                right_last_date,
                ratio,
                status
            ) VALUES (
                %s, %s, %s, %s
            ) ON DUPLICATE KEY UPDATE
                ratio = VALUES(ratio),
                status = VALUES(status)
        """
        super().save(sql, params=(
            symbol["symbol_code"],
            symbol["right_last_date"],
            symbol["ratio"],
            symbol["status"] if "status" in symbol else "0"
        ))

    def apply_divide(self, divide):
        sql = """
            UPDATE symbol_daily_info SET
                first_opening_price = first_opening_price / %s,
                first_high_price = first_high_price / %s,
                first_low_price = first_low_price / %s,
                first_closing_price = first_closing_price / %s,
                latter_opening_price = latter_opening_price / %s,
                latter_high_price = latter_high_price / %s,
                latter_low_price = latter_low_price / %s,
                latter_closing_price = latter_closing_price / %s
            WHERE
                symbol_code = %s
            AND
                opening_date <= %s
        """
        super().save(sql, params=(
            divide["ratio"],
            divide["ratio"],
            divide["ratio"],
            divide["ratio"],
            divide["ratio"],
            divide["ratio"],
            divide["ratio"],
            divide["ratio"],
            divide["symbol_code"],
            divide["right_last_date"]
        ))
