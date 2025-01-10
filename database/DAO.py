from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_years():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select DISTINCT YEAR(datetime) as year
                        from sighting s 
                        order by year"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["year"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_states_year(anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT s.*
                        FROM new_ufo_sightings.state as s, new_ufo_sightings.sighting as a
                        WHERE s.id = a.state AND YEAR(datetime) = %s
                        GROUP BY s.id
                        ORDER BY Name"""
            cursor.execute(query, (anno,))

            for row in cursor:
                result.append(State(row["id"],
                                      row["Name"],
                                      row["Capital"],
                                      row["Lat"],
                                      row["Lng"],
                                      row["Area"],
                                      row["Population"],
                                      row["Neighbors"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_avvistamenti(year, state):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s1.id as id1, s2.id as id2
                    FROM new_ufo_sightings.sighting as s1, new_ufo_sightings.sighting as s2
                    WHERE YEAR(s1.datetime)= %s
                    AND YEAR(s1.datetime)=YEAR(s2.`datetime`)
                    AND s1.state = %s
                    AND s1.state = s2.state
                    AND s1.shape = s2.shape
                    AND s1.id < s2.id"""
            cursor.execute(query, (year, state,))

            for row in cursor:
                result.append((row["id1"], row["id2"]))
            cursor.close()
            cnx.close()
        return result

