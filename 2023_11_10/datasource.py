import requests
import psycopg2
import password as pw

def __download_PM_data()->list[dict]:
    '''
    下載taiwan_pm25
    https://data.moenv.gov.tw/api/v2/aqx_p_02?language=zh&api_key={pw.APIKEY}
    '''
    PM_url = 'https://data.moenv.gov.tw/api/v2/aqx_p_02?language=zh&api_key={pw.APIKEY}'
    response = requests.get(PM_url)
    response.raise_for_status()
    print("連線中，請稍後．．．")
    return response.json()

def __create_table(conn)->None:    
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE  IF NOT EXISTS taiwan_pm25(
            "id"	SERIAL,
            "測站名稱"	TEXT NOT NULL,
            "縣市名稱"	TEXT NOT NULL,
            "細懸浮微粒濃度"	INTEGER NOT NULL,
            "資料建置日期"	TEXT NOT NULL,
            PRIMARY KEY("id"),
            UNIQUE(測站名稱,資料建置日期) 
        );
        '''
    )
    conn.commit()
    cursor.close()
    print("Table建立中．．．")

def __insert_data(conn,values:list[any])->None:
    cursor = conn.cursor()
    sql = '''
    INSERT INTO taiwan_pm25 (測站名稱, 縣市名稱, 細懸浮微粒濃度, 資料建置日期) 
    VALUES (%s,%s,%s,%s)
    ON CONFLICT (測站名稱,資料建置日期) DO NOTHING
    '''
    cursor.execute(sql,values)    
    conn.commit()
    cursor.close()

def updata_render_data()->None:
    '''
    下載,並更新資料庫
    '''
    data = __download_PM_data()
    conn = psycopg2.connect(database=pw.DATABASE,
                            user=pw.USER, 
                            password=pw.PASSWORD,
                            host=pw.HOST, 
                            port="5432")
        
    __create_table(conn)
    for item in data:
        __insert_data(conn,[item['site'],item['county'],item['pm25'],item['datacreationdate']])
    conn.close()

def lastest_datetime_data()->list[tuple]:
    conn = psycopg2.connect(database=pw.DATABASE,
                            user=pw.USER, 
                            password=pw.PASSWORD,
                            host=pw.HOST, 
                            port="5432")
    cursor = conn.cursor()
    sql = '''
    SELECT 測站名稱,MAX(資料建置日期) AS 資料建置日期,縣市名稱,細懸浮微粒濃度
    FROM taiwan_pm25
    GROUP BY 測站名稱,縣市名稱,資料建置日期,細懸浮微粒濃度
    '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return rows


#https://data.moenv.gov.tw/api/v2/aqx_p_02?language=zh&api_key=0d345e45-9ef9-4614-bdd2-c2adc11b2a5d PM2.5網址