from pytrends.request import TrendReq
# from pytrends import interest_over_time

def get_interest_over_time(*args):
    pytrends = TrendReq(hl='en-US', tz=360)
    
    kw_list = []
    for arg in args:
        kw_list.append(arg.capitalize())
    # print(kw_list)
    # return
    # kw_list = ["Blockchain"]
    pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')

    interests = pytrends.interest_over_time()
    data = []
    for index, row in interests.iterrows():
        data.append({'date' : index.date().strftime('%Y-%m-%d'), 'value' : row['Blockchain']})

    return data

def get_related_topics(*args):
    pytrends = TrendReq(hl='en-US', tz=360)
    
    kw_list = []
    for arg in args:
        kw_list.append(arg.capitalize())
    # print(kw_list)
    # return
    # kw_list = ["Blockchain"]
    pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')

    interests =    pytrends.related_topics()
    rising_data = []
    top_data = []
    print(type(interests['Blockchain']['rising']))
    return interests
    for index, row in interests.iterrows():
        data.append({'date' : index.date().strftime('%Y-%m-%d'), 'value' : row['Blockchain']})

    return data

def get_multirange_interest_over_time(*args):
    pytrends = TrendReq(hl='en-US', tz=360)
    
    # kw_list = []
    # for arg in args:
    #     kw_list.append(arg.capitalize())
    kw_list = ['Blockchain']
    pytrends.build_payload(kw_list, timeframe=['2022-09-04 2022-09-10', '2022-09-18 2022-09-24'])
    interests = pytrends.multirange_interest_over_time()
    print(interests)
    
    # # kw_list = ["Blockchain"
    # data = []
    # for index, row in interests.iterrows():
    #     data.append({'date' : index.date().strftime('%Y-%m-%d'), 'value' : row['Blockchain']})

    # return data

data = get_related_topics('blockchain')
print(data)
