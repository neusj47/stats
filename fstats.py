
import pandas as pd
from pykrx import stock
import requests
from datetime import datetime
from io import BytesIO
import warnings
warnings.filterwarnings(action='ignore')


ticker = pd.read_excel('C:/Users/ysj/Desktop/2022/20211220_부울경지수_시뮬레이션/기업리스트.xlsx', dtype = {'티커':str})

stddate = '20211228'

def get_html_fnguide(ticker):
    url = "http://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode=A"+ ticker +"&cID=&MenuYn=Y&ReportGB=&NewMenuID=103&stkGb=701"
    try :
        req =requests.get(url)
        html_text = pd.read_html(req.text)
    except AttributeError as e :
        return None
    return html_text

def get_value_by_ticker(stddate):
    query_str_parms = {
        'searchType': '1',
        'mktId': 'STK', # ALL(전체), STK(코스피)
        'trdDd': stddate,
        'csvxls_isNo': 'false',
        'name': 'fileDown',
        'url': 'dbms/MDC/STAT/standard/MDCSTAT03501'
        }
    headers = {
        'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0'
        }
    r = requests.get('http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd', query_str_parms, headers=headers)
    form_data = {
        'code': r.content
        }
    r = requests.post('http://data.krx.co.kr/comm/fileDn/download_excel/download.cmd', form_data, headers=headers)
    df = pd.read_excel(BytesIO(r.content))
    df['날짜'] = datetime.strptime(stddate, "%Y%m%d")
    df['날짜'] = datetime.strptime(stddate, "%Y%m%d")
    df['ROE'] = ''
    df['자기자본'] = ''
    df['매출액'] = ''
    for i in range(0,len(df.종목코드)) :
        df['종목코드'].iloc[i] = str(df['종목코드'][i]).zfill(6)
        try :
            df['자기자본'].iloc[i] = get_html_fnguide(df['종목코드'][i])[2]['2020/12'][8]
        except :
            df['자기자본'].iloc[i] = 0
        try :
            df['매출액'].iloc[i] = get_html_fnguide(df.티커[i])[0]['2020/12'][0]
        except :
            df['매출액'].iloc[i] = 0
        if (df['선행 PER'].iloc[i] == '-' and df['PER'].iloc[i] == '-') or (df['PBR'].iloc[i] == '-'):
            df['ROE'].iloc[i] = 0
        elif (df['선행 PER'].iloc[i] == '-' and df['PER'].iloc[i] != '-') :
            df['ROE'].iloc[i] = df['PBR'].iloc[i] / df['PER'].iloc[i]
        else :
            df['ROE'].iloc[i] = df['PBR'].iloc[i] / df['선행 PER'].iloc[i]
    return df

df_value = get_value_by_ticker(stddate)


