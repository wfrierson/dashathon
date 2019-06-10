import mechanize
import pandas as pd
import bs4
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from math import ceil
from time import sleep
import re
import os
import sys
import unicodedata


def strip_special_latin_char(string):
    """
    Method that either transliterates selected latin characters, or maps unexpected characters to empty string, ''.

    Example::

        strip_special_latin_char('thƝis ƛis a teōst: ÆæœƔþðßøÞĿØĳƧaÐŒƒ¿Ǣ')

    :param str string: String to be striped of special latin characters
    :return: String striped of special latin characters
    :rtype: str
    """
    latin_char_map = {'Æ': 'AE', 'Ð': 'D', 'Ø': 'O', 'Þ': 'TH', 'ß': 'ss', 'æ': 'ae',
                      'ð': 'd', 'ø': 'o', 'þ': 'th', 'Œ': 'OE', 'œ': 'oe', 'ƒ': 'f'}
    string_ascii = ''
    for s in string:
        # Check if string character is ascii
        if ord(s) < 128:
            string_ascii += s
        # If not ascii but is a special latin character, transliterate
        elif s in latin_char_map.keys():
            string_ascii += latin_char_map[s]
        # Otherwise, remove the unexpected character
        else:
            string_ascii += ''
    return string_ascii


def strip_accents(string):
    """
    Method that transliterates accented characters.

    Example::

        strip_accents('thîš ìŝ ã tëśt')

    :param str string: String to be striped of accented characters
    :return: String striped of accented characters
    :rtype: str
    """
    # Taken from here:
    # https://stackoverflow.com/a/518232
    return ''.join(c for c in unicodedata.normalize('NFD', string)
                   if unicodedata.category(c) != 'Mn')


def convert_to_ascii(string):
    """
    Method that ensures a given string object is converted into ascii format by removing accented characters
    and transliterating special latin characters.

    Example::

        convert_to_ascii('thƝîš ƛìŝ ã tëśt: ÆæœƔþðßøÞĿØĳƧaÐŒƒ¿Ǣ')

    :param str string: String to be converted into ascii
    :return: String converted into ascii
    :rtype: str
    """
    string = strip_accents(string)
    string = strip_special_latin_char(string)
    return string


