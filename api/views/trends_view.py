from django.shortcuts import render
from Trends import get_trending_searches,get_daily_interest_over_time, get_yearly_top_charts_for_all_categories
import pycountry

def DailyCountryTrendSearchView(request): 
    countries_list = list(pycountry.countries)
    country_names = []
    for country in countries_list:
        country_names.append(country.name)
        
    # data = get_trending_searches('United States')
    context = {'countries' : country_names}


    # for key in data:
    #     print(get_daily_interest_over_time(key))
    #     print()
    #     print('..........................................')

    return render(request, 'api/DailyCountryTrendSearchMain.html', context=context)
def yearlyTopChartsView(request): 
    countries_list = [
        {'key' : 'GLOBAL' , 'value' : 'Global'},
        {'key' : 'US' , 'value' : 'United States'},
        {'key' : 'IT' , 'value' : 'Italy'},
        {'key' : 'GB' , 'value' : 'United Kingdom'},
        {'key' : 'DE' , 'value' : 'Germany'},
        {'key' : 'FR' , 'value' : 'France'},
        {'key' : 'RU' , 'value' : 'Russia'},
        {'key' : 'CA' , 'value' : 'Canada'},
        
        ]
    context={'countries' : countries_list}
    return render(request, 'api/YearlyTopChartsMain.html', context=context)

def yearlyTopChartsResultsView(request): 
    if request.method == 'POST':
        year = request.POST.get('year')
        country = request.POST.get('country')
        data = get_yearly_top_charts_for_all_categories(year,geo=country)
        
        data_arr = []
        # {'category': 'Searches', 'keywords': ['Wordle', 'India vs England', 'Ukraine', 'Queen Elizabeth', 'Ind vs SA', 'World Cup', 'India vs West Indies', 'iPhone 14', 'Jeffrey Dahmer', 'Indian Premier League']}
        for d in data:
            if d['category'] != 'Passings':
                if 'Google Lens:' in d['category']:
                    data_arr.append({'category' : d['category'].replace('Google Lens:', ''), 'keywords' : d['keywords']})
                elif 'Google Maps:' in d['category']:
                    data_arr.append({'category' : d['category'].replace('Google Maps:', ''), 'keywords' : d['keywords']})
                elif 'Hum to Search:' in d['category']:
                    data_arr.append({'category' : d['category'].replace('Hum to Search:', ''), 'keywords' : d['keywords']})
                else:
                    data_arr.append({'category' : d['category'], 'keywords' : d['keywords']})
        
        context = {'data' : data_arr, 'year' : year}
        
    return render(request, 'api/yearlyTopChartsResult.html', context = context)

def DailyCountryTrendSearchResultView(request): 
    if request.method == 'POST':
        country_name = request.POST.get('countryName')
        data = get_trending_searches(country_name)
    

        trends_data = []
        for key in data:
            trends_data.append(get_daily_interest_over_time(key))
        todays_trend_data = []
        for data in trends_data:
            todays_trend_data.append(data[1])
        newlist = sorted(todays_trend_data, key=lambda d: d['value']) 
        newlist.reverse()
        context ={'trends' : newlist, 'country_name' : country_name}
        
        
        return render(request, 'api/DailyCountryTrendSearchResult.html', context=context)
