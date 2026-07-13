from database.DB_connect import DBConnect
from model.arco import Arco
from model.arco10 import Arco10
from model.arco2 import Arco2
from model.arco3 import Arco3
from model.arco5 import Arco5
from model.attore import Attore
from model.film import Film
from model.regista import Regista


class DAO():

    @staticmethod
    def getAllRatings():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct r.avg_rating as rating
                    from ratings r 
                    order by r.avg_rating asc"""

        cursor.execute(query)

        for row in cursor:
            results.append(row["rating"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(voto1, voto2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct n.*
from role_mapping rm , ratings r , movie m , names n 
where rm.movie_id = m.id and r.movie_id = m.id and rm.name_id =n.id 
and r.avg_rating between %s and %s
and N.date_of_birth is not NULL"""

        cursor.execute(query,(voto1, voto2))

        for row in cursor:
            results.append(Attore(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(idMapAttori, voto1, voto2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select rm1.name_id as id1, rm2.name_id as id2 , sum(cast(replace(replace(m.worlwide_gross_income,"$",""),",","")as unsigned)) as incasso
from role_mapping rm1, role_mapping rm2 , movie m, ratings r , names n1, names n2
where m.id = r.movie_id 
and rm1.movie_id = m.id and rm2.movie_id = m.id and r.avg_rating between %s and %s
and rm1.name_id = n1.id and rm2.name_id = n2.id and n1.date_of_birth is not null and n2.date_of_birth is not null
and rm1.movie_id = rm2.movie_id and rm1.name_id < rm2.name_id 
and m.worlwide_gross_income is not null
group by rm1.name_id , rm2.name_id"""

        cursor.execute(query,(voto1, voto2))

        for row in cursor:
            results.append(Arco(idMapAttori[row["id1"]],idMapAttori[row["id2"]], row["incasso"]))

        cursor.close()
        conn.close()
        return results


    #VERSIONE 2
    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct year(n.date_of_birth) as year
                    from names n 
                    where n.date_of_birth is not null
                    order by n.date_of_birth asc"""

        cursor.execute(query,)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getAllNodes2(annoDiNascita):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from names n 
                    where year(n.date_of_birth) > %s and n.date_of_birth is not null"""

        cursor.execute(query, (annoDiNascita,))

        for row in cursor:
            results.append(Attore(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges2(annoDiNascita, idMapAttori):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select rm.name_id as id1, rm2.name_id as id2 , count(*) as peso
        from role_mapping rm, role_mapping rm2, names n, names n2 
        where rm.movie_id = rm2.movie_id and rm.name_id < rm2.name_id and n.id = rm.name_id and n2.id = rm2.name_id 
        and year(n.date_of_birth) > %s and n.date_of_birth is not null and 
        year(n2.date_of_birth) > %s and n2.date_of_birth is not null 
        group by rm.name_id , rm2.name_id """

        cursor.execute(query, (annoDiNascita,annoDiNascita))

        for row in cursor:
            results.append(Arco2(idMapAttori[row["id1"]],idMapAttori[row["id2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results

    #VERSIONE3
    @staticmethod
    def getAllRatings2():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct R.avg_rating as rating
                from ratings r 
                order by R.avg_rating asc """

        cursor.execute(query, )

        for row in cursor:
            results.append(row["rating"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes3(rating):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select M.* 
from movie m, ratings r 
where M.id =R.movie_id and R.avg_rating > %s"""

        cursor.execute(query, (rating,))

        for row in cursor:
            results.append(Film(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges3(rating, idMapFilm):
        conn = DBConnect.get_connection()

        results = []
        #non mettere il group by perche i duplicati NON mi servono per calcolare il peso, in questo caso, ogni coppia mi serve SOLO 1 VOLTA
        cursor = conn.cursor(dictionary=True)
        query = """distinct select rm.movie_id as id1, rm2.movie_id as id2, abs(r.avg_rating - r2.avg_rating ) as peso
                from role_mapping rm , role_mapping rm2 ,movie m , movie m2 , ratings r , ratings r2 
                where rm.name_id = rm2.name_id and m.id=rm.movie_id and m2.id= rm2.movie_id and m.year < m2.year 
    and r.movie_id = m.id and r2.movie_id = m2.id and r.avg_rating > %s and r2.avg_rating > %s
"""

        cursor.execute(query, (rating, rating))

        for row in cursor:
            results.append(Arco3(idMapFilm[row["id1"]], idMapFilm[row["id2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results

        #VERSIONE 5
    @staticmethod
    def getAllNodes5(rating1, rating2):
            conn = DBConnect.get_connection()

            results = []
            # non mettere il group by perche i duplicati NON mi servono per calcolare il peso, in questo caso, ogni coppia mi serve SOLO 1 VOLTA
            cursor = conn.cursor(dictionary=True)
            query = """select n.*
from role_mapping rm , names n, ratings r , movie m 
where rm.movie_id = m.id and r.movie_id = m.id and rm.name_id =n.id and r.avg_rating between %s and %s
        """

            cursor.execute(query, (rating1, rating2))

            for row in cursor:
                results.append(Attore(**row))

            cursor.close()
            conn.close()
            return results

    @staticmethod
    def getAllEdges5(rating1, rating2, idMapAttori5):
        conn = DBConnect.get_connection()

        results = []
        # non mettere il group by perche i duplicati NON mi servono per calcolare il peso, in questo caso, ogni coppia mi serve SOLO 1 VOLTA
        cursor = conn.cursor(dictionary=True)
        query = """select rm.name_id as id1, rm2.name_id as id2, count(*) as peso
from role_mapping rm , role_mapping rm2 , movie m, ratings r , names n , names n2 
where rm.movie_id = rm2.movie_id and m.id =r.movie_id  and m.id =rm.movie_id and r.avg_rating between %s and %s
and n.id = rm.name_id and n2.id =rm2.name_id and n.date_of_birth < n2.date_of_birth and n.date_of_birth is not null 
and n2.date_of_birth is not null
group by  rm.name_id , rm2.name_id 
                """

        cursor.execute(query, (rating1, rating2))

        for row in cursor:
            results.append(Arco2(idMapAttori5[row["id1"]], idMapAttori5[row["id2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges5_V2(rating1, rating2, idMapAttori5):
        conn = DBConnect.get_connection()

        results = []
        # non mettere il group by perche i duplicati NON mi servono per calcolare il peso, in questo caso, ogni coppia mi serve SOLO 1 VOLTA
        cursor = conn.cursor(dictionary=True)
        query = """
select rm.name_id as id1 , rm2.name_id as id2, n.date_of_birth as db1, n2.date_of_birth as db2
from role_mapping rm , role_mapping rm2 , movie m, ratings r , names n , names n2 
where rm.movie_id = rm2.movie_id and m.id =r.movie_id  and m.id =rm.movie_id and r.avg_rating between %s and %s
and n.id = rm.name_id and n2.id =rm2.name_id and rm.name_id < rm2.name_id and n.date_of_birth is not null 
and n2.date_of_birth is not null
 
                """

        cursor.execute(query, (rating1, rating2))

        for row in cursor:
            results.append(Arco5(idMapAttori5[row["id1"]], idMapAttori5[row["id2"]], row["db1"], row["db2"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes5(rating1, rating2):
        conn = DBConnect.get_connection()

        results = []
        # non mettere il group by perche i duplicati NON mi servono per calcolare il peso, in questo caso, ogni coppia mi serve SOLO 1 VOLTA
        cursor = conn.cursor(dictionary=True)
        query = """select n.*
                   from role_mapping rm, \
                        names n, \
                        ratings r, \
                        movie m
                   where rm.movie_id = m.id \
                     and r.movie_id = m.id \
                     and rm.name_id = n.id \
                     and r.avg_rating between %s and %s \
                """

        cursor.execute(query, (rating1, rating2))

        for row in cursor:
            results.append(Attore(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges5(rating1, rating2, idMapAttori5):
        conn = DBConnect.get_connection()

        results = []
        # non mettere il group by perche i duplicati NON mi servono per calcolare il peso, in questo caso, ogni coppia mi serve SOLO 1 VOLTA
        cursor = conn.cursor(dictionary=True)
        query = """select rm.name_id as id1, rm2.name_id as id2, count(*) as peso
                   from role_mapping rm, \
                        role_mapping rm2, \
                        movie m, \
                        ratings r, \
                        names n, \
                        names n2
                   where rm.movie_id = rm2.movie_id \
                     and m.id = r.movie_id \
                     and m.id = rm.movie_id \
                     and r.avg_rating between %s and %s
                     and n.id = rm.name_id \
                     and n2.id = rm2.name_id \
                     and n.date_of_birth < n2.date_of_birth \
                     and n.date_of_birth is not null
                     and n2.date_of_birth is not null
                   group by rm.name_id, rm2.name_id \
                """

        cursor.execute(query, (rating1, rating2))

        for row in cursor:
            results.append(Arco2(idMapAttori5[row["id1"]], idMapAttori5[row["id2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges5_V2(rating1, rating2, idMapAttori5):
        conn = DBConnect.get_connection()

        results = []
        # non mettere il group by perche i duplicati NON mi servono per calcolare il peso, in questo caso, ogni coppia mi serve SOLO 1 VOLTA
        cursor = conn.cursor(dictionary=True)
        query = """
                select rm.name_id as id1, rm2.name_id as id2, n.date_of_birth as db1, n2.date_of_birth as db2
                from role_mapping rm, \
                     role_mapping rm2, \
                     movie m, \
                     ratings r, \
                     names n, \
                     names n2
                where rm.movie_id = rm2.movie_id \
                  and m.id = r.movie_id \
                  and m.id = rm.movie_id \
                  and r.avg_rating between %s and %s
                  and n.id = rm.name_id \
                  and n2.id = rm2.name_id \
                  and rm.name_id < rm2.name_id \
                  and n.date_of_birth is not null
                  and n2.date_of_birth is not null \

                """

        cursor.execute(query, (rating1, rating2))

        for row in cursor:
            results.append(Arco5(idMapAttori5[row["id1"]], idMapAttori5[row["id2"]], row["db1"], row["db2"]))

        cursor.close()
        conn.close()
        return results

    #VERSIONE 10
    @staticmethod
    def getAllNodes10(rating):
        conn = DBConnect.get_connection()

        results = []
        # non mettere il group by perche i duplicati NON mi servono per calcolare il peso, in questo caso, ogni coppia mi serve SOLO 1 VOLTA
        cursor = conn.cursor(dictionary=True)
        query = """select dm.name_id,n.name , n.height , n.date_of_birth , n.known_for_movies , avg(r.avg_rating) as avg_rating
from names n , director_mapping dm, movie m , ratings r 
where dm.name_id = n.id and m.id = dm.movie_id and r.movie_id = m.id and r.avg_rating > %s
group by dm.name_id,n.name , n.height , n.date_of_birth , n.known_for_movies """


        #select distinct n.* from names n , director_mapping dm, movie m , ratings r
        # where dm.name_id = n.id and m.id = dm.movie_id and r.movie_id = m.id and r.avg_rating > %s


        cursor.execute(query, (rating, ))

        for row in cursor:
            results.append(Regista(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges10(rating, idMapRegista):
        conn = DBConnect.get_connection()

        results = []
        # non mettere il group by perche i duplicati NON mi servono per calcolare il peso, in questo caso, ogni coppia mi serve SOLO 1 VOLTA
        cursor = conn.cursor(dictionary=True)
        query = """select dm.name_id as id1 , dm2.name_id as id2, count(distinct rm.name_id) as peso
from director_mapping dm , director_mapping dm2, role_mapping rm , role_mapping rm2, movie m, movie m2 , ratings r , ratings r2 
where rm.movie_id = dm.movie_id and rm2.movie_id = dm2.movie_id and rm.name_id = rm2.name_id 
and dm.movie_id = m.id and m.id = r.movie_id and r.avg_rating>%s
and dm2.movie_id = m2.id and m2.id = r2.movie_id and r2.avg_rating>%s and dm.name_id < dm2.name_id 
group by dm.name_id , dm2.name_id
                """

        cursor.execute(query, (rating,rating))

        for row in cursor:
            results.append(Arco10(idMapRegista[row["id1"]], idMapRegista[row["id2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results