def row_count_csv(input_file):
    """
    Method to return the number of populated rows in a text file.

    Example::

        row_count_csv('example_file.txt')

    :param str input_file: File path
    :return: Number of popluated rows in input_file
    :rtype: int
    """
    # Modified from https://stackoverflow.com/a/44144945/3905509
    with open(input_file, errors='ignore') as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def get_last_line_csv(input_file):
    """
    Method to return the last populated line in a text file.

    Example::

        get_last_line_csv('example_file.txt')

    :param str input_file: File path
    :return: Last populated line of input_file
    :rtype: str
    """
    if row_count_csv(input_file) == 1:
        with open(input_file, 'r') as f:
            return f.readline()

    # Modified from https://www.quora.com/How-can-I-read-the-last-line-from-a-log-file-in-Python
    with open(input_file, 'rb') as f:
        f.seek(-2, os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
        last_line = f.readline().decode('utf-8')

    return last_line


def delete_last_line_csv(input_file):
    """
    Method to delete the last line in a text file.

    Example::

        delete_last_line_csv('example_file.txt')

    :param str input_file: File path
    """
    # If there's 1 line left, clear the file. This is hack-y, but needed since the code below doesn't appear to work
    # when there's 1 remaining populated row followed by 1 blank line.
    if row_count_csv(input_file) == 1:
        open(input_file, 'w').close()

    # Modified from https://stackoverflow.com/a/10289740/3905509
    with open(input_file, "r+", errors='ignore', encoding="utf-8") as file:
        # Move the pointer (similar to a cursor in a text editor) to the end of the file
        file.seek(0, os.SEEK_END)

        # This code means the following code skips the very last character in the file -
        # i.e. in the case the last line is null we delete the last line
        # and the penultimate one
        pos = file.tell() - 1

        # Read each character in the file one at a time from the penultimate
        # character going backwards, searching for a newline character
        # If we find a new line, exit the search
        while pos > 0 and file.read(1) != "\n":
            pos -= 1
            file.seek(pos, os.SEEK_SET)

        # So long as we're not at the start of the file, delete all the characters ahead
        # of this position
        if pos > 0:
            file.seek(pos, os.SEEK_SET)
            file.truncate()


def scrape_chicago_marathon_urls(url='http://chicago-history.r.mikatiming.de/2015/', year=2016,
                                 event="MAR_999999107FA30900000000A1", gender='M', num_results_per_page=1000,
                                 unit_test_ind=False):
    """
    Method to scrape all URLs of each Chicago Marathon runner returned from a specified web form.

    Example::

        scrape_chicago_marathon_urls(url='http://chicago-history.r.mikatiming.de/2015/', year=2017,
                                          event="MAR_999999107FA30900000000A1", gender='M',
                                          num_results_per_page=1000, unit_test_ind=True)

    :param str url: URL to Chicago Marathon web form
    :param int year: Year of marathon (supported values: 2014, 2015, 2016, 2017)
    :param str event: Internal label used to specify the type of marathon participants (varies by year)
    :param str gender: Gender of runner ('M' for male, 'W' for female)
    :param int num_results_per_page: Number of results per page to return from the web form (use default value only)
    :param bool unit_test_ind: Logical value to specify if only the first URL should be returned (True) or all (False)
    :return: DataFrame containing URLs, City, and State for all runners found in results page
    :rtype: pandas.DataFrame
    """
    # Setup backend browser via mechanize package
    br = mechanize.Browser()

    # Ignore robots.txt
    # Note: I have not found any notice on the Chicago Marathon website that prohibits web scraping.
    br.set_handle_robots(False)

    br.open(url)

    # Select the overall results, not individual runner results
    br.select_form(nr=2)

    # Set year
    br.form['event_main_group'] = [str(year)]
    
    # Manually add an option for the 'event' drop-down, which is expected to be populated when the the
    # 'event_main_group' drop-down is modified.
    mechanize.Item(
        br.form.find_control(name='event'),
        {'contents': event, 'value': event, 'label': event}
    )

    # Set event
    br.form['event'] = [event]

    # Set gender
    br.form['search[sex]'] = gender

    # Set age group
    br.form['search[age_class]'] = "%"

    # Set number of results per page
    br.form['num_results'] = [str(num_results_per_page)]

    # Submit form
    resp = br.submit()
    
    # Retrieve selected tags via SoupStrainer
    html = resp.read()            
    strainer = SoupStrainer(["ul", "h4"])
    soup = BeautifulSoup(html, "lxml", parse_only=strainer)
    
    # The first instance of ul with class = list-group appears to always
    # contain the total expected number of results
    first_list_group_item = soup.select_one('li.list-group-item').text
    total_expected_num_results = int(str.split(first_list_group_item)[0])
    total_expected_num_pages = ceil(total_expected_num_results / num_results_per_page)
    print('Finding URLs for Year = ' + str(year) + ' and Gender = ' + str(gender))
    print('Total expected results: ' + str(total_expected_num_results))
    
    # Define lists to store data
    result_urls = []
    result_cities = []
    result_states = []
    
    # Starting with 1 page returned since the form was submitted
    total_returned_num_pages = 1
    total_returned_num_results = 0
    while total_returned_num_pages <= total_expected_num_pages:        
        print('Progress: Page ' + str(total_returned_num_pages) + ' of ' + str(total_expected_num_pages), end='\r')
        if total_returned_num_pages > 1:
            # Note: No delay is included here because the current code
            # takes longer than 1 second to complete per page. We feel
            # that this is enough to avoid hammering the server and hogging
            # resources.
                        
            # The link with text ">" appears to always point to the next
            # results page.
            next_page_link = br.find_link(text='>')
            resp = br.follow_link(next_page_link)
            html = resp.read()
            soup = BeautifulSoup(html, "lxml", parse_only=strainer)
        
        # Store URLs for individual runners
        runner_links = soup.select('h4.type-fullname a[href]')
        result_per_page_count = 0
        for link in runner_links:
            runner_url = url + link['href']
            result_urls.extend([runner_url])
            result_per_page_count += 1
            if unit_test_ind:
                break
                
        # Grab city & state data since it's only fully populated on the
        # form results page, not the individual runners' pages.
        # The 'type-eval' label appears to always store this info.        
        # The first element in the CSS select statement is the table
        # header "City, State", which we don't want. Manually removing
        # this element via indexing.
        location_table = soup.select('div.type-eval')[1:]
        for location_row in location_table:
            # The text of each location_row includes a sub-header "City, State",
            # which we don't want. Using re.sub to remove it.
            location = re.sub('City, State', '', location_row.text).split(', ')

            # Some runners have no location listed, which is presented as '-'.
            if location[0] == '–':
                result_cities.append(None)
                result_states.append(None)
            else:
                city = convert_to_ascii(location[0].replace('"', ''))
                result_cities.append(city)
                
                # Store state info if present in the 2nd element of location.
                if len(location) == 2:
                    state = convert_to_ascii(location[1].replace('"', ''))
                    result_states.append(state)
                else:
                    result_states.append(None)
            if unit_test_ind:
                break
                
        # Tracking returned results for printing to console.
        total_returned_num_results += result_per_page_count
        total_returned_num_pages += 1

        if unit_test_ind:
            break
    
    print('')
    print('URL scraping complete!')
    
    # Combining all results into one pd.DataFrame.
    dict_urls = {'urls': result_urls}
    dict_city = {'city': result_cities}
    dict_state = {'state': result_states}
    dict_results = {}
    for dictionary in [dict_urls, dict_city, dict_state]:
        dict_results.update(dictionary)
        
    df = pd.DataFrame.from_dict(dict_results)
    df = df.reindex(['urls', 'city', 'state'], axis='columns')
    
    return df


def scrape_chicago_runner_details(url, gender, city, state):
    """
    Method to scrape relevant information about a given runner in Chicago Marathon. The scraped details include:

    * **year**: Year in which the runner participated in the marathon
    * **bib**: Bib number to specify the runner for the particular marathon
    * **age_group**: Age of runner at time of marathon. Expressed in 5 year bands, except for 16-19.
    * **gender**: Gender of runner
    * **city**: Runner's home city
    * **state**: Runner's home state
    * **country**: Runner's home country
    * **overall**: Overall rank for runner based on the finish time
    * **rank_gender**: Rank for runner within gender category based on the finish time
    * **rank_age_group**: Rank for runner within age category based on the finish time
    * **5k**: Split time at 5 km in seconds
    * **10k**: Split time at 10 km in seconds
    * **15k**: Split time at 15 km in seconds
    * **20k**: Split time at 20 km in seconds
    * **half**: Split time at half marathon in seconds
    * **25k**: Split time at 25 km in seconds
    * **30k**: Split time at 30 km in seconds
    * **35k**: Split time at 35 km in seconds
    * **40k**: Split time at 40 km in seconds
    * **finish**: Split time to complete marathon in seconds

    Example::

        scrape_chicago_runner_details(url=('http://chicago-history.r.mikatiming.de/2015/?content=detail&fpid='
                                           'search&pid=search&idp=999999107FA309000019D3BA&lang=EN_CAP&event='
                                           'MAR_999999107FA309000000008D&lang=EN_CAP&search%5Bstart_no%5D='
                                           '54250&search_event=ALL_EVENT_GROUP_2016'), gender='M', city='Portland',
                                           state='OR')

    :param str url: URL for an individual runner's results
    :param str gender: Gender of runner ('M' for male, 'W' for female)
    :param str city: City specified by runner
    :param str state: State specified by runner
    :return: DataFrame
    :rtype: pandas.DataFrame
    """
    br = mechanize.Browser()

    # Ignore robots.txt
    br.set_handle_robots(False)

    # Link to results of a single runner
    # Use try/except in case of unexpected internet/URL issues
    try:
        br.open(url)
    except (mechanize.HTTPError, mechanize.URLError) as e:
        if hasattr(e, 'code'):
            if int(e.code) == 500:
                print('Following URL has HTTP Error 500:')
                print(url)
            else:
                print('Following URL has unexpected connection issue:')
                print(url)
            return 'Connection error'

    html = br.response().read()    
    strainer = SoupStrainer(['tr', 'thead'])
    soup = BeautifulSoup(html, "lxml", parse_only=strainer)

    # Only process runners having event = 'Marathon', for the purposes of this project.
    # Note: This is precautionary, as early exploration showed that non-runners were included among the results.
    # This issue no longer appears present.
    event_name = soup.select('td.f-event_name')[0].text
    if event_name != 'Marathon':
        return None
    
    # Grab runner's info
    marathon_year = int(soup.select('td.f-event_date')[0].text)
    full_name = soup.select('td.f-__fullname')[0].text
    age_group = soup.select('td.f-age_class')[0].text
    bib_number = soup.select('td.f-start_no')[0].text

    # Derive country name from runner's name.
    # Modified from here:
    # https://stackoverflow.com/a/4894156/3905509
    country = convert_to_ascii(full_name[full_name.find("(")+1:full_name.find(")")])

    rank_gender = soup.select('td.f-place_all')[0].text
    rank_age_group = soup.select('td.f-place_age')[0].text
    rank_overall = soup.select('td.f-place_nosex')[0].text

    headers_index = ['year', 'bib', 'age_group', 'gender', 'city', 'state', 'country', 'overall', 'rank_gender',
                     'rank_age_group']
    headers = headers_index.copy()
    cols_constant = [marathon_year, bib_number, age_group, gender, city, state, country, rank_overall, rank_gender,
                     rank_age_group]
    headers_splits = soup.select('thead th')
    for header_split in headers_splits:
        headers.append(header_split.text)

    headers = [header.lower() for header in headers]    

    df = pd.DataFrame(columns=headers)
    split_string_bs4 = 'tr.f-time_'
    splits = ['05', '10', '15', '20', '52', '25', '30', '35', '40', 'finish_netto']
    splits_select_list = [split_string_bs4 + split for split in splits]
    for split_select in splits_select_list:
        splits_row = soup.select(split_select)

        # Take union of text in each column of splits_row
        splits_row_union = [cell.text for cell in splits_row]

        # Expecting the 'Finish' split time to share CSS tag with 'Finish Time',
        # which excludes other info. In this case, only keep the former data.
        if len(splits_row_union) > 1:        
            cols = cols_constant + splits_row_union[1].split('\n')[1:-1]
        else:
            cols = cols_constant + splits_row_union[0].split('\n')[1:-1]

        # Convert results into a single row pd.DataFrame
        cols = [dict(zip(headers, cols))]
        df_row = pd.DataFrame(cols, columns=headers)
        df = df.append(df_row)

    # Reset index of dataframe since each row was individually appended
    df.reset_index(drop=True, inplace=True)

    # Only keep relevant fields
    df = df[headers_index + ['split', 'time']]

    # Convert split times into numeric seconds from strings.
    # Modified from the following:
    # https://stackoverflow.com/a/44445488/3905509
    df['time'] = pd.to_timedelta(df['time']).dt.total_seconds()

    # Convert split labels to lowercase
    df['split'] = df['split'].str.lower()

    # Pivot scraped data into 1 row for convenience
    df = pd.pivot_table(
        df,
        index=headers_index,
        columns='split',
        values='time',
        aggfunc='first'
    ).reset_index()
    
    # Rename '05k' column to '5k'
    df.rename(columns={'05k': '5k'}, inplace=True)
    
    # Reorder split times for convenience
    headers = headers_index.copy() + ['5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k', 'finish']
    df = df.reindex(headers, axis='columns')
    
    return df


def scrape_chicago_marathon(path_input, path_output, path_error, gender, headers, df_urls=None):
    """
    Method to scrape all Chicago Marathon data for a given year and gender using output from
    `scrape_chicago_marathon_urls` and `scrape_chicago_runner_details`.

    * If running for first time, the input `df_urls` should be direct output from `scrape_chicago_marathon_urls`.

    * If restarting a prior scraping run, leave `df_urls` as None or empty and specify the input caching file
      `path_input`, which is a subset of output from `scrape_chicago_marathon_urls`.

    Each row of `path_input` is used to scrape an individual runner's split times. The scraped data is inserted into
    the `path_output` file and then the row from `path_input` is deleted to log the completed scrape.

    **Note**: The `headers` input is assumed to contain the same headers as returned by `scrape_chicago_runner_details`.
    If the code for this function changes, the input headers should be modified.

    The final output of this method is the populated file designated by `path_output` (nothing is returned).

    Example::

        # FIRST SCRAPING RUN
        scraped_df_url = scrape_chicago_marathon_urls(url='http://chicago-history.r.mikatiming.de/2015/', year=2017,
                                                      event="MAR_999999107FA30900000000A1", gender='M',
                                                      num_results_per_page=1000, unit_test_ind=True)

        scrape_chicago_marathon(path_input='demo_input_chicago.csv', path_output='demo_output_chicago.csv',
                                path_error='demo_error_log_chicago.csv', gender='M', headers=headers_chicago,
                                df_urls=scraped_df_url)

        # SECOND AND SUBSEQUENT SCRAPING RUNS
        scrape_chicago_marathon(path_input='demo_input_chicago.csv', path_output='demo_output_chicago.csv',
                                path_error='demo_error_log_chicago.csv', gender='M', headers=headers_chicago)

    :param str path_input: Path for file containing exported results from scrape_chicago_marathon_urls. If it does not
                           exist and df_urls is supplied, it will be created and populated with data exported from
                           df_urls.
    :param str path_output: Path for file containing exported results from scrape_chicago_runner_details. If it does
                            not exist, it will be created.
    :param str path_error: Path for file containing a log of records from path_input that could not be processed due to
                           a connectivity error.
    :param str gender: Gender of runner ('M' for male, 'W' for female)
    :param list[str] headers: List of strings representing expected headers for scrape_chicago_runner_details.
    :param pandas.DataFrame df_urls: DataFrame containing output from scrape_chicago_marathon_urls. This should only be
                                     included when running the first scraping for that year & gender.
    """
    # Assume headers is a list. Convert it to a flattened string.
    headers = '|'.join(headers) + '\n'
    
    # Check if the expected input file of URLs exists or not.
    check_file_input = os.path.isfile(path_input)    
    
    # Export df_urls if the input file doesn't exist, i.e., starting from scratch
    if not check_file_input and df_urls is not None:
        df_urls.to_csv(path_input, header=False, index=False, sep='|')

        len_input = row_count_csv(path_input)
        
        # Need to remove blank line created by Pandas for Windows machines
        # See the following link for details:
        # https://github.com/pandas-dev/pandas/issues/20353#issuecomment-392302201
        if sys.platform == 'win32' and len_input > 1:
            delete_last_line_csv(path_input) 
    else:
        len_input = row_count_csv(path_input)

    # Check if expected output file of scraped data exists or not
    check_file_output = os.path.isfile(path_output)
    
    # Create output file and append expected header row if it doesn't exist.
    if not check_file_output:
        with open(path_output, 'w', encoding="utf-8") as output_file:
            output_file.write(headers)

    # Check if expected error log exists or not
    check_file_error = os.path.isfile(path_error)
    # Create output file and append expected header row if it doesn't exist.
    if not check_file_error:
        with open(path_error, 'w', encoding="utf-8") as error_file:
            error_file.write('failed_urls\n')
    
    print('Starting to scrape Chicago Marathon split times...')
    scrape_count = 0
    while os.stat(path_input).st_size > 0:        
        # Grab last line of input file and scrape its associated data
        row_input = get_last_line_csv(path_input).strip()
        runner_input = row_input.split('|')
        url_input = runner_input[0]
        city_input = runner_input[1]
        state_input = runner_input[2]
        
        runner_output = scrape_chicago_runner_details(
            url=url_input,
            gender=gender,
            city=city_input,
            state=state_input
        )
        
        # Handle cases where scrape_chicago_runner_details returns none. Remove the input record and continues,
        # assuming the record is not relevant for this analysis.
        if runner_output is None:
            delete_last_line_csv(path_input)            
            sleep(0.5)
            print('Reducing total number of runners...')
            len_input -= 1
            continue
        
        # Handle cases where scrape_chicago_runner_details has a connection issue. Often, these are random and could be
        # retried later. The current path_input row is appended to an error log.
        if type(runner_output).__name__ == 'str' and runner_output == 'Connection error':            
            with open(path_error, 'a', encoding="utf-8") as error_file:
                error_file.write(row_input)
                error_file.write('\n')
            delete_last_line_csv(path_input)
            sleep(0.5)
            print('Reducing total number of runners...')
            len_input -= 1
            continue
        
        output_string = re.sub(' +', '|', runner_output.to_string(header=False, index=False))[1:] + '\n'

        # Append scraped data to the output file path_output
        with open(path_output, 'a', encoding="utf-8") as output_file:
            output_file.write(output_string)

        delete_last_line_csv(path_input)
        scrape_count += 1
        print('Progress: ' + str(scrape_count) + ' of ' + str(len_input), end='\r')
        sleep(0.5)
    
    print('')
    print('Scraping of split times complete!')


# London
def scrape_london_marathon_urls(url, event='MAS', year=2017, gender='M', num_results_per_page=1000,
                                unit_test_ind=False):
    """
    Method to scrape all URLs of each London Marathon runner returned from a specified web form::

        scrape_london_marathon_urls(url='http://results-2017.virginmoneylondonmarathon.com/2017/',
                                         event='MAS', year=2017, gender='M', num_results_per_page=1000,
                                         unit_test_ind=True)

    :param str url: URL to London Marathon web form
    :param str event: Internal label used to specify the type of marathon participants (varies by year)
    :param int year: Year of marathon (supported values: 2014, 2015, 2016, 2017)
    :param str gender: Gender of runner ('M' for male, 'W' for female)
    :param int num_results_per_page: Number of results per page to return from the web form (use default value only)
    :param bool unit_test_ind: Logical value to specify if only the first URL should be returned (True) or all (False)
    :return: DataFrame containing URLs for all runners found in results page
    :rtype: pandas.DataFrame
    """
    # Setup backend browser via mechanize package
    br = mechanize.Browser()

    # Ignore robots.txt
    # Note: I have not found any notice on the London Marathon website that prohibits web scraping.
    br.set_handle_robots(False)
        
    br.open(url)

    # Select the overall results, not individual runner results
    br.select_form(nr=1)

    # Set event
    br.form['event'] = [event]

    # Set gender
    br.form['search[sex]'] = gender

    # Set age group
    br.form['search[age_class]'] = "%"

    # Set number of results per page
    br.form['num_results'] = [str(num_results_per_page)]

    # Submit form
    resp = br.submit()
    
    # Use bs4 package to find expected number of total results to facilitate retrieving URLs.
    html = resp.read()
    soup = BeautifulSoup(html, "html.parser")

    num_results_div = soup.find_all('div', {'class': 'list-info-text'})[0]
    total_expected_num_results = int(str.split(num_results_div.text)[0])
    total_expected_num_pages = ceil(total_expected_num_results / num_results_per_page)
    print('Finding URLs for Year = ' + str(year) + ' and Gender = ' + str(gender))
    print('Total expected results: ' + str(total_expected_num_results))
    
    # Define lists to store data
    result_urls = []
    
    # Starting with 1 page returned since the form was submitted
    total_returned_num_pages = 1
    total_returned_num_results = 0
    while total_returned_num_pages <= total_expected_num_pages:        
        print('Progress: Page ' + str(total_returned_num_pages) + ' of ' + str(total_expected_num_pages), end='\r')
        if total_returned_num_pages > 1:
            # Note: No delay is included here because the current code takes longer than 1 second to complete per page.
            # We feel that this is enough to avoid hammering the server and hogging resources.
            
            # The link with text ">" appears to always point to the next results page.
            next_page_link = br.find_link(text='>')
            resp = br.follow_link(next_page_link)
            html = resp.read()
            soup = BeautifulSoup(html, "html.parser")            

        results_table = soup.find('tbody').find_all('tr')
        result_per_page_count = 0
        for results_row in results_table:
            results_url_cell = results_row.find_all('td')[3]
            results_url = results_url_cell.find_all('a', href=True)[0]['href']
            result_urls.extend([url + results_url])
            result_per_page_count += 1
            if unit_test_ind:
                break

        total_returned_num_results += result_per_page_count                                        
        total_returned_num_pages += 1
        if unit_test_ind:
            break
    
    print('')
    print('URL scraping complete!')
    dict_urls = {'urls': result_urls}        
    df = pd.DataFrame.from_dict(dict_urls)
    
    return df


def scrape_london_runner_details(url, year, gender):
    """
    Method to scrape relevant information about a given runner in London Marathon. The scraped details include:

    * **year**: Year in which the runner participated in the marathon
    * **bib**: Bib number to specify the runner for the particular marathon
    * **age_group**: Age of runner at time of marathon. Expressed in 5 year bands with the youngest being 18-39.
    * **gender**: Gender of runner
    * **country**: Runner's home country
    * **overall**: Overall rank for runner based on the finish time
    * **rank_gender**: Rank for runner within gender category based on the finish time
    * **rank_age_group**: Rank for runner within age category based on the finish time
    * **5k**: Split time at 5 km in seconds
    * **10k**: Split time at 10 km in seconds
    * **15k**: Split time at 15 km in seconds
    * **20k**: Split time at 20 km in seconds
    * **half**: Split time at half marathon in seconds
    * **25k**: Split time at 25 km in seconds
    * **30k**: Split time at 30 km in seconds
    * **35k**: Split time at 35 km in seconds
    * **40k**: Split time at 40 km in seconds
    * **finish**: Split time to complete marathon in seconds

    Example::

        scrape_london_runner_details(url=('http://results-2017.virginmoneylondonmarathon.com/2017/?content='
                                          'detail&fpid=list&pid=list&idp=9999990F5ECC85000024C3F9&lang='
                                          'EN_CAP&event=MAS&num_results=1000&search%5Bage_class%5D='
                                          '%25&search%5Bsex%5D=M&search_event=MAS'), year=2017, gender='M')

    :param str url: URL for an individual runner's results
    :param int year: Year of marathon (supported values: 2014, 2015, 2016, 2017)
    :param str gender: Gender of runner ('M' for male, 'W' for female)
    :return: DataFrame
    :rtype: pandas.DataFrame
    """
    br = mechanize.Browser()

    # Ignore robots.txt
    br.set_handle_robots(False)

    # Link to results of a single runner. Use try/except in case of unexpected internet/URL issues.
    try:
        br.open(url)
    except (mechanize.HTTPError, mechanize.URLError) as e:
        if hasattr(e, 'code'):
            if int(e.code) == 500:
                print('Following URL has HTTP Error 500:')
                print(url)
            else:
                print('Following URL has unexpected connection issue:')
                print(url)
            return 'Connection error'

    html = br.response().read()
    soup = BeautifulSoup(html, "html.parser")

    age_group = soup.find_all('td', {'class': 'f-age_class'})[0].text
    bib_number = soup.find_all('td', {'class': 'f-start_no_text'})[0].text
    full_name = soup.find_all('td', {'class': 'f-__fullname'})[0].text
    
    # Modified from here:
    # https://stackoverflow.com/a/4894156/3905509
    country = convert_to_ascii(full_name[full_name.find("(")+1:full_name.find(")")])

    rank_gender = soup.find_all('td', {'class': 'f-place_all'})[0].text
    rank_age_group = soup.find_all('td', {'class': 'f-place_age'})[0].text
    rank_overall = soup.find_all('td', {'class': 'f-place_nosex'})[0].text

    # Some runners have no split data at all. This can be found when the total number of "table" tabs is not equal to 5.
    # The expected split table is the 4th table when there are 5 total tables.
    splits_table = soup.find_all('table', {'class': 'list-table'})
    if len(splits_table) != 5:
        return None
    else:
        splits_table = splits_table[3]

    headers_index = ['year', 'bib', 'age_group', 'gender', 'country', 'overall', 'rank_gender', 'rank_age_group']
    headers = headers_index.copy()
    cols_constant = [year, bib_number, age_group, gender, country, rank_overall, rank_gender, rank_age_group]
    for header_name in splits_table.find_all('tr')[0]:
        if type(header_name) is not bs4.element.NavigableString:        
            headers.append(header_name.get_text())

    # Ensure headers are lowercase for downstream convention
    headers = [header.lower() for header in headers]

    # Populate data
    df = pd.DataFrame(columns=headers)
    for split_row in splits_table.find_all('tr'):    
        split_row_name = split_row.find_all('th')[0].text
        cols = split_row.find_all('td')
        cols = cols_constant + [split_row_name] + [cell.text.strip() for cell in cols]    
        cols = [dict(zip(headers, cols))]
        df_row = pd.DataFrame(cols, columns=headers)
        # First element of split_row contains metadata that we don't want to scrap.
        if split_row_name != 'Split':
            df = df.append(df_row)

    # Reset index of dataframe since each row was individually appended.
    df.reset_index(drop=True, inplace=True)

    # Only keep relevant fields
    df = df[headers_index + ['split', 'time']]

    # Convert split times into numeric seconds from strings.
    # Modified from the following:
    # https://stackoverflow.com/a/44445488/3905509
    df['time'] = pd.to_timedelta(df['time']).dt.total_seconds()

    # Convert split labels to lowercase
    df['split'] = df['split'].str.lower()

    # Pivot scraped data into 1 row for convenience
    df = pd.pivot_table(
        df,
        index=headers_index,
        columns='split',
        values='time',
        aggfunc='first'
    ).reset_index()

    # Rename '05k' column to '5k'
    df.rename(columns={'05k': '5k'}, inplace=True)

    # Reorder split times for convenience
    if year == 2014:
        headers_splits = ['5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k', 'finish time']
    else:
        headers_splits = ['5k', '10k', '15k', '20k', 'half', '25k', '30k', '35k', '40k', 'finish']
    
    headers = headers_index.copy() + headers_splits
    df = df.reindex(headers, axis='columns')

    return df


def scrape_london_marathon(path_input, path_output, path_error, year, gender, headers, df_urls=None):
    """
    Method to scrape all London Marathon data for a given year and gender using output from
    `scrape_london_marathon_urls` and `scrape_london_runner_details`.

    * If running for first time, the input `df_urls` should be direct output from `scrape_london_marathon_urls`.

    * If restarting a prior scraping run, leave `df_urls` as None or empty and specify the input caching file
      `path_input`, which is a subset of output from `scrape_london_marathon_urls`.

    Each row of `path_input` is used to scrape an individual runner's split times. The scraped data is inserted into
    the `path_output` file and then the row from `path_input` is deleted to log the completed scrape.

    **Note**: The `headers` input is assumed to contain the same headers as returned by `scrape_london_runner_details`.
    If the code for this function changes, the input headers should be modified.

    The final output of this method is the populated file designated by `path_output` (nothing is returned).

    Example::

        # FIRST SCRAPING RUN
        scraped_df_url = scrape_london_marathon_urls(url='http://results-2017.virginmoneylondonmarathon.com/2017/',
                                                     event='MAS', year=2017, gender='M', num_results_per_page=1000,
                                                     unit_test_ind=True)

        scrape_london_marathon(path_input='demo_input_london.csv',
                               path_output='demo_output_london.csv',
                               path_error='demo_error_log_london.csv',
                               year=2017, gender='M', headers=headers_london, df_urls=scraped_df_url)

        # SECOND AND SUBSEQUENT SCRAPING RUNS
        scrape_london_marathon(path_input='demo_input_london.csv',
                               path_output='demo_output_london.csv',
                               path_error='demo_error_log_london.csv',
                               year=2017, gender='M', headers=headers_london)

    :param str path_input: Path for file containing exported results from scrape_london_marathon_urls. If it does not
                           exist and df_urls is supplied, it will be created and populated with data exported from
                           df_urls.
    :param str path_output: Path for file containing exported results from scrape_london_runner_details. If it does
                            not exist, it will be created.
    :param str path_error: Path for file containing a log of records from path_input that could not be processed due to
                           a connectivity error.
    :param int year: Year of marathon (supported values: 2014, 2015, 2016, 2017)
    :param str gender: Gender of runner ('M' for male, 'W' for female)
    :param list[str] headers: List of strings representing expected headers for scrape_london_runner_details.
    :param pandas.DataFrame df_urls: DataFrame containing output from scrape_london_marathon_urls. This should only be
                                     included when running the first scraping for that year & gender.
    """
    # Assume headers is a list. Convert it to a flattened string.
    headers = '|'.join(headers) + '\n'
    
    # Check if the expected input file of URLs exists or not
    check_file_input = os.path.isfile(path_input)
    
    # Export df_urls if the input file doesn't exist, i.e., starting from scratch.
    if not check_file_input and df_urls is not None:
        df_urls.to_csv(path_input, header=False, index=False, sep='|')

        len_input = row_count_csv(path_input)

        # Need to remove blank line created by Pandas for Windows machines
        # See the following link for details:
        # https://github.com/pandas-dev/pandas/issues/20353#issuecomment-392302201
        if sys.platform == 'win32' and len_input > 1:
            delete_last_line_csv(path_input)
    else:
        len_input = row_count_csv(path_input)
        
    # Check if expected output file of scraped data exists or not.
    check_file_output = os.path.isfile(path_output)
    
    # Create output file and append expected header row if it doesn't exist.
    if not check_file_output:
        with open(path_output, 'w', encoding="utf-8") as output_file:
            output_file.write(headers)

    # Check if expected error log exists or not
    check_file_error = os.path.isfile(path_error)
    
    # Create output file and append expected header row if it doesn't exist.
    if not check_file_error:
        with open(path_error, 'w', encoding="utf-8") as error_file:
            error_file.write('failed_urls\n')
            
    len_input = row_count_csv(path_input) 
    
    print('Starting to scrape London Marathon split times...')
    scrape_count = 0
    while os.stat(path_input).st_size > 0:        
        # Grab last line of input file and scrape its associated data
        row_input = get_last_line_csv(path_input).strip()
        
        runner_output = scrape_london_runner_details(
            url=row_input,
            year=year,
            gender=gender
        )
        
        # Handle cases where scrape_london_runner_details returns None, which occur when a runner's details page
        # excludes split times.
        if runner_output is None:
            delete_last_line_csv(path_input)
            sleep(0.5)
            print('Runner has no split times.')
            print('Reducing total number of runners...')
            len_input -= 1
            continue
        
        # Handle cases where scrape_london_runner_details has a connection issue. Often, these are random and could be
        # retried later. The current path_input row is appended to an error log.
        if type(runner_output).__name__ == 'str' and runner_output == 'Connection error':            
            with open(path_error, 'a', encoding="utf-8") as error_file:
                error_file.write(row_input)
                error_file.write('\n')
            delete_last_line_csv(path_input)
            sleep(0.5)
            print('Reducing total number of runners...')
            len_input -= 1
            continue
        
        output_string = re.sub(' +', '|', runner_output.to_string(header=False, index=False))[1:] + '\n'

        # Append scraped data to the output file path_output
        with open(path_output, 'a', encoding="utf-8") as output_file:
            output_file.write(output_string)

        delete_last_line_csv(path_input)
        scrape_count += 1
        print('Progress: ' + str(scrape_count) + ' of ' + str(len_input), end='\r')
        sleep(0.5)
    
    print('')
    print('Scraping of split times complete!')


def scrape_berlin_marathon_urls(url, event='MAL', year=2017, gender='M', num_results_per_page=100, unit_test_ind=False):
    """
    Method to scrape all URLs of each Berlin Marathon runner returned from a specified web form::

        scrape_berlin_marathon_urls(url='http://results.scc-events.com/2016/',
                                         event='MAL_99999905C9AF3F0000000945', year=2016, gender='M',
                                         num_results_per_page=100, unit_test_ind=True)

    :param str url: URL to Berlin Marathon web form
    :param str event: Internal label used to specify the type of marathon participants (varies by year)
    :param int year: Year of marathon (supported values: 2014, 2015, 2016, 2017)
    :param str gender: Gender of runner ('M' for male, 'W' for female)
    :param int num_results_per_page: Number of results per page to return from the web form (use default value only)
    :param bool unit_test_ind: Logical value to specify if only the first URL should be returned (True) or all (False)
    :return: DataFrame containing URLs for all runners found in results page
    :rtype: pandas.DataFrame
    """
    # Setup backend browser via mechanize package
    br = mechanize.Browser()

    # Ignore robots.txt
    # Note: I have not found any notice on the London Marathon website that prohibits web scraping.
    br.set_handle_robots(False)
        
    br.open(url)

    # Select the overall results, not individual runner results
    br.select_form(nr=1)

    # Set event
    br.form['event'] = [event]

    # Set gender
    if year == 2017:
        br.form['search[sex]'] = gender
    else:        
        br.form['sex'] = [gender]
    
    # Set age group
    if year == 2017:
        br.form['search[age_class]'] = "%"
    else:
        br.form['ageclass'] = [""]        

    # Set number of results per page
    br.form['num_results'] = [str(num_results_per_page)]

    # Submit form
    resp = br.submit()
    
    # Use bs4 package to find expected number of total results to facilitate retrieving URLs
    html = resp.read()
    soup = BeautifulSoup(html, "html.parser")
    
    # The first instance of ul with class = list-group appears to always contain the total expected number of results.
    num_results_div = soup.find_all('div', {'class': 'pages'})[0]
    total_expected_num_pages = int(num_results_div.find_all('a')[-2].text)
    print('Finding URLs for Year = ' + str(year) + ' and Gender = ' + str(gender))
    
    # Define lists to store data
    result_urls = []
    
    # Starting with 1 page returned since the form was submitted
    total_returned_num_pages = 1
    total_returned_num_results = 0
    while total_returned_num_pages <= total_expected_num_pages:        
        print('Progress: Page ' + str(total_returned_num_pages) + ' of ' + str(total_expected_num_pages), end='\r')
        if total_returned_num_pages > 1:
            # Note: No delay is included here because the current code takes longer than 1 second to complete per page.
            # We feel that this is enough to avoid hammering the server and hogging resources.
            
            # The link with text ">" appears to always point to the next results page.
            next_page_link = br.find_link(text='>')
            resp = br.follow_link(next_page_link)
            html = resp.read()
            soup = BeautifulSoup(html, "html.parser")

        result_per_page_urls = []
        
        results_table = soup.find('tbody').find_all('tr')
        result_per_page_count = 0
        for results_row in results_table:
            results_url_cell = results_row.find_all('td')[2]
            results_url = results_url_cell.find_all('a', href=True)[0]['href']
            result_per_page_urls.extend([url + results_url])
            result_per_page_count += 1
            if unit_test_ind:
                break
            
        # Store URLs
        result_urls.extend(result_per_page_urls)
        
        total_returned_num_results += result_per_page_count                                        
        total_returned_num_pages += 1
        if unit_test_ind:
            break
    
    print('')
    print(str(total_returned_num_results) + ' results returned.')
    print('URL scraping complete!')
    dict_urls = {'urls': result_urls}        
    df = pd.DataFrame.from_dict(dict_urls)
    
    return df


def scrape_berlin_runner_details(url, year, gender):
    """
    Method to scrape relevant information about a given runner in Berlin Marathon. The scraped details include:

    * **year**: Year in which the runner participated in the marathon
    * **bib**: Bib number to specify the runner for the particular marathon
    * **age_group**: Age of runner at time of marathon. Expressed in 5 year bands with the youngest being 30-34.
    * **gender**: Gender of runner
    * **country**: Runner's home country
    * **rank_gender**: Rank for runner within gender category based on the finish time
    * **rank_age_group**: Rank for runner within age category based on the finish time
    * **5k**: Split time at 5 km in seconds
    * **10k**: Split time at 10 km in seconds
    * **15k**: Split time at 15 km in seconds
    * **20k**: Split time at 20 km in seconds
    * **half**: Split time at half marathon in seconds
    * **25k**: Split time at 25 km in seconds
    * **30k**: Split time at 30 km in seconds
    * **35k**: Split time at 35 km in seconds
    * **40k**: Split time at 40 km in seconds
    * **finish**: Split time to complete marathon in seconds

    Example::

        scrape_berlin_runner_details(url=('http://results.scc-events.com/2016/?content=detail&fpid='
                                          'search&pid=search&idp=99999905C9AF460000404FFD&lang=EN&event='
                                          'MAL_99999905C9AF3F0000000945&search%5Bstart_no%5D=30529'
                                          '&search_sort=name&search_event=MAL_99999905C9AF3F0000000945'),
                                           year=2016, gender='M')

    :param str url: URL for an individual runner's results
    :param int year: Year of marathon (supported values: 2014, 2015, 2016, 2017)
    :param str gender: Gender of runner ('M' for male, 'W' for female)
    :return: DataFrame
    :rtype: pandas.DataFrame
    """
    br = mechanize.Browser()

    # Ignore robots.txt
    br.set_handle_robots(False)

    # Link to results of a single runner.
    # Use try/except in case of unexpected internet/URL issues.
    try:
        br.open(url)
    except (mechanize.HTTPError, mechanize.URLError) as e:
        if hasattr(e, 'code'):
            if int(e.code) == 500:
                print('Following URL has HTTP Error 500:')
                print(url)
            else:
                print('Following URL has unexpected connection issue:')
                print(url)
            return 'Connection error'

    html = br.response().read()
    soup = BeautifulSoup(html, "html.parser")

    # Dropping first character of returned age group, which always appears to be gender.
    age_group = soup.find_all('td', {'class': 'f-age_class'})[0].text[1:]

    if age_group != 'H' and age_group != 'JA' and age_group != '':
        # To have consistent formatting, express age_group as a range        
        age_group = age_group + '-' + str(int(age_group) + 4)            
    
    bib_number = soup.find_all('td', {'class': 'f-start_no_text'})[0].text
    full_name = soup.find_all('td', {'class': 'f-__fullname'})[0].text
    
    # Modified from here:
    # https://stackoverflow.com/a/4894156/3905509
    country = convert_to_ascii(full_name[full_name.find("(")+1:full_name.find(")")])

    rank_gender = soup.find_all('td', {'class': 'f-place_all'})[0].text
    rank_age_group = soup.find_all('td', {'class': 'f-place_age'})[0].text

    if year == 2014:
        splits_table = soup.find_all('table', {'class': 'list-table'})[3]
    else:
        splits_table = soup.find_all('table', {'class': 'list-table'})[4]

    headers_index = ['year', 'bib', 'age_group', 'gender', 'country', 'rank_gender', 'rank_age_group']
    headers = headers_index.copy()
    cols_constant = [year, bib_number, age_group, gender, country, rank_gender, rank_age_group]
    for header_name in splits_table.find_all('tr')[0]:
        if type(header_name) is not bs4.element.NavigableString:        
            headers.append(header_name.get_text())

    # Ensure headers are lowercase for downstream convention
    headers = [header.lower() for header in headers]

    # Populate data
    df = pd.DataFrame(columns=headers)
    for split_row in splits_table.find_all('tr'):    
        split_row_name = split_row.find_all('th')[0].text
        cols = split_row.find_all('td')
        cols = cols_constant + [split_row_name] + [cell.text.strip() for cell in cols]    
        cols = [dict(zip(headers, cols))]
        df_row = pd.DataFrame(cols, columns=headers)
        # First element of split_row contains metadata that we don't want to scrap.
        if split_row_name != 'Split':
            df = df.append(df_row)

    # Reset index of dataframe since each row was individually appended
    df.reset_index(drop=True, inplace=True)
    
    # Only keep relevant fields
    if 'zeit' in df.columns:
        df = df[headers_index + ['split', 'zeit']]
        df.rename(columns={'zeit': 'time'}, inplace=True)
    elif 'time' in df.columns:
        df = df[headers_index + ['split', 'time']]

    # Convert split times into numeric seconds from strings.
    # Modified from the following:
    # https://stackoverflow.com/a/44445488/3905509
    df['time'] = pd.to_timedelta(df['time']).dt.total_seconds()

    # Convert split labels to lowercase
    df['split'] = df['split'].str.lower()

    # Pivot scraped data into 1 row for convenience
    df = pd.pivot_table(
        df,
        index=headers_index,
        columns='split',
        values='time',
        aggfunc='first'
    ).reset_index()

    # Reorder split times for convenience
    headers_splits = ['5 km', '10 km', '15 km', '20 km', 'halb', '25 km', '30 km', '35 km', '40 km', 'finish']    
    headers = headers_index.copy() + headers_splits
    df = df.reindex(headers, axis='columns')
    
    df.rename(columns={'5 km': '5k', '10 km': '10k', '15 km': '15k', '20 km': '20k', 'halb': 'half', '25 km': '25k',
                       '30 km': '30k', '35 km': '35k', '40 km': '40k'}, inplace=True)
    
    df = pd.DataFrame(df.to_records()).drop('index', axis='columns')

    return df


def scrape_berlin_marathon(path_input, path_output, path_error, year, gender, headers, df_urls=None):
    """
    Method to scrape all Berlin Marathon data for a given year and gender using output from
    `scrape_berlin_marathon_urls` and `scrape_berlin_runner_details`.

    * If running for first time, the input `df_urls` should be direct output from `scrape_berlin_marathon_urls`.

    * If restarting a prior scraping run, leave `df_urls` as None or empty and specify the input caching file
      `path_input`, which is a subset of output from `scrape_berlin_marathon_urls`.

    Each row of `path_input` is used to scrape an individual runner's split times. The scraped data is inserted into
    the `path_output` file and then the row from `path_input` is deleted to log the completed scrape.

    **Note**: The `headers` input is assumed to contain the same headers as returned by `scrape_berlin_runner_details`.
    If the code for this function changes, the input headers should be modified.

    The final output of this method is the populated file designated by `path_output` (nothing is returned).

    Example::

        # FIRST SCRAPING RUN
        scraped_df_url = scrape_berlin_marathon_urls(url='http://results.scc-events.com/2016/',
                                                     event='MAL_99999905C9AF3F0000000945', year=2016, gender='M',
                                                     num_results_per_page=100, unit_test_ind=True)

        scrape_berlin_marathon(path_input='test_input_berlin.csv', path_output='test_output_berlin.csv',
                               path_error='test_error_log_berlin.csv', year=2016, gender='M', headers=headers_berlin,
                               df_urls=scraped_df_url)

        # SECOND AND SUBSEQUENT SCRAPING RUNS
        scrape_berlin_marathon(path_input='test_input_berlin.csv', path_output='test_output_berlin.csv',
                               path_error='test_error_log_berlin.csv', year=2016, gender='M', headers=headers_berlin)

    :param str path_input: Path for file containing exported results from scrape_berlin_marathon_urls. If it does not
                           exist and df_urls is supplied, it will be created and populated with data exported from
                           df_urls.
    :param str path_output: Path for file containing exported results from scrape_berlin_runner_details. If it does
                            not exist, it will be created.
    :param str path_error: Path for file containing a log of records from path_input that could not be processed due to
                           a connectivity error.
    :param int year: Year of marathon (supported values: 2014, 2015, 2016, 2017)
    :param str gender: Gender of runner ('M' for male, 'W' for female)
    :param list[str] headers: List of strings representing expected headers for scrape_berlin_runner_details.
    :param pandas.DataFrame df_urls: DataFrame containing output from scrape_berlin_marathon_urls. This should only be
                                     included when running the first scraping for that year & gender.
    """
    # Assume headers is a list. Convert it to a flattened string.
    headers = '|'.join(headers) + '\n'
    
    # Check if the expected input file of URLs exists or not
    check_file_input = os.path.isfile(path_input)
    
    # Export df_urls if the input file doesn't exist, i.e., starting from scratch.
    if not check_file_input and df_urls is not None:
        df_urls.to_csv(path_input, header=False, index=False, sep='|')

        len_input = row_count_csv(path_input)

        # Need to remove blank line created by Pandas for Windows machines
        # See the following link for details:
        # https://github.com/pandas-dev/pandas/issues/20353#issuecomment-392302201
        if sys.platform == 'win32' and len_input > 1:
            delete_last_line_csv(path_input)
    else:
        len_input = row_count_csv(path_input)
        
    # Check if expected output file of scraped data exists or not
    check_file_output = os.path.isfile(path_output)
    
    # Create output file and append expected header row if it doesn't exist.
    if not check_file_output:
        with open(path_output, 'w', encoding="utf-8") as output_file:
            output_file.write(headers)
            
    # Check if expected error log exists or not
    check_file_error = os.path.isfile(path_error)
    
    # Create output file and append expected header row if it doesn't exist.
    if not check_file_error:
        with open(path_error, 'w', encoding="utf-8") as error_file:
            error_file.write('failed_urls\n')

    len_input = row_count_csv(path_input) 
    
    print('Starting to scrape Berlin Marathon split times...')
    scrape_count = 0
    while os.stat(path_input).st_size > 0:        
        # Grab last line of input file and scrape its associated data
        row_input = get_last_line_csv(path_input).strip()
        
        runner_output = scrape_berlin_runner_details(
            url=row_input,
            year=year,
            gender=gender
        )
        
        # Handle cases where scrape_london_runner_details has a connection issue. Often, these are random and could be
        # retried later. The current path_input row is appended to an error log.
        if type(runner_output).__name__ == 'str' and runner_output == 'Connection error':            
            with open(path_error, 'a', encoding="utf-8") as error_file:
                error_file.write(row_input)
                error_file.write('\n')
            delete_last_line_csv(path_input)
            sleep(0.5)
            print('Reducing total number of runners...')
            len_input -= 1
            continue
        
        output_string = re.sub(' +', '|', runner_output.to_string(header=False, index=False))[1:] + '\n'

        # Append scraped data to the output file path_output
        with open(path_output, 'a', encoding="utf-8") as output_file:
            output_file.write(output_string)

        delete_last_line_csv(path_input)
        scrape_count += 1
        print('Progress: ' + str(scrape_count) + ' of ' + str(len_input), end='\r')
        sleep(0.5)
    
    print('')
    print('Scraping of split times complete!')
