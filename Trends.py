from pytrends.request import TrendReq
import pycountry
from PyTrendsLocal import TrendReq as TrendReqLocal
# from pytrends import interest_over_time

def get_interest_over_time(*args):
    pytrends = TrendReq(hl='en-US', tz=360)
    
    kw_list = []
    for arg in args:
        kw_list.append(arg.capitalize())
    # print(kw_list)
    # return
    # kw_list = ["Blockchain"]
    # pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')
    pytrends.build_payload(kw_list=kw_list, timeframe='today 5-y')

    interests = pytrends.interest_over_time()
    # print(interests)
    data = []
    
    for keyword in kw_list:
        data_temp = {}
        for index, row in interests.iterrows():
            try:
                data_temp[index.date().strftime('%Y-%m-%d')] += row[keyword]
            except:
                data_temp[index.date().strftime('%Y-%m-%d')] = 0
        for key, value in data_temp.items():
            
            data.append({'date' : key, 'value' :value, 'key' : key})
            


    return data

def get_daily_interest_over_time(*args):
    pytrends = TrendReq(hl='en-US', tz=360)
    
    kw_list = []
    for arg in args:
        kw_list.append(arg.capitalize())
    # print(kw_list)
    # return
    # kw_list = ["Blockchain"]
    # pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')
    # pytrends.build_payload(kw_list=kw_list, timeframe='now 1-d')
    pytrends.build_payload(kw_list=kw_list, timeframe='now 1-d')

    interests = pytrends.interest_over_time()
    # print(interests)
    data = []
    
    for keyword in kw_list:
        data_temp = {}
        for index, row in interests.iterrows():
            try:
                data_temp[index.date().strftime('%Y-%m-%d')] += row[keyword]
            except:
                data_temp[index.date().strftime('%Y-%m-%d')] = 0
        for key, value in data_temp.items():
            
            data.append({'date' : key, 'value' :value, 'key' : keyword})
            


    return data


def get_related_topics(*args):
    pytrends = TrendReq(hl='en-US', tz=360)
    
    kw_list = []
    for arg in args:
        kw_list.append(arg.capitalize())
    # print(kw_list)
    # return
    # kw_list = ["Blockchain"]
    pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='GLOBAL', gprop='')
    # pytrends.build_payload(kw_list)

    interests =    pytrends.related_topics()
    rising_data = []
    top_data = []
    # columns : ['value' 'formattedValue' 'link' 'topic_mid' 'topic_title' 'topic_type']
    for key in kw_list:
        try:
            rising_df = interests[key]['rising']
            # rising_df = rising_df.drop(['formattedValue','link','topic_mid'], axis=1)
            # rising_data.append({'key' : key , 'data' : rising_df})
            for index, row in rising_df.iterrows():
                rising_data.append({'key' : key, 'value' : row['value'], 'topic_title' : row['topic_title'], 'topic_type' : row['topic_type']})
            top_df = interests[key]['top']
            for index, row in top_df.iterrows():
                top_data.append({'key' : key, 'value' : row['value'], 'topic_title' : row['topic_title'], 'topic_type' : row['topic_type']})
        except Exception as e:
            print(e)
    return rising_data, top_data
    

def get_multirange_interest_over_time(*args):
    pytrends = TrendReq(hl='en-US', tz=360)
    
    # kw_list = []
    # for arg in args:
    #     kw_list.append(arg.capitalize())
    kw_list = ['Blockchain']
    pytrends.build_payload(kw_list, timeframe=['2022-09-04 2022-09-10', '2022-09-18 2022-09-24'])
    interests = pytrends.multirange_interest_over_time()
    
    
    # # kw_list = ["Blockchain"
    # data = []
    # for index, row in interests.iterrows():
    #     data.append({'date' : index.date().strftime('%Y-%m-%d'), 'value' : row['Blockchain']})

    # return data



def get_categories(*args):
    pytrends = TrendReq(hl='en-US', tz=360)
    
    kw_list = []
    for arg in args:
        kw_list.append(arg.capitalize())
    # print(kw_list)
    # return
    # kw_list = ["Blockchain"]
    pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='GLOBAL', gprop='')
    data = pytrends.categories()
    
