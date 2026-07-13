from database.DB_connect import DBConnect
from model.arco import Arco
from model.attore import Attore


class DAO():

    @staticmethod
    def getAllGeneri():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct g.genre  as genere
from genre g 
order by g.genre asc 
                """

        cursor.execute(query)

        for row in cursor:
            results.append(row["genere"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllAttori(genere):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select  n.id as id1 , n.name as n , n.height as h, n.date_of_birth as db , n.known_for_movies as kn ,count(*) as numFilmGenere, avg(r.avg_rating) as ratingMedio
from role_mapping rm,movie m , genre g , names n , ratings r 
where rm.movie_id = m.id and m.id = g.movie_id and g.genre = %s and rm.name_id = n.id and r.movie_id = m.id 
group by n.id
                """

        cursor.execute(query,(genere,))

        for row in cursor:
            results.append(Attore(row["id1"],row["n"],row["h"], row["db"],
                                  row["kn"], row["numFilmGenere"], row["ratingMedio"]))

        cursor.close()
        conn.close()
        return results

    #Esiste un arco A1 → A2 se:
    # hanno recitato insieme in almeno un film del genere scelto
    # ratingMedio(A1) > ratingMedio(A2)
    # In caso di parità si inseriscono due archi.
    # Peso:
    # numeroFilmInComune ×|ratingMedio(A1)-ratingMedio(A2)|

    @staticmethod
    def getAllEdges(genere, idMapAttori):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
             select rm.name_id as attore1, rm2.name_id as attore2, count(*) as numFilmComune
from role_mapping rm , role_mapping rm2, movie m, genre g 
where rm.movie_id = rm2.movie_id and rm.movie_id = m.id and m.id = g.movie_id and g.genre = %s
and rm.name_id < rm2.name_id
group by rm.name_id , rm2.name_id

                """

        cursor.execute(query,(genere,))

        for row in cursor:
            results.append(Arco(idMapAttori[row["attore1"]],idMapAttori[row["attore2"]], row["numFilmComune"]))

        cursor.close()
        conn.close()
        return results