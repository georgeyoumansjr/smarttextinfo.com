from django.shortcuts import render, redirect
from Trends import get_trending_searches,get_daily_interest_over_time, get_yearly_top_charts_for_all_categories,get_related_topics,get_related_queries

# google trends only provide data for these countries
country_list = ['Argentina', 'Australia', 'Austria', 'Belgium', 'Brazil', 'Canada', 'Chile', 'Colombia', 'Czechia', 'Denmark', 'Egypt', 'Finland', 'France', 'Germany', 'Greece', 'Hong Kong', 'Hungary', 'India', 'Indonesia', 'Ireland', 'Israel', 'Italy', 'Japan', 'Kenya', 'Malaysia', 'Mexico', 'Netherlands', 'New Zealand', 'Nigeria', 'Norway', 'Peru', 'Philippines', 'Portugal', 'Romania', 'Russia', 'Saudi Arabia', 'Singapore', 'South africa', 'South Korea', 'Spain', 'Sweden', 'Switzerland', 'Taiwan', 'Thailand', 'Turkey', 'Ukraine', 'United Kingdom', 'United States']


def DailyCountryTrendSearchView(request): 
    context = {'countries' : country_list}
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
        try:
            year = request.POST.get('year')
            country = request.POST.get('country')
            data = get_yearly_top_charts_for_all_categories(year,geo=country)
            
            data_arr = []
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
            if len(data_arr) < 1:
                context['errors'] = f'Unable to get data for Year : {year} and Country : {country}, Please try again for a different Year and Country !'
            return render(request, 'api/yearlyTopChartsResult.html', context = context)
        except Exception as e:
            print(e)
            context = {
                'errors' : f'Unable to get data for Year : {year} and Country : {country}, Please try again for a different Year and Country !'
            }
            return render(request, 'api/yearlyTopChartsResult.html', context)
    return redirect(to='YearlyTopCharts')


def DailyCountryTrendSearchResultView(request): 
    if request.method == 'POST':
        try:
            country_name = request.POST.get('countryName')
            data = get_trending_searches(country_name)
        
            trends_data = []
            for key in data:
                trends_data.append(get_daily_interest_over_time(key))
            todays_trend_data = []
            for data in trends_data:
                try:
                    todays_trend_data.append(data[1])
                except Exception as e:
                    print(e)
            newlist = sorted(todays_trend_data, key=lambda d: d['value']) 
            newlist.reverse()
            context ={'trends' : newlist, 'country_name' : country_name}
            
            
            return render(request, 'api/DailyCountryTrendSearchResult.html', context=context)
        except Exception as e:
            print("Error :",e)
            context = {
                'errors' : f"Unable to find trends for {country_name}"
            }
            return render(request, 'api/DailyCountryTrendSearchResult.html', context)
    return redirect(to='DailyCountryTrendSearch')

def KeywordResearchView(request): 
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
    return render(request, 'api/KeywordResearchMain.html', context=context)

def KeywordResearchResultView(request): 
    if request.method == 'POST':
        try:
            keyword = request.POST.get('keyword')
            country = request.POST.get('country')
            related_topics = get_related_topics(keyword)
            # related_topics = get_related_topics(keyword_List=keyword , geo=country)
            # related_queries = get_related_queries(keyword , country)
            context={'countries' :[]}
            if len(related_topics) < 1:
                context['errors'] = f'Unable to get related queries for Keyword : {keyword}, please try again with a different keyword'
            context={'countries' :[]}
            return render(request, 'api/KeywordResearchResult.html', context)
        except Exception as e:
            print(e)
            context={'errors' : f'Unable to get related queries for Keyword : {keyword}, please try again with a different keyword'}
            return render(request, 'api/KeywordResearchResult.html', context)
    return redirect(to='KeywordResearch')
