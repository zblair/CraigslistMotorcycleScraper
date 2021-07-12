from craigslist import CraigslistForSale
from matplotlib import pyplot as plt
import numpy


class MotorcycleMake:
    """A motorcycle make that will be plotted in the graph"""
    def __init__(self, name, marker_format, line_format):
        self.name = name
        self.marker_format = marker_format
        self.line_format = line_format
        self.num_results = 0
        self.sum_of_prices = 0


# Parameters of the motorcycle search
location = 'vancouver'
years = range(1995, 2021)
makes = [MotorcycleMake('Harley', 'yo', 'y--'),
         MotorcycleMake('Honda', 'r.', 'r--'),
         MotorcycleMake('Kawasaki', 'g+', 'g:'),
         MotorcycleMake('Triumph', 'm.', 'm-'),
         MotorcycleMake('Yamaha', 'co', 'c-.')]

# Calculate the average price for each make and year
make_names = [m.name for m in makes]
average_prices = {key: list() for key in make_names}
for y in years:
    print(f"Querying Craigslist for year {y}...")
    cl = CraigslistForSale(site=location, category='mca', filters={'min_year': y, 'max_year': y})
    results = cl.get_results()

    for make in makes:
        make.sum_of_prices = 0
        make.num_results = 0

    # Get all of the results. Note that iterating over results actually makes requests to CL so we only
    # want to iterate over results once and not put it in an inner loop
    for result in results:
        for make in makes:
            if make.name in result['name']:
                make.num_results = make.num_results + 1
                make.sum_of_prices = make.sum_of_prices + int(result['price'].strip('$').replace(',', ''))

    for make in makes:
        average_price = (make.sum_of_prices / make.num_results) if make.num_results > 0 else 0
        average_prices[make.name].append(average_price)

# Plot the prices vs the year
print("Building an X-Y plot for average price vs model year for each make...")
for make in makes:

    # Ignore years for which we found no entries or the average price was zero
    raw_prices = average_prices[make.name]
    nonzero_prices = []
    nonzero_years = []
    for i in range(0, len(years)):
        if raw_prices[i] > 0:
            nonzero_years.append(years[i])
            nonzero_prices.append(raw_prices[i])

    plt.plot(nonzero_years, nonzero_prices, make.marker_format, label=make.name)

    # Show a trend line
    z = numpy.polyfit(nonzero_years, nonzero_prices, 1)
    p = numpy.poly1d(z)
    plt.plot(years, p(years), make.line_format, label=make.name)

plt.title("Average Motorcycle Prices By Year and Make")
plt.xlabel('Year')
plt.ylabel('Price')
plt.figlegend()
plt.show()
