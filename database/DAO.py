from database.DB_connect import DBConnect
from model.arco import Arco
from model.regista import Regista


class DAO():

        @staticmethod
        def getAllYears():
            conn = DBConnect.get_connection()

            results = []

            cursor = conn.cursor(dictionary=True)
            query = """
                    select distinct m.`year` as year
from movie m 
                    """

            cursor.execute(query)

            for row in cursor:
                results.append(row["year"])

            cursor.close()
            conn.close()
            return results

        @staticmethod
        def getAllRegisti(year):
            conn = DBConnect.get_connection()

            results = []

            cursor = conn.cursor(dictionary=True)
            query = """
                    select  n.id as id,n.name as name ,n.height as h , n.date_of_birth as db , n.known_for_movies as kn, count(*) as numFilmDiretti ,avg(r.avg_rating) as ratingMedio
from director_mapping dm , movie m , names n , ratings r 
where dm.movie_id = m.id and year(m.date_published)  = %s and dm.name_id = n.id and r.movie_id =m.id
group by n.id 
                    """

            cursor.execute(query,(year,))

            for row in cursor:
                results.append(Regista(row["id"], row["name"], row["h"], row["db"], row["kn"], row["numFilmDiretti"], row["ratingMedio"]))

            cursor.close()
            conn.close()
            return results

        #Esiste un arco tra due registi R1 e R2 se hanno diretto almeno un film appartenente ad almeno un genere comune.
        # Il peso dell'arco è:
        # numeroFilmComuniGenere ×(mediaRating(R1)+mediaRating(R2))
        # dove: numeroFilmComuniGenere = numero di coppie di film dei due registi che condividono almeno un genere -> COPPIE = DISTINCT MOVIE1, MOVIE2

        @staticmethod
        def getAllEdges(year, idMapRegisti):
            conn = DBConnect.get_connection()

            results = []

            cursor = conn.cursor(dictionary=True)
            query = """
                   select dm.name_id as id1 , dm2.name_id as id2, count(distinct dm.movie_id, dm2.movie_id) as numFilmGenereComune
from director_mapping dm , director_mapping dm2 , movie m , movie m2 , genre g , genre g2 
where dm.movie_id = m.id and m.id = g.movie_id and m.year = %s
and  dm2.movie_id = m2.id and m2.id = g2.movie_id and m2.`year` = %s
and g.genre = g2.genre and dm.name_id < dm2.name_id 
group by dm.name_id, dm2.name_id 
                    """

            cursor.execute(query, (year,year))

            for row in cursor:
                results.append(Arco(idMapRegisti[row["id1"]], idMapRegisti[row["id2"]], row["numFilmGenereComune"]))

            cursor.close()
            conn.close()
            return results