def get_keyword_suggestions(*args):
    pytrends = TrendReq(hl='en-US', tz=360)
    
    kw_list = []
    for arg in args:
        kw_list.append(arg.capitalize())
    # print(kw_list)
    # return
    # kw_list = ["Blockchain"]
    for keyword in kw_list:
        data = pytrends.suggestions(keyword)
        
        
def get_yearly_top_charts(year):
    pytrends = TrendReq(hl='en-US', tz=360)
    
    
    # data = pytrends.top_charts(year, hl='en-US', tz=300, geo='US')    
    data = pytrends.top_charts(year, hl='en-US', tz=300, geo='GLOBAL')    
    return(data['title'].tolist())
        
def get_related_queries(*args):
    pytrends = TrendReq(hl='en-US', tz=360)
    kw_list = []
    top_data = []
    rising_data = []
    for arg in args:
        kw_list.append(arg.capitalize())
    pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='GLOBAL', gprop='')
    data = pytrends.related_queries()
    for keyword in kw_list:
        top_data = []
        rising_data = []
        top_data_obj = data[keyword]['top']
        rising_data_obj = data[keyword]['rising']
        for index, row in top_data_obj.iterrows():
            top_data.append({'keyword' : keyword, 'query' : row['query'], 'value' : row['value']})
        for index, row in rising_data_obj.iterrows():
            rising_data.append({'keyword' : keyword, 'query' : row['query'], 'value' : row['value']})
    return rising_data, top_data
    
    # return(data['title'].tolist())

def get_realtime_trending_searches(country):
    country_obj = pycountry.countries.search_fuzzy(country)
    country_code = (country_obj[0].alpha_2)
    
    pytrends = TrendReq(hl='en-US', tz=360)
    data = pytrends.realtime_trending_searches(pn=country_code)
    return (data['title'].tolist())

def get_trending_searches(country):
    # country_obj = pycountry.countries.search_fuzzy(country)
    # print(country_obj[0])
    # return
    country = country.lower()
    country = country.replace(' ', '_')
    country_code = country
    pytrends = TrendReq(hl='en-US', tz=360)
    data = pytrends.trending_searches(pn=country_code)
    return data[0].tolist()

def get_todays_searches_for_country(country):
    pytrend = TrendReq()

    #get today's treniding topics
    trendingtoday = pytrend.today_searches(pn='US')
    return trendingtoday


def interest_over_time_test():
    # create pytrends object
    pytrends = TrendReq()

    # set up payload
    kw_list = ["python"]
    cat = 0
    timeframe = "today 5-y"
    geo = ""
    gprop = ""

    # get categories
    pytrends.build_payload(kw_list=kw_list, cat=cat, timeframe=timeframe, geo=geo, gprop=gprop)
    categories = pytrends.categories()
    # print(categories['children'])
    # print(categories['name'])
    # print(categories['id'])
    # for key, value in categories.items():
    #     print(key)
    # return
    # get trends by category for the last 5 years
    results = []
    for category in categories['children']:
        print(f"Getting trends for category: {category['name']}")
        pytrends.build_payload(kw_list=kw_list, cat=category['id'], timeframe=timeframe, geo=geo, gprop=gprop)
        category_results = pytrends.interest_over_time()
        if not category_results.empty:
            category_results = category_results.drop(columns=["isPartial"])
            category_results.columns = [category["name"]]
            results.append(category_results)

    # combine results into single dataframe
    df = results[0]
    for i in range(1, len(results)):
        df = df.join(results[i], how="outer")

    # resample dataframe to yearly frequency and sum values for each year
    df = df.resample("Y").sum()

    # print results
    print(df)




# rising_data , top_data = get_related_topics('blockchain')
# print(data)
# get_yearly_top_charts(2022)
# data = get_interest_over_time('Blockchain')
# print(data)

# data = get_trending_searches('United States')



# for key in data:
#     print(get_daily_interest_over_time(key))
#     print()
#     print('..........................................')

# get_todays_searches_for_country('united states')

# print(get_yearly_top_charts(2022))


def get_yearly_top_charts_for_all_categories(year, geo='GLOBAL'):

    pytrends = TrendReqLocal(hl='en-US', tz=360)

    # Set the year and location

    
    
    
    return pytrends.top_charts(year, geo = geo)
    