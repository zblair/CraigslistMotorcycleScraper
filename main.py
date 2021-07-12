from craigslist import CraigslistForSale
from matplotlib import pyplot as plt
import numpy

# Parameters of the motorcycle search
location = 'vancouver'
years = range(1995, 2021)
makes = ['Harley', 'Honda', 'Kawasaki', 'Triumph', 'Yamaha']
marker_formats = {'Harley': 'yo', 'Honda': 'r.', 'Kawasaki': 'g+', 'Triumph': 'm.', 'Yamaha': 'co'}
line_formats = {'Harley': 'y-', 'Honda': 'r--', 'Kawasaki': 'g:', 'Triumph': 'm-', 'Yamaha': 'c-.'}

# Calculate the average price for each make and year
average_prices = {}
for make in makes:
    average_prices[make] = []

if __name__ == '__main__':

    for y in years:
        print(f"Querying Craigslist for year {y}...")
        cl = CraigslistForSale(site=location, category='mca', filters={'min_year': y, 'max_year': y})
        results = cl.get_results()

        num_results = {}
        sum_of_prices = {}
        for make in makes:
            sum_of_prices[make] = 0
            num_results[make] = 0

        # Get all of the results. Note that iterating over results actually makes requests to CL so we only
        # want to iterate over results once and not put it in an inner loop
        for result in results:
            for make in makes:
                if make in result['name']:
                    num_results[make] = (num_results[make] + 1) if (make in num_results) else 1
                    sum_of_prices[make] = (sum_of_prices[make] if (make in sum_of_prices) else 0) + int(result['price'].strip('$').replace(',', ''))

        for make in makes:
            average_price = (sum_of_prices[make] / num_results[make]) if num_results[make] > 0 else 0
            average_prices[make].append(average_price)

    # Plot the prices vs the year
    print("Building an X-Y plot for average price vs model year for each make...")
    for make in makes:
        plt.plot(years, average_prices[make], marker_formats[make], label=make)

        # Show a trend line
        z = numpy.polyfit(years, average_prices[make], 1)
        p = numpy.poly1d(z)
        plt.plot(years, p(years), line_formats[make], label=make)

    plt.title("Average Motorcycle Prices By Year and Make")
    plt.xlabel('Year')
    plt.ylabel('Price')
    plt.figlegend()
    plt.show()
