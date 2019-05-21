import pickle
from sqlite_conn import SqliteConn
import pprint

DB_PATH = 'Chinook_Sqlite.sqlite'


def execute_query(query_string):
    """Executes query and returns data from data base"""
    with SqliteConn(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query_string)
        data = cursor.fetchall()
        return data


def first_query():
    query_string = '''
        SELECT DISTINCT c.FirstName || ' ' || c.LastName AS Name, c.Phone as Phone
        FROM Invoice as i
        INNER JOIN Customer as c on c.CustomerId = i.CustomerId
        INNER JOIN (
            SELECT City, count(City) as customersCount
            FROM Customer
            GROUP BY City
            HAVING customersCount > 1
        ) as cCount on cCount.City = c.City
    '''
    return execute_query(query_string)


def second_query():
    query_string = '''
        SELECT c.City, round(sum(i.Total), 2) as TotalSum
        FROM Invoice as i
        LEFT JOIN Customer as c on c.CustomerId = i.CustomerId
        GROUP BY c.City
        ORDER BY TotalSum DESC
        LIMIT 3       
    '''

    return execute_query(query_string)


def third_query():
    query_string = '''
        SELECT gtop.Name as Genre, t.Name as Track, alb.Title as Album, art.Name as Artist
        FROM Track as t
        INNER JOIN (
            SELECT g.GenreId, g.Name, sum(il.Quantity) as Quantity
            FROM InvoiceLine as il
            INNER JOIN Track as t on t.TrackId = il.TrackId
            INNER JOIN Genre as g on g.GenreId = t.GenreId
            GROUP BY g.GenreId
            ORDER  BY Quantity DESC
            LIMIT 1     
        ) as gtop on gtop.GenreId = t.GenreId
        LEFT JOIN Album as alb on alb.AlbumId = t.AlbumId
        LEFT JOIN Artist as art on art.ArtistId = alb.ArtistId
        ORDER BY Artist, Album
    '''
    return execute_query(query_string)


if __name__ == '__main__':
    pprint.pprint(first_query(), width=100)
    print('-' * 80)
    pprint.pprint(second_query())
    print('-' * 80)
    pprint.pprint(third_query(), width=100)
