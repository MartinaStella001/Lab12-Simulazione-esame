from database.DB_connect import DBConnect
from model.arco import Arco
from model.film import Film


class DAO():
    @staticmethod
    def getAllFilm(voto):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select  m.id as id, m.title as title, m.`year` as y , m.date_published as dp, m.duration as d , 
                    m.country as c , m.worlwide_gross_income as wg
                        , m.languages as l , m.production_company as pc, count(distinct g.genre) as numGeneri, r.avg_rating  as ratingMedio 
from movie m , ratings r , genre g 
where m.id = r.movie_id and r.total_votes >= %s and m.id = g.movie_id 
group by m.id 
                """

        cursor.execute(query,(voto,))

        for row in cursor:
            results.append(Film(row["id"],row["title"], row["y"], row["dp"], row["d"], row["c"],
                                row["wg"], row["l"],row["pc"],row["numGeneri"],row["ratingMedio"]))

        cursor.close()
        conn.close()
        return results


    #Esiste un arco tra F1 e F2 se:condividono almeno un genere, hanno almeno un attore in comune
    # Peso:
    # peso = (numero attori comuni) + (numero generi comuni) -> QUI LE COPPIE SAREBBERO genere1-genere1 (uguali) -> allora usare DISTINCT genere1

    @staticmethod
    def getAllEdges(voto, idMapFilm):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
              select t1.movie_id as id1, t2.movie_id as id2, count(distinct t1.genre ) as numGeneriComune, count(distinct t1.name_id) as numAttoriComuni
from(select g.genre, rm.name_id, rm.movie_id
from role_mapping rm , movie m , genre g 
where rm.movie_id = m.id and g.movie_id = m.id) t1, (select g.genre, rm.name_id,rm.movie_id
from role_mapping rm , movie m , genre g 
where rm.movie_id = m.id and g.movie_id = m.id) t2, ratings r, ratings r2
where t1.name_id = t2.name_id and t1.genre = t2.genre and t1.movie_id < t2.movie_id and t1.movie_id = r.movie_id and r.total_votes >= %s
and t2.movie_id = r2.movie_id and r2.total_votes >= %s
group by t1.movie_id, t2.movie_id

                """

        cursor.execute(query, (voto,voto))

        for row in cursor:
            results.append(Arco(idMapFilm[row["id1"]], idMapFilm[row["id2"]], row["numGeneriComune"], row["numAttoriComuni"]))

        cursor.close()
        conn.close()
        return results





