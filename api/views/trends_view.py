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
    return render(request, 'api/YearlyTopChartsMain.html')

def yearlyTopChartsResultsView(request): 
    if request.method == 'POST':
        year = request.POST.get('year')
        data = get_yearly_top_charts_for_all_categories(year)
        context = {'data' : data}
        print(context)
    return render(request, 'api/YearlyTopChartsMain.html', context = context)

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
