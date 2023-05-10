import csv
from collections import defaultdict


def summarize_whisky_sales(input_file, output_file):
    # Create a dictionary to store the summarized sales data
    summarized_data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    # Read the input file
    with open(input_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Abbreviate the property name
            if "Malt, First fill bourbon" in row['Property']:
                property_abbr = "WHISKY " + row['Property'].split(", ")[0][:3].upper() + " MFFB " + \
                                row['Property'].split(", ")[3]
            elif "Malt, Refill hogshead" in row['Property']:
                property_abbr = "WHISKY " + row['Property'].split(", ")[0][:3].upper() + " MRH " + \
                                row['Property'].split(", ")[3]
            elif "Malt, Refill bourbon" in row['Property']:
                property_abbr = "WHISKY " + row['Property'].split(", ")[0][:3].upper() + " MRB " + \
                                row['Property'].split(", ")[3]

            # Sum up the sales prices, cost basis, and realised gain for transactions on the same date
            summarized_data[property_abbr][row['Date sold']]['Sales price'] += float(
                row['Sales price'].replace('$', '').replace(',', ''))
            summarized_data[property_abbr][row['Date sold']]['Cost basis'] += float(
                row['Cost basis'].replace('$', '').replace(',', ''))
            summarized_data[property_abbr][row['Date sold']]['Realised Gain'] += float(
                row['Realised Gain'].replace('$', '').replace(',', ''))

    # Write the summarized data to the output file
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Property', 'Date acquired', 'Date sold', 'Sales price', 'Cost basis', 'Realised Gain']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for property_abbr, dates in summarized_data.items():
            for date_sold, sales_data in dates.items():
                writer.writerow({'Property': property_abbr, 'Date acquired': 'VARIOUS', 'Date sold': date_sold,
                                 'Sales price': "${:,.0f}".format(sales_data['Sales price']),
                                 'Cost basis': "${:,.0f}".format(sales_data['Cost basis']),
                                 'Realised Gain': "${:,.0f}".format(sales_data['Realised Gain'])})


# Example usage
summarize_whisky_sales("input.csv", "output.csv